import requests
from models.content_generation_models import ContentGeneration
import streamlit as st


def compute_content(payload: ContentGeneration, server_url: str):
    try:
        # Enviar solicitud POST al servidor con el payload
        r = requests.post(
            server_url,
            json=payload.dict(),
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        # Lanzar excepción si la solicitud falla
        r.raise_for_status()

        # Extraer el contenido generado de la respuesta
        response_data = r.json()
        
        # Obtener el contenido refinado del diccionario de respuesta
        generated_content = response_data.get("generated_content", {}).get("refined_content", "")
        
        # Limpiar el prefijo "refined_content=" si existe
        if generated_content.startswith("refined_content="):
            generated_content = generated_content[len("refined_content="):]
            
        # Reemplazar los saltos de línea literales "\n" con espacios
        generated_content = generated_content.replace("\\n", " ")
        
        return generated_content
    except requests.exceptions.RequestException as e:
        # Manejar excepciones de solicitud y devolver un mensaje de error
        st.error(f"Error al comunicarse con el servidor: {str(e)}")
        return None