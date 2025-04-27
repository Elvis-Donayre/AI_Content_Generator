from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from src.llm import GroqModelHandler
from prompts.content_generation_prompts import GENERATE_INFO
from prompts.tone_generator import GENERATE_REFINED_INFO
from models.content_generation_models import ContentGenerationScript, ToneGenerationScript

class ContentGenerator:
    def __init__(self):
        # Initialize the Groq LLM handler
        llm_handler = GroqModelHandler()
        self.llm = llm_handler.get_llm()
    
    def create_parser(self):
        """Create a Pydantic output parser."""
        return PydanticOutputParser(pydantic_object=ContentGenerationScript)
    
    def create_tone_parser(self):
        """Create a Pydantic output parser for tone refinement."""
        return PydanticOutputParser(pydantic_object=ToneGenerationScript)
    
    def create_script_chain(self, template, parser, input_variables):
        """Create a chain that generates script content."""
        prompt = PromptTemplate(
            template=template,
            input_variables=input_variables,
            partial_variables={"format_instructions": parser.get_format_instructions()}
        )
        
        return prompt | self.llm | parser
    
    def generate_text(self, info):
        """Genera un texto basado en la información de entrada."""
        parser = self.create_parser()
        content_chain = self.create_script_chain(
            template=GENERATE_INFO,
            parser=parser,
            input_variables=[
                "title",
                "price",
                "description",
                "available_sizes",
                "additional_info",
                "image_description",
            ],
        )

        try:
            result = content_chain.invoke(
                {
                    "title": info["title"],
                    "price": info["price"],
                    "description": info["description"],
                    "available_sizes": info["available_sizes"],
                    "additional_info": info["additional_info"],
                    "image_description": info["image_description"],
                }
            )
            
            # Verificar si el resultado es un diccionario y si tiene la clave 'content'
            if isinstance(result, dict):
                if "content" in result:
                    return result
                else:
                    # Si no tiene la clave 'content', crear una estructura adecuada
                    return {"content": str(result)}
            else:
                # Si no es un diccionario, crear una estructura adecuada
                return {"content": str(result)}
                
        except Exception as e:
            print(f"Error al generar texto: {e}")
            # En caso de error, devolver un texto predeterminado
            return {"content": f"¡Descubre el producto {info['title']} a un precio increíble de {info['price']}! {info['image_description']}"}
    
    def refine_content(self, original_content, new_target_audience, new_tone, language):
        """Refina el contenido original según la audiencia, tono e idioma especificados."""
        parser = self.create_tone_parser()
        refine_chain = self.create_script_chain(
            template=GENERATE_REFINED_INFO,
            parser=parser,
            input_variables=["previous_script", "new_target_audience", "new_tone", "language"]
        )
        
        try:
            result = refine_chain.invoke({
                "previous_script": original_content,
                "new_target_audience": new_target_audience,
                "new_tone": new_tone,
                "language": language
            })
            
            # Verificar resultado y manejar diferentes estructuras
            if isinstance(result, dict) and "refined_content" in result:
                return result
            elif isinstance(result, dict):
                return {"refined_content": str(result)}
            else:
                return {"refined_content": str(result)}
                
        except Exception as e:
            print(f"Error al refinar el contenido: {e}")
            return {"refined_content": f"Versión refinada (error): {original_content}"}
    
    def generate_content(self, metadata, new_target_audience, new_tone, language):
        """Genera y refina el contenido completo."""
        # Primero generar el contenido original
        original_content = self.generate_text(metadata)
        
        # Luego refinar el contenido según los parámetros especificados
        if isinstance(original_content, dict) and "content" in original_content:
            refined_content = self.refine_content(
                original_content["content"],
                new_target_audience,
                new_tone,
                language
            )
            return refined_content
        else:
            # Manejar el caso donde original_content no tiene la estructura esperada
            content_str = str(original_content)
            refined_content = self.refine_content(
                content_str,
                new_target_audience,
                new_tone,
                language
            )
            return refined_content