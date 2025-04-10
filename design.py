import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_elements import elements, mui, html
from streamlit_card import card
import hydralit_components as hc
import time

def set_custom_style():
    """Configura los estilos personalizados de la interfaz"""
    # Detectar el tema actual
    is_dark_theme = st.get_option("theme.base") == "dark"
    
    # Colores base según el tema
    colors = {
        "light": {
            "bg": "#ffffff",
            "text": "#1e293b",
            "primary": "#6366f1",
            "secondary": "#8b5cf6",
            "accent": "#3b82f6",
            "surface": "#f8fafc",
            "border": "#e2e8f0",
            "hover": "#f1f5f9"
        },
        "dark": {
            "bg": "#0f172a",
            "text": "#e2e8f0",
            "primary": "#818cf8",
            "secondary": "#a78bfa",
            "accent": "#60a5fa",
            "surface": "#1e293b",
            "border": "#334155",
            "hover": "#1e293b"
        }
    }
    
    theme = colors["dark"] if is_dark_theme else colors["light"]
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
        
        /* Estilos generales */
        .stApp {{
            font-family: 'Inter', sans-serif;
            background-color: {theme["bg"]};
            color: {theme["text"]};
        }}
        
        /* Contenedor principal */
        .main-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 1.5rem;
        }}
        
        /* Encabezado */
        .main-header {{
            background: linear-gradient(135deg, {theme["primary"]}, {theme["secondary"]});
            color: white;
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}
        
        /* Tarjetas de capacidades */
        .capability-card {{
            background: {theme["surface"]};
            padding: 1.5rem;
            border-radius: 1rem;
            border: 1px solid {theme["border"]};
            margin: 0.75rem 0;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        
        .capability-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        }}
        
        /* Mensajes del chat */
        .chat-message {{
            padding: 1.25rem;
            border-radius: 1rem;
            margin: 0.75rem 0;
            background: {theme["surface"]};
            border: 1px solid {theme["border"]};
        }}
        
        .chat-message.user {{
            background: {theme["primary"] + "15"};
            border-left: 4px solid {theme["primary"]};
        }}
        
        .chat-message.assistant {{
            background: {theme["secondary"] + "15"};
            border-left: 4px solid {theme["secondary"]};
        }}
        
        /* Input del chat */
        .stTextInput > div > div > input {{
            background: {theme["surface"]} !important;
            border: 2px solid {theme["border"]} !important;
            border-radius: 1rem !important;
            color: {theme["text"]} !important;
            padding: 0.75rem 1rem !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: {theme["primary"]} !important;
            box-shadow: 0 0 0 2px {theme["primary"] + "40"} !important;
        }}
        
        /* Botones */
        .stButton > button {{
            background: linear-gradient(135deg, {theme["primary"]}, {theme["secondary"]}) !important;
            color: white !important;
            border: none !important;
            padding: 0.5rem 1.25rem !important;
            border-radius: 1rem !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px {theme["primary"] + "40"} !important;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {theme["surface"]};
            border-right: 1px solid {theme["border"]};
        }}
        
        /* Estado del sistema */
        .status-badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.4rem 1rem;
            border-radius: 2rem;
            font-size: 0.875rem;
            font-weight: 500;
            background: {theme["primary"] + "20"};
            color: {theme["primary"]};
        }}
        
        /* Scrollbar personalizado */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {theme["surface"]};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {theme["primary"]};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {theme["secondary"]};
        }}
        
        /* Animaciones */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate-fade-in {{
            animation: fadeIn 0.5s ease forwards;
        }}
        
        /* Código */
        .code-block {{
            background: {theme["bg"] if not is_dark_theme else "#1a1a1a"};
            color: {theme["text"]};
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid {theme["border"]};
            font-family: 'JetBrains Mono', monospace;
            margin: 1rem 0;
            position: relative;
        }}
        
        /* Enlaces */
        a {{
            color: {theme["primary"]};
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        
        a:hover {{
            color: {theme["secondary"]};
            text-decoration: underline;
        }}
        </style>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Muestra la barra lateral con información sobre VictorIA"""
    with st.sidebar:
        # Logo y título con estilo mejorado
        st.markdown("""
        <div style='text-align: center; margin-bottom: 1.5rem;'>
            <img src="https://i.imgur.com/SvRc5db.jpeg" style="width: 90px; border: 2px solid #e5e7eb; border-radius: 50%; padding: 0.5rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        </div>
        """, unsafe_allow_html=True)
        # Estado del sistema
        st.markdown("""
        <div style='text-align: center'>
            <h2 style='margin-bottom: 0.5rem;'>VictorIA 🤖</h2>
            <div class='status-badge online'>
                Sistema Activo
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Menú de navegación
        selected = option_menu(
            menu_title=None,
            options=["💬 Chat", "📚 Docs", "💡 Ejemplos", "ℹ️ Acerca de"],
            default_index=0,
            styles={
                "container": {"padding": "0.5rem"},
                "nav-link": {
                    "font-size": "1rem",
                    "text-align": "left",
                    "margin": "0.2rem 0",
                    "padding": "0.8rem 1rem",
                    "border-radius": "0.5rem"
                }
            }
        )
        
        if selected == "ℹ️ Acerca de":
            st.markdown("""
            <div class="animate-fade-in">
            ### Sobre VictorIA
            
            Desarrollada por estudiantes de la Universidad Andrés Bello El Salvador.
            
            **Versión:** 1.0.0  
            **Actualización:** Marzo 2025
            
            #### Tecnologías
            - Python 3.11
            - Streamlit
            - scikit-learn
            - OpenAI API
            </div>
            """, unsafe_allow_html=True)
        
        # Separador
        st.markdown("<hr style='margin: 1.5rem 0; border-color: #e5e7eb;'>", unsafe_allow_html=True)
        
        # Enlaces útiles
        st.markdown("""
        <div class="animate-fade-in">
        ### Enlaces Útiles
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(2)
        with cols[0]:
            st.link_button("📚 Docs", "https://docs.victoria.ai", use_container_width=True)
            st.link_button("💡 Ejemplos", "https://examples.victoria.ai", use_container_width=True)
        with cols[1]:
            st.link_button("🤝 Soporte", "mailto:soporte@victoria.ai", use_container_width=True)
            st.link_button("🌟 GitHub", "https://github.com/victoria-ai", use_container_width=True)
        
        # Información adicional
        st.markdown("""
        <div style="margin-top: 2rem; font-size: 0.8rem; color: #6b7280; text-align: center;">
            © 2025 VictorIA - UNAB El Salvador
        </div>
        """, unsafe_allow_html=True)

def show_capabilities():
    """Muestra las capacidades de Victoria en formato de tarjetas"""
    capabilities = [
        {
            "icon": "🧠",
            "title": "Machine Learning",
            "features": [
                "Modelos de clasificación y regresión",
                "Clustering y segmentación",
                "Optimización automática de modelos"
            ],
            "color": "#4f46e5"
        },
        {
            "icon": "📈",
            "title": "Visualización",
            "features": [
                "Gráficos interactivos con Plotly",
                "Dashboards dinámicos",
                "Análisis visual de patrones"
            ],
            "color": "#7c3aed"
        },
        {
            "icon": "🔍",
            "title": "Análisis Exploratorio",
            "features": [
                "Informes automáticos de datos",
                "Detección de outliers",
                "Análisis de correlaciones"
            ],
            "color": "#2563eb"
        },
        {
            "icon": "💡",
            "title": "Mejores Prácticas",
            "features": [
                "Código limpio y documentado",
                "Validación de datos",
                "Seguridad y ética en el análisis"
            ],
            "color": "#9333ea"
        }
    ]
    
    # Crear un grid de 2x2 para las tarjetas
    col1, col2 = st.columns(2)
    cols = [col1, col2]
    
    for i, cap in enumerate(capabilities):
        with cols[i % 2]:
            with elements("capability_" + str(i)):
                with mui.Card(
                    sx={
                        "background": "white",
                        "borderRadius": "1rem",
                        "padding": "1.5rem",
                        "marginBottom": "1rem",
                        "transition": "all 0.3s ease",
                        "&:hover": {
                            "transform": "translateY(-4px)",
                            "boxShadow": "0 12px 20px -8px rgba(0, 0, 0, 0.15)"
                        },
                        "borderTop": f"4px solid {cap['color']}"
                    }
                ):
                    mui.Box(
                        children=[
                            html.div(
                                cap["icon"],
                                style={"fontSize": "2.5rem", "marginBottom": "0.5rem"}
                            ),
                            mui.Typography(
                                cap["title"],
                                variant="h5",
                                sx={"fontWeight": "600", "color": cap["color"]}
                            ),
                            mui.List(
                                [mui.ListItem(
                                    mui.ListItemText(feature)
                                ) for feature in cap["features"]],
                                sx={"paddingLeft": 0}
                            )
                        ]
                    )

def format_code_blocks(text):
    """Formatea los bloques de código con sintaxis resaltada"""
    import re
    code_blocks = re.finditer(r'```(?:python)?(.*?)```', text, re.DOTALL)
    formatted_text = text
    
    for block in code_blocks:
        code = block.group(1).strip()
        formatted_code = f"""
        <div class="code-block">
            <pre><code class="python">{code}</code></pre>
        </div>
        """
        formatted_text = formatted_text.replace(block.group(0), formatted_code)
    
    return formatted_text

def show_header():
    """Muestra el encabezado principal de la aplicación"""
    st.markdown("""
        <div class='main-header animate-fade-in'>
            <h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 1rem;'>
                VictorIA 🤖
            </h1>
            <p style='font-size: 1.2rem; opacity: 0.9; line-height: 1.5;'>
                Tu asistente inteligente para análisis de datos y programación
            </p>
        </div>
    """, unsafe_allow_html=True)

def init_page():
    """Inicializa la configuración de la página"""
    st.set_page_config(
        page_title="VictorIA - Asistente de Análisis de Datos",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://docs.victoria.ai',
            'Report a bug': 'https://github.com/victoria-ai/issues',
            'About': 'VictorIA - Desarrollada por estudiantes de UNAB El Salvador'
        }
    )
    set_custom_style()

def show_chat_message(role, content, avatar=None):
    """Muestra un mensaje individual del chat con estilo mejorado"""
    with st.chat_message(role, avatar=avatar):
        message_class = "user" if role == "user" else "assistant"
        st.markdown(f"""
            <div class='chat-message {message_class} animate-slide-in'>
                {format_code_blocks(content) if role == "assistant" else content}
            </div>
        """, unsafe_allow_html=True)

def show_chat_interface(chatbot):
    """Muestra la interfaz del chat"""
    # Contenedor para el historial de chat
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-history">', unsafe_allow_html=True)
        # Mostrar historial
        for message in st.session_state.messages:
            show_chat_message(
                role=message["role"],
                content=message["content"],
                avatar="🤖" if message["role"] == "assistant" else None
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # Input del usuario con estilo mejorado
    if prompt := st.chat_input("¿En qué puedo ayudarte con tu análisis de datos? 💭"):
        # Agregar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        show_chat_message("user", prompt)

        # Generar respuesta
        response = chatbot.generate_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    # Inicializar la configuración de página
    init_page()
    
    # Mostrar sidebar (siempre visible)
    show_sidebar()
    
    # Contenedor principal condicional
    if "ui_initialized" not in st.session_state:
        # Elementos que solo deben mostrarse una vez
        show_header()
        show_capabilities()
        st.markdown("<hr style='margin: 2rem 0; border-color: #e9ecef;'>", unsafe_allow_html=True)
        st.session_state.ui_initialized = True  # Marcar como mostrado
    
    # Inicializar chatbot y mensajes
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = VictoriaChatbot()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Mostrar interfaz de chat (siempre visible)
    show_chat_interface(st.session_state.chatbot)

if __name__ == "__main__":
    main()