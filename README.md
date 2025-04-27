# Generador de Contenido para Reels con IA

Un sistema sofisticado de generación de contenido que crea descripciones atractivas para productos de comercio electrónico mediante la extracción de información de productos y el uso de IA para generar contenido de marketing convincente.

## 💯 Ventajas de Usar esta Aplicación

- **Ahorro de Tiempo**: Reduce drásticamente el tiempo necesario para crear contenido de marketing de alta calidad.
- **Consistencia de Marca**: Mantiene un tono consistente en todas las descripciones de productos.
- **Escalabilidad**: Genera contenido para cientos de productos sin esfuerzo adicional.
- **Adaptabilidad**: Personaliza fácilmente el contenido para diferentes audiencias y canales.
- **Mejora de Conversiones**: Crea descripciones persuasivas que incrementan las tasas de conversión.
- **Multilingüe**: Elimina barreras de idioma generando contenido en varios idiomas.
- **Optimización de Recursos**: Libera a los equipos creativos para tareas de mayor valor.
- **Análisis Visual**: Incorpora detalles visuales importantes que podrían pasarse por alto.
- **Actualización Sencilla**: Adapta rápidamente el contenido cuando cambian los productos o las tendencias del mercado.
- **Sin Necesidad de Conocimientos Técnicos**: Interfaz intuitiva accesible para usuarios sin experiencia técnica.

## 🌟 Características

- **Web Scraping**: Extrae automáticamente información de productos de sitios de comercio electrónico
- **Generación de Contenido con IA**: Crea guiones de marketing adaptados a audiencias y tonos específicos
- **Análisis de Imágenes**: Genera descripciones a partir de imágenes de productos utilizando modelos de visión artificial
- **Refinamiento de Contenido**: Adapta el contenido para diferentes audiencias objetivo y estilos de escritura
- **Soporte Multilingüe**: Genera contenido tanto en español como en inglés

## 📋 Arquitectura del Sistema

El proyecto sigue una arquitectura de microservicios con dos componentes principales:

### Servicios Backend

- **Motor de Web Scraping**: Extrae detalles de productos a partir de URLs
- **Servicio de Análisis de Imágenes**: Genera descripciones a partir de imágenes de productos
- **Motor de Generación de Contenido**: Crea guiones de marketing utilizando modelos de IA a través de Groq
- **Servidor FastAPI**: Proporciona endpoints de API RESTful para el frontend

### Interfaz Frontend

- **Aplicación Streamlit**: Interfaz amigable para generar contenido
- **Configuración de Entrada**: Opciones para audiencia objetivo, tono e idioma
- **Visualización de Salida**: Muestra el contenido generado con opciones de descarga

## 🛠️ Tecnologías Utilizadas

- **Backend**:
  - Python 3.9
  - FastAPI
  - Langchain
  - Groq API (integración LLM)
  - Selenium & BeautifulSoup (web scraping)
  - Modelos de visión para análisis de imágenes

- **Frontend**:
  - Streamlit
  - Requests

- **Infraestructura**:
  - Docker & Docker Compose
  - Configuración de entorno mediante dotenv

## 🚀 Primeros Pasos

### Requisitos Previos

- Docker y Docker Compose
- Clave API de Groq

### Instrucciones de Configuración

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tunombredeusuario/ai-reel-content-generator.git
   cd ai-reel-content-generator
   ```

2. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   GROQ_API_KEY="tu_clave_api_de_groq"
   MODEL_NAME="gemma2-9b-it"
   VISION_MODEL_NAME="deepseek-r1-distill-llama-70b"
   BACKEND_URL="http://backend:8004/content_generator"
   ```

3. Construye y ejecuta la aplicación usando Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Accede a la aplicación:
   - Frontend: Abre tu navegador y navega a `http://localhost:8501`
   - API Backend: Disponible en `http://localhost:8004`

## 📝 Uso

1. Ingresa la URL de un producto de comercio electrónico
2. Selecciona tu audiencia objetivo (ej. "Adultos jóvenes (25-35 años)")
3. Elige el tono deseado (ej. "Profesional", "Casual", "Motivacional")
4. Selecciona el idioma (Español o Inglés)
5. Haz clic en "Generar Guion" para crear tu contenido de marketing
6. Descarga el contenido generado como JSON

## 🧩 Estructura del Proyecto

```
.
├── .env                        # Variables de entorno
├── .gitignore                  # Archivo de ignorados para Git
├── docker-compose.yml          # Configuración de Docker Compose
├── backend/                    # Servicio backend
│   ├── Dockerfile              # Configuración Docker del backend
│   ├── requirements.txt        # Dependencias de Python
│   ├── models/                 # Modelos de datos
│   ├── prompts/                # Prompts para LLM
│   └── src/                    # Código fuente
│       ├── content_generator.py # Lógica de generación de contenido
│       ├── image_describer.py  # Servicio de análisis de imágenes
│       ├── llm.py              # Integración con LLM
│       ├── scraping.py         # Lógica de web scraping
│       └── server.py           # Servidor FastAPI
└── frontend/                   # Aplicación frontend
    ├── Dockerfile              # Configuración Docker del frontend
    ├── requirements.txt        # Dependencias de Python
    ├── models/                 # Modelos de datos
    └── src/                    # Código fuente
        ├── generate_content.py # Solicitudes de generación de contenido
        └── ui.py               # Interfaz de usuario Streamlit
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! No dudes en enviar un Pull Request.

1. Haz un fork del repositorio
2. Crea tu rama de características (`git checkout -b feature/caracteristica-asombrosa`)
3. Confirma tus cambios (`git commit -m 'Añadir alguna característica asombrosa'`)
4. Envía a la rama (`git push origin feature/caracteristica-asombrosa`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.

## 🙏 Agradecimientos

- [Groq](https://groq.com/) por proporcionar la API de LLM
- [Langchain](https://github.com/langchain-ai/langchain) por el framework de LLM
- [Streamlit](https://streamlit.io/) por la interfaz web
- [FastAPI](https://fastapi.tiangolo.com/) por la API backend
- [Selenium](https://www.selenium.dev/) y [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) por las capacidades de web scraping
