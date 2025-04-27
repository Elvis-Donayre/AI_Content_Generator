import os
import base64
import requests
import math
import logging
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from src.llm import GroqModelHandler

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Cargar variables del archivo .env
load_dotenv()

class ImageGridDescriber:
    def __init__(self):
        # Initialize the GroqModelHandler client and load the vision model name
        self.client = GroqModelHandler().get_client()
        
        # Get the vision model from environment variables with a clear fallback
        vision_model = os.getenv("VISION_MODEL_NAME")
        if not vision_model:
            vision_model = "meta-llama/llama-4-scout-17b-16e-instruct"
            logger.warning(f"VISION_MODEL_NAME no encontrado en .env, usando modelo por defecto: {vision_model}")
        
        self.vision_model = vision_model
        logger.info(f"Inicializado ImageGridDescriber con modelo: {self.vision_model}")

    @staticmethod
    def encode_image(image: Image.Image) -> str:
        """Encode an image to a base64 string."""
        try:
            buffered = BytesIO()
            # Save as JPEG with quality parameter to manage file size
            image.save(buffered, format="JPEG", quality=85)
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_size_kb = len(encoded_image) * 3 / 4 / 1024  # Approximate size in KB
            logger.info(f"Imagen codificada, tamaño aproximado: {image_size_kb:.2f} KB")
            return encoded_image
        except Exception as e:
            logger.error(f"Error al codificar imagen: {e}")
            raise

    def concatenate_images_square(self, urls, img_size=(300, 300)):
        """Create a square grid from multiple product images."""
        if not urls:
            logger.warning("No hay URLs de imágenes para procesar")
            return None
            
        logger.info(f"Procesando {len(urls)} URLs de imágenes")
        images = []
        failed_urls = []
        
        # Try to download and process each image
        for url in urls[:4]:  # Limitar a 4 imágenes para una cuadrícula 2x2
            try:
                logger.info(f"Descargando imagen desde: {url[:60]}...")
                response = requests.get(url, timeout=10)  # Added timeout
                
                if response.status_code != 200:
                    logger.warning(f"Error al descargar imagen. Código de estado: {response.status_code}")
                    failed_urls.append(url)
                    continue
                    
                img = Image.open(BytesIO(response.content))
                
                # Ensure the image is RGB (convert if needed)
                if img.mode != 'RGB':
                    logger.info(f"Convirtiendo imagen de modo {img.mode} a RGB")
                    img = img.convert('RGB')
                    
                img = img.resize(img_size)
                images.append(img)
                logger.info("Imagen procesada correctamente")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Error en la solicitud HTTP: {e}")
                failed_urls.append(url)
            except Exception as e:
                logger.error(f"Error al procesar la imagen {url[:60]}: {e}")
                failed_urls.append(url)
        
        if failed_urls:
            logger.warning(f"No se pudieron procesar {len(failed_urls)} imágenes")
        
        if not images:
            logger.error("No se pudo procesar ninguna imagen")
            return None
        
        # Determinar el número de filas y columnas para la cuadrícula
        n_images = len(images)
        cols = math.ceil(math.sqrt(n_images))
        rows = math.ceil(n_images / cols)
        
        logger.info(f"Creando cuadrícula de {rows}x{cols} para {n_images} imágenes")
        
        # Crear una nueva imagen para la cuadrícula
        grid_width = cols * img_size[0]
        grid_height = rows * img_size[1]
        grid_img = Image.new('RGB', (grid_width, grid_height), color='white')
        
        # Colocar las imágenes en la cuadrícula
        for i, img in enumerate(images):
            x = (i % cols) * img_size[0]
            y = (i // cols) * img_size[1]
            grid_img.paste(img, (x, y))
        
        logger.info(f"Cuadrícula de imágenes creada correctamente: {grid_width}x{grid_height}")
        return grid_img

    def get_image_description(self, concatenated_image):
        """Generate AI description for a product image or image grid."""
        try:
            logger.info("Codificando imagen para enviar a la API de visión...")
            base64_image = self.encode_image(concatenated_image)
            
            logger.info("Solicitando descripción de la imagen al modelo de visión...")
            # Print model being used for debugging
            logger.info(f"Usando modelo de visión: {self.vision_model}")
            
            completion = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en describir productos a partir de imágenes. Proporciona descripciones detalladas enfocándote en el color, material, estilo, características destacadas y posibles usos del producto. Describe en tercera persona y sin mencionar la imagen en sí."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Describe este producto en detalle, mencionando sus características principales, materiales, colores y diseño."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                temperature=1,
                max_tokens=1024, 
            )

            description = completion.choices[0].message.content
            logger.info("Descripción de imagen generada exitosamente")
            return description
            
        except Exception as e:
            logger.error(f"Error al generar descripción de imagen: {e}")
            return "No se pudo generar una descripción para la imagen del producto."