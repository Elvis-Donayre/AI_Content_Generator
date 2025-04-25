from pydantic import BaseModel


class ContentGeneration(BaseModel):
    url: str  # Example field for students to follow

    # TODO: Add a field for the new target audience
    new_target_audience: str

    # TODO: Add a field for the new tone
    new_tone: str

    # TODO: Add a field for the language
    language: str