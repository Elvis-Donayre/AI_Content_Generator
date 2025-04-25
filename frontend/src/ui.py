import os
import json
from dotenv import load_dotenv
import streamlit as st
from models.content_generation_models import ContentGeneration
from src.generate_content import compute_content


# TODO: Load environment variables from .env file
load_dotenv()


# TODO: Set the title of the Streamlit app
st.title("AI-Powered Reel Content Generator")

# TODO: Add a description for the app
st.write(
    """
Ingresa una url de un producto para crear el guion
"""
)

# TODO: Create input fields for URL, target audience, tone, and language
input_url = st.text_input("URL del producto:")
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

# TODO: Add a button to trigger content generation
if st.button("Generar Guion"):
    if input_url and new_target_audience and new_tone and language:
        with st.spinner("Generando guion..."):
            backend_url = os.getenv("BACKEND_URL", "http://backend:8004/content_generator")
            # TODO: Create a payload using the ContentGeneration model
            payload = ContentGeneration(
                url=input_url,
                new_target_audience=new_target_audience,
                new_tone=new_tone,
                language=language,
            )

            # TODO: Call the compute_content function to generate the script
            refined_script = compute_content(payload, backend_url)

            # TODO: Display the generated script and add a download button
            if refined_script:
                st.header("Guion Finalizado")
                st.write(refined_script)
                
                # Preparar datos para descargar
                script_data = {
                    "url": input_url,
                    "target_audience": new_target_audience,
                    "tone": new_tone,
                    "language": language,
                    "script": refined_script
                }
                
                script_json = json.dumps(script_data, indent=2, ensure_ascii=False)
                
                st.download_button(
                    label="Descargar Guion en JSON",
                    data=script_json,
                    file_name="guion_generado.json",
                    mime="application/json",
                )
            else:
                st.error("No se pudo generar el guion. Por favor, intenta nuevamente.")
    else:
        # TODO: Show a warning if any input field is missing
        st.warning("Por favor, completa todos los campos.")