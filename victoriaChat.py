import os
import re
from openai import OpenAI
from dotenv import load_dotenv
import time
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
import xgboost as xgb
import streamlit as st
import design
import json
import threading
import openai
import warnings

# Suprimir advertencias específicas de secuencias de escape inválidas
warnings.filterwarnings("ignore", category=SyntaxWarning, module="streamlit.elements.lib.column_types")
warnings.filterwarnings("ignore", category=SyntaxWarning, module="streamlit.elements.widgets.button")
warnings.filterwarnings("ignore", category=SyntaxWarning, module="streamlit_elements.core.callback")
# Suprimir específicamente el aviso de \W en streamlit_elements
warnings.filterwarnings("ignore", message="invalid escape sequence '\\W'")

# Configuración de la página (DEBE ser la primera llamada a Streamlit)
st.set_page_config(
    page_title="VictorIA - Asistente de Minería de Datos",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.victoria.ai',
        'Report a bug': 'https://github.com/victoria-ai/issues',
        'About': 'VictorIA - Desarrollada por estudiantes de UNAB El Salvador'
    }
)

# Cargar variables de entorno SOLO en entorno local
if not st.secrets.get("RUNNING_IN_STREAMLIT_CLOUD", False):
    load_dotenv()

# Aplicar estilos personalizados
design.set_custom_style()

class SecurityValidator:
    def __init__(self):
        self.blocked_patterns = [
            r"(SELECT|INSERT|UPDATE|DELETE).*FROM",  # SQL injection
            r"requests\.get\(|urllib\.request|selenium",  # Web scraping
            r"exec\(|eval\(|os\.(system|popen)",  # Code injection
            r"\.exe|\.dll|\.bat|\.sh",  # Executable files
            r"(rm|rmdir|del|format).*-rf"  # Dangerous system commands
        ]
    
    def validate_input(self, message):
        # Validación de intención
        if any(pattern in message.lower() for pattern in ["hack", "crack", "exploit", "vulnerability"]):
            return False, "Solicitud potencialmente maliciosa detectada"
        
        # Validación de patrones bloqueados
        for pattern in self.blocked_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return False, "Patrón de código potencialmente peligroso detectado"
        
        return True, ""

class MLTools:
    @staticmethod
    def auto_ml(X, y, task='classification', custom_params=None):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        models = {
            'classification': [
                ('logistic', LogisticRegression()),
                ('rf', RandomForestClassifier()),
                ('xgb', xgb.XGBClassifier())
            ],
            'regression': [
                ('xgb', xgb.XGBRegressor())
            ],
            'clustering': [
                ('kmeans', KMeans())
            ]
        }
        
        best_score = float('-inf')
        best_model = None
        
        for name, model in models.get(task, []):
            if custom_params:
                grid = GridSearchCV(model, custom_params.get(name, {}))
                grid.fit(X_train_scaled, y_train)
                model = grid.best_estimator_
            else:
                model.fit(X_train_scaled, y_train)
            
            score = model.score(X_test_scaled, y_test)
            if score > best_score:
                best_score = score
                best_model = model
        
        return best_model, scaler, best_score

class VictoriaChatbot:
    def __init__(self):
        self.stop_generation = False
        self.response_thread = None
        self.current_response = ""
        self.is_generating = False
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        )
        self.model = "deepseek-chat"
        self.security = SecurityValidator()
        self.system_prompt = """Eres VictorIA, una asistente hombre salvadoreño virtual especializada en **minería de datos y análisis estadístico**, creada por estudiantes de la **Universidad Andrés Bello (UNAB), El Salvador**.  

**Equipo creador:**  
- **Estudiantes:** Héctor, Germán, Miguel, Víctor, Melissa y Melvin.  
- **Ingeniero supervisor:** José Guillermo Rivera Pleitez (Contacto: joseguillermo.rivera@unab.edu.sv)

        Tus capacidades incluyen:
        1. Modelos de Machine Learning:
           - Regresión y clasificación con scikit-learn
           - Modelos avanzados con XGBoost
           - Clustering y segmentación
           - AutoML para optimización automática
        
        2. Visualización de datos:
           - Gráficos interactivos con Plotly
           - Visualizaciones declarativas con Altair
           - Dashboards con Streamlit
           
        3. Análisis exploratorio:
           - Generación automática de informes con pandas-profiling
           - Detección de outliers y patrones
           - Análisis de correlaciones
        
        4. Validación y seguridad:
           - Verificación de intención del usuario
           - Protección contra código malicioso
           - Cumplimiento de normativas GDPR
        """
        self.history = []
    
    def _format_messages(self, user_input):
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.history[-4:],
            {"role": "user", "content": user_input}
        ]
        return messages
    
    def is_code_request(self, message):
        patterns = [
            r"\b(código|programar|script|función|analizar datos)\b",
            r"\b(pandas|numpy|matplotlib|seaborn|python|ml|machine learning)\b",
            r"\b(gráfico|gráfica|visualización|plot|predict|entrenar)\b"
        ]
        return any(re.search(p, message.lower()) for p in patterns)
    
    def validate_request(self, message):
        # Validación de seguridad
        is_safe, warning = self.security.validate_input(message)
        if not is_safe:
            return False, warning
        
        # Validación de longitud
        if len(message) > 2000:
            return False, "Mensaje demasiado largo"
            
        return True, ""
    
    def stop_response(self):
        """Detiene la generación de la respuesta actual"""
        self.stop_generation = True
        self.is_generating = False
        if self.response_thread and self.response_thread.is_alive():
            self.response_thread.join(timeout=1.0)
    
    def generate_response(self, prompt):
        """Genera una respuesta usando la API de Deepseek con streaming"""
        self.stop_generation = False
        self.current_response = ""
        self.is_generating = True
        
        # Crear un contenedor para la respuesta en streaming
        response_container = st.empty()
        stop_button_container = st.empty()
        
        # Mostrar el botón de detener con un diseño más compacto
        with stop_button_container:
            if st.button("🛑", key="stop_button", help="Detener respuesta"):
                self.stop_response()
                st.markdown("""
                    <div style='color: #ff4b4b; font-size: 0.9em;'>
                        Respuesta detenida
                    </div>
                """, unsafe_allow_html=True)
                return self.current_response

        try:
            # Iniciar la generación de respuesta usando Deepseek
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                stream=True
            )

            # Procesar la respuesta en streaming
            for chunk in response:
                if self.stop_generation:
                    break
                
                if hasattr(chunk.choices[0].delta, 'content'):
                    content = chunk.choices[0].delta.content
                    self.current_response += content
                    
                    # Actualizar el contenedor con la respuesta actual usando un diseño más compacto
                    with response_container:
                        st.markdown(f"""
                            <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0;'>
                                {self.current_response}
                            </div>
                        """, unsafe_allow_html=True)

            self.is_generating = False
            return self.current_response

        except Exception as e:
            self.is_generating = False
            return f"Lo siento, ha ocurrido un error: {str(e)}"

    def get_current_response(self):
        """Retorna la respuesta actual"""
        return self.current_response

    def is_generating_response(self):
        """Verifica si está generando una respuesta"""
        return self.is_generating

def main():
    # Verifica si los secrets están configurados correctamente
    if 'DEEPSEEK_API_KEY' not in st.secrets and 'DEEPSEEK_API_KEY' not in os.environ:
        st.error("""
            🔒 API Key no configurada. Por favor:
            
            1. Para desarrollo local: crea un archivo `.env` con tu clave DEEPSEEK_API_KEY
            2. Para producción en Streamlit Cloud: configura los secrets en la configuración de la app
            
            Consulta la documentación para más detalles.
        """)
        return
    
    # Inicializa la interfaz
    design.show_sidebar()
    design.show_header()
    design.show_capabilities()
    
    # Separador visual
    st.markdown("<hr style='margin: 2rem 0; border-color: #e9ecef;'>", unsafe_allow_html=True)
    
    # Inicializar el chatbot
    if "chatbot" not in st.session_state:
        try:
            st.session_state.chatbot = VictoriaChatbot()
        except Exception as e:
            st.error(f"No se pudo inicializar el chatbot: {str(e)}")
            return
    
    # Inicializar historial de mensajes
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar interfaz de chat
    design.show_chat_interface(st.session_state.chatbot)

if __name__ == "__main__":
    main()
