import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from groq import Groq


# Cargar variables del archivo .env
load_dotenv()


class GroqModelHandler:
    def __init__(self):
        # TODO: Load the Groq API key and model name from environment variables
        api_key = os.getenv("GROQ_API_KEY")
        model_name = os.getenv("MODEL_NAME", "gemma2-9b-it")

        # TODO: Validate if the API key is provided
        if not api_key:
            raise ValueError(
                "La API Key de Groq no está configurada en el archivo .env"
            )

        # TODO: Initialize the Groq client and ChatGroq LLM
        self.client = Groq(api_key=api_key)
        self.llm = ChatGroq(
            model_name=model_name,
            groq_api_key=api_key,
            temperature=0.7,
            max_tokens=1024,
        )

    def get_client(self):
        # TODO: Return the Groq client instance
        return self.client

    def get_llm(self):
        # Example method for students to follow
        return self.llm