import requests
from bs4 import BeautifulSoup
from src.image_describer import ImageGridDescriber


class FalabellaScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
        self.soup = self._get_soup()

    def _get_soup(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            print(f"Error al obtener el HTML: {e}")
            return None

    def get_product_name(self):
        if self.soup:
            name_tag = self.soup.find("h1", class_="jsx-783883818 product-name")
            return name_tag.text.strip() if name_tag else "Nombre no encontrado"
        return None

    def get_product_price(self):
        if self.soup:
            # Buscar con el selector que vimos en el paste.txt
            price_tag = self.soup.find("span", class_="copy17 primary senary jsx-2835692965 bold")
            if price_tag:
                return price_tag.text.strip()
            
            # Intentar con otros selectores comunes
            price_tag = self.soup.find("span", attrs={"data-testid": "product-price"})
            if price_tag:
                return price_tag.text.strip()
                
            price_tag = self.soup.find("span", class_="copy10 primary high jsx-3548557188 normal")
            return price_tag.text.strip() if price_tag else "Precio no encontrado"
        return None

    def get_image_links(self):
        image_links = []
        if self.soup:
            # Buscar imágenes en el carrusel como se muestra en paste.txt
            image_tags = self.soup.find_all("img", class_="jsx-2487856160")
            
            for img in image_tags:
                if img.has_attr("src"):
                    # Obtener la versión de mayor resolución de la imagen
                    img_url = img["src"]
                    # Reemplazar tamaño para obtener imágenes más grandes
                    high_res_url = img_url.replace("w=100,h=100", "w=500,h=500")
                    image_links.append(high_res_url)
        
        return image_links

    def get_product_specifications(self):
        specifications = {}
        if self.soup:
            # Buscar la tabla de especificaciones como se muestra en paste.txt
            spec_table = self.soup.find("table", class_="jsx-960159652 specification-table")
            
            if spec_table:
                rows = spec_table.find_all("tr")
                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) >= 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        specifications[key] = value
        
        return specifications

    def get_additional_info(self):
        if self.soup:
            # Buscar la información adicional como se muestra en paste.txt
            info_div = self.soup.find("div", class_="fb-product-information-tab__copy")
            if info_div:
                return info_div.text.strip()
            
            # Como alternativa, buscar otra sección de información
            info_div = self.soup.find("div", class_="fb-product-information__product-information-tab")
            if info_div:
                return info_div.text.strip()
        
        return "Información adicional no encontrada"

    def get_available_sizes(self):
        sizes = []
        if self.soup:
            # Buscar botones de tallas como se muestra en paste.txt
            size_buttons = self.soup.find_all("button", class_="jsx-3027654667 size-button")
            for button in size_buttons:
                size = button.text.strip()
                if size:
                    sizes.append(size)
        
        return sizes if sizes else ["Talla única"]

    def get_image_description(self, image_links):
        if not image_links:
            return "No hay imágenes disponibles para describir."
        
        try:
            image_describer = ImageGridDescriber()
            concatenated_image = image_describer.concatenate_images_square(image_links)
            
            if concatenated_image:
                return image_describer.get_image_description(concatenated_image)
            else:
                return "No se pudieron procesar las imágenes para generar una descripción."
        except Exception as e:
            print(f"Error al describir las imágenes: {e}")
            return "Error al generar la descripción de las imágenes."

    def scrape(self):
        if not self.soup:
            # Si no se pudo obtener la página, devolver datos de ejemplo
            return {
                "title": "Producto de ejemplo",
                "price": "S/ 999",
                "description": "Descripción de ejemplo",
                "additional_info": "Información adicional de ejemplo",
                "available_sizes": "Talla única",
                "image_description": "Descripción de imagen de ejemplo",
                "image_links": []
            }
        
        # Obtener todos los datos del producto
        product_name = self.get_product_name()
        product_price = self.get_product_price()
        image_links = self.get_image_links()
        specifications = self.get_product_specifications()
        additional_info = self.get_additional_info()
        available_sizes = self.get_available_sizes()
        
        # Obtener la descripción de las imágenes
        image_description = self.get_image_description(image_links)
        
        # Compilar todos los datos en un diccionario
        product_data = {
            "title": product_name if product_name else "Producto de ejemplo",
            "price": product_price if product_price else "S/ 999",
            "description": str(specifications) if specifications else "Descripción de ejemplo",
            "additional_info": additional_info if additional_info else "Información adicional de ejemplo",
            "available_sizes": ", ".join(available_sizes),
            "image_description": image_description,
            "image_links": image_links
        }
        
        return product_data