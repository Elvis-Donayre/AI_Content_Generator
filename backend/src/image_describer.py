import os
import base64
import requests
import math
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from src.llm import GroqModelHandler

# Cargar variables del archivo .env
load_dotenv()

class ImageGridDescriber:
    def __init__(self):
        # TODO: Initialize the GroqModelHandler client and load the vision model name from environment variables
        self.client = GroqModelHandler().get_client()
        self.vision_model = os.getenv("VISION_MODEL_NAME", "llama-3.2-11b-vision-preview")

    @staticmethod
    def encode_image(image: Image.Image) -> str:
        # TODO: Encode an image to a base64 string
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def concatenate_images_square(self, urls, img_size=(200, 200)):
        # TODO: Concatenate multiple images into a square grid
        images = []
        for url in urls[:4]:  # Limitar a 4 imágenes para una cuadrícula 2x2
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                img = img.resize(img_size)
                images.append(img)
            except Exception as e:
                print(f"Error al procesar la imagen {url}: {e}")
        
        if not images:
            return None
        
        # Determinar el número de filas y columnas para la cuadrícula
        n_images = len(images)
        cols = math.ceil(math.sqrt(n_images))
        rows = math.ceil(n_images / cols)
        
        # Crear una nueva imagen para la cuadrícula
        grid_img = Image.new('RGB', (cols * img_size[0], rows * img_size[1]), color='white')
        
        # Colocar las imágenes en la cuadrícula
        for i, img in enumerate(images):
            x = (i % cols) * img_size[0]
            y = (i // cols) * img_size[1]
            grid_img.paste(img, (x, y))
        
        return grid_img

    def get_image_description(self, concatenated_image):
        # Example method for students to follow
        base64_image = self.encode_image(concatenated_image)

        completion = self.client.chat.completions.create(
            model=self.vision_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe el producto en la imagen."},
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
            max_completion_tokens=1024,
        )

        return completion.choices[0].message.content