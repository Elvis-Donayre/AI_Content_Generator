import requests
from models.content_generation_models import ContentGeneration
import streamlit as st


def compute_content(payload: ContentGeneration, server_url: str):
    try:
        # TODO: Send a POST request to the server with the payload
        r = requests.post(
            server_url,
            json=payload.dict(),
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        # TODO: Raise an exception if the request fails
        r.raise_for_status()

        # TODO: Extract and return the generated content from the response
        response_data = r.json()
        generated_content = response_data.get("generated_content", {}).get("refined_content", "")
        return generated_content
    except requests.exceptions.RequestException as e:
        # TODO: Handle request exceptions and return an error message
        st.error(f"Error al comunicarse con el servidor: {str(e)}")
        return None