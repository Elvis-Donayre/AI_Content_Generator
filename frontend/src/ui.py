import os
import json
from dotenv import load_dotenv
import streamlit as st
from models.content_generation_models import ContentGeneration
from src.generate_content import compute_content


# Cargar variables de entorno desde .env file
load_dotenv()

# Configuraciones de la página
st.set_page_config(
    page_title="AI-Powered Reel Content Generator",
    page_icon="🎬",
    layout="wide"
)

# Título y descripción principal
st.title("🎬 AI-Powered Reel Content Generator")
st.write(
    """
    Esta aplicación te permite generar guiones para reels de productos utilizando inteligencia artificial.
    **IMPORTANTE**: Esta herramienta funciona exclusivamente con URLs de productos de Falabella Perú (https://www.falabella.com.pe/).
    Simplemente ingresa la URL del producto de Falabella y personaliza las opciones para obtener un guion adaptado a tus necesidades.
    """
)

# Sección de manual de uso con expander
with st.expander("📚 Manual de Uso"):
    st.markdown("""
    ### ¿Cómo usar este generador de guiones?
    
    1. **Ingresa la URL del producto**: Pega el enlace completo del producto de Falabella Perú (https://www.falabella.com.pe/) para el cual deseas crear un guion. SOLO funciona con productos de esta tienda.
    
    2. **Selecciona la audiencia objetivo**: Elige el grupo demográfico al que va dirigido tu reel.
    
    3. **Escoge el tono del guion**: Define el estilo de comunicación que deseas utilizar.
    
    4. **Elige el idioma**: Selecciona si quieres el guion en español o inglés.
    
    5. **Genera el guion**: Haz clic en el botón "Generar Guion" y espera unos segundos.
    
    6. **Descarga tu resultado**: Una vez generado, puedes descargar el guion en formato JSON para guardarlo.
    
    ### Consejos para mejores resultados:
    
    - Usa ÚNICAMENTE URLs de productos de Falabella Perú (https://www.falabella.com.pe/).
    - Asegúrate de que la URL sea de una página de producto específica y no de listados o categorías.
    - El formato correcto de URL debe ser similar a: https://www.falabella.com.pe/falabella-pe/product/[código-producto]/[nombre-producto]
    - Selecciona una audiencia que realmente coincida con el mercado objetivo del producto.
    - El tono "Informativo" es ideal para productos técnicos, mientras que "Emocional" o "Motivacional" funcionan mejor para artículos de estilo de vida.
    """)

# Crear dos columnas para la entrada de datos
col1, col2 = st.columns(2)

with col1:
    # Sección de entrada de datos
    st.subheader("Datos del Producto")
    input_url = st.text_input("URL del producto de Falabella Perú:", placeholder="https://www.falabella.com.pe/falabella-pe/product/...")
    
    new_target_audience = st.selectbox(
        "Audiencia objetivo:",
        options=[
            "Jóvenes (18-25 años)",
            "Adultos jóvenes (25-35 años)",
            "Adultos (35-50 años)",
            "Adultos mayores (50+ años)",
            "Profesionales",
            "Estudiantes",
            "Padres de familia",
            "Deportistas",
        ],
    )

with col2:
    st.subheader("Estilo del Guion")
    new_tone = st.selectbox(
        "Tono:",
        options=[
            "Divertido",
            "Profesional",
            "Informativo",
            "Emocional",
            "Motivacional",
            "Casual",
            "Elegante",
            "Juvenil",
        ],
    )
    
    language = st.selectbox(
        "Idioma:",
        options=["Español", "Inglés"],
    )

# Botón de generación centrado
st.markdown("<br>", unsafe_allow_html=True)  # Espacio adicional
col_button = st.columns(3)
with col_button[1]:
    generate_button = st.button("✨ Generar Guion", use_container_width=True)

# Procesamiento y resultado
if generate_button:
    if input_url and new_target_audience and new_tone and language:
        with st.spinner("⏳ Generando guion... Esto puede tomar unos segundos."):
            backend_url = os.getenv("BACKEND_URL", "http://backend:8004/content_generator")
            # Crear payload usando el modelo ContentGeneration
            payload = ContentGeneration(
                url=input_url,
                new_target_audience=new_target_audience,
                new_tone=new_tone,
                language=language,
            )

            # Llamar a la función compute_content para generar el guion
            refined_script = compute_content(payload, backend_url)

            # Mostrar el guion generado y agregar botón de descarga
            if refined_script:
                st.success("¡Guion generado con éxito!")
                
                # Sección de resultados con estilo
                st.markdown("---")
                st.header("📝 Guion Finalizado")
                
                # Mostrar resumen de parámetros
                st.markdown("**Detalles del guion:**")
                details_col1, details_col2 = st.columns(2)
                with details_col1:
                    st.info(f"**Audiencia:** {new_target_audience}")
                    st.info(f"**Idioma:** {language}")
                with details_col2:
                    st.info(f"**Tono:** {new_tone}")
                
                # Mostrar el guion en un área de texto
                st.markdown("### Contenido del guion:")
                st.text_area("", refined_script, height=250)
                
                # Preparar datos para descargar
                script_data = {
                    "url": input_url,
                    "target_audience": new_target_audience,
                    "tone": new_tone,
                    "language": language,
                    "script": refined_script
                }
                
                script_json = json.dumps(script_data, indent=2, ensure_ascii=False)
                
                # Opciones de descarga
                download_col1, download_col2 = st.columns(2)
                with download_col1:
                    st.download_button(
                        label="📥 Descargar Guion en JSON",
                        data=script_json,
                        file_name="guion_generado.json",
                        mime="application/json",
                    )
                with download_col2:
                    st.download_button(
                        label="📄 Descargar Guion como Texto",
                        data=refined_script,
                        file_name="guion_generado.txt",
                        mime="text/plain",
                    )
            else:
                st.error("No se pudo generar el guion. Por favor, verifica que la URL sea de un producto válido de Falabella Perú e intenta nuevamente.")
    else:
        # Mostrar advertencia si falta algún campo
        st.warning("⚠️ Por favor, completa todos los campos antes de generar el guion. Recuerda que solo funcionan URLs de productos de Falabella Perú.")

# Pie de página
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: gray;">
        Desarrollado por Elvis donayre con ❤️ | AI-Powered Reel Content Generator | © 2025
    </div>
    """, 
    unsafe_allow_html=True
)