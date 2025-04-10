# VictorIA - Asistente Virtual para Análisis de Datos

VictorIA es un chatbot especializado en minería de datos y análisis estadístico, desarrollado por estudiantes de la Universidad Andrés Bello (UNAB) en El Salvador.

## Características

- **Análisis de Datos**: Procesamiento y análisis de datos con pandas y numpy
- **Machine Learning**: Modelos de clasificación, regresión y clustering
- **Visualización**: Gráficos interactivos y dashboards
- **Generación de Código**: Código Python optimizado para análisis de datos
- **Interfaz Moderna**: Diseño atractivo y responsivo con Streamlit
- **Control de Respuestas**: Capacidad para detener la generación de respuestas

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/victoria-chatbot.git
cd victoria-chatbot
```

2. Crea un entorno virtual e instala las dependencias:
```bash
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt
```

3. Configura las variables de entorno:
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```
DEEPSEEK_API_KEY=tu_api_key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

## Uso

Para ejecutar el chatbot:

```bash
streamlit run victoriaChat.py
```

## Equipo

- **Estudiantes**: Héctor, Germán, Miguel, Víctor, Melissa y Melvin
- **Ingeniero supervisor**: José Guillermo Rivera Pleitez

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles. 
