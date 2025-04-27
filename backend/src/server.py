from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import logging
import traceback
import time
from src.content_generator import ContentGenerator
from models.content_generation_models import ContentGeneration
from src.scraping import FalabellaScraper

# Configurar logs con formato mejorado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Text Generation with LLMs",
    description="""Create high-quality text content using advanced Large Language Models (LLMs).  
                  Generate textual descriptions, narratives, and insights from images and text inputs.  
                  Access the Streamlit interface at port 8501 for an interactive experience.""",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    """Endpoint to check the health of the API"""
    return {"status": "ok"}


@app.post("/content_generator")
def generate_content(request: ContentGeneration):
    """Generate content based on metadata scraped from the given URL"""
    start_time = time.time()
    logger.info(f"Iniciando generación de contenido para URL: {request.url}")
    logger.info(f"Parámetros: Audiencia={request.new_target_audience}, Tono={request.new_tone}, Idioma={request.language}")
    
    try:
        # Scrape metadata using FalabellaScraper
        logger.info(f"Iniciando web scraping de la URL: {request.url}")
        scraper = FalabellaScraper(request.url)
        metadata = scraper.scrape()
        scrape_time = time.time()
        logger.info(f"Web scraping completado en {scrape_time - start_time:.2f} segundos")

        # Validate metadata
        if not metadata or not isinstance(metadata, dict):
            logger.error("La metadata obtenida no es válida")
            raise ValueError("No se pudo extraer metadata válida del producto.")

        # Log metadata keys for debugging (without the full content to keep logs clean)
        logger.info(f"Metadata obtenida con claves: {list(metadata.keys())}")
        
        # Generate content using the ContentGenerator
        logger.info("Iniciando generación de contenido con LLM")
        content_generator = ContentGenerator()
        content = content_generator.generate_content(
            metadata, 
            request.new_target_audience, 
            request.new_tone, 
            request.language
        )
        generation_time = time.time()
        logger.info(f"Generación de contenido completada en {generation_time - scrape_time:.2f} segundos")

        # Log successful generation
        total_time = time.time() - start_time
        logger.info(f"Proceso completo finalizado con éxito en {total_time:.2f} segundos")
        return {"generated_content": content}

    except ValueError as ve:
        logger.error(f"Error de validación: {ve}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=400, detail={"error": "Datos inválidos", "message": str(ve)}
        )

    except Exception as e:
        logger.error(f"Error interno: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500, detail={"error": "Error interno", "message": str(e)}
        )