from pydantic import BaseModel, Field


class ContentGenerationScript(BaseModel):
    content: str = Field(..., description="Contenido textual del reel")


# TODO: Define the ToneGenerationScript class with a field for the refined content
class ToneGenerationScript(BaseModel):
    refined_content: str = Field(..., description="Contenido refinado con el tono especificado")


# TODO: Define the ContentGeneration class with fields for URL, target audience, tone, and language
class ContentGeneration(BaseModel):
    url: str = Field(..., description="URL del producto a analizar")
    new_target_audience: str = Field(..., description="Audiencia objetivo del contenido")
    new_tone: str = Field(..., description="Tono deseado para el contenido")
    language: str = Field(..., description="Idioma en el que se generará el contenido")