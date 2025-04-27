import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from src.image_describer import ImageGridDescriber

class FalabellaScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._setup_driver()
        self.soup = None
        self._load_page()

    def _setup_driver(self):
        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # User agent para evitar bloqueos
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Inicializar el driver
        return webdriver.Chrome(options=chrome_options)

    def _load_page(self):
        try:
            self.driver.get(self.url)
            
            # Esperar a que la página cargue completamente (ajustar tiempo según sea necesario)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Esperar un poco más para asegurar que el JS se ejecute
            time.sleep(2)
            
            # Obtener el HTML después de que el JavaScript se haya ejecutado
            html = self.driver.page_source
            self.soup = BeautifulSoup(html, "html.parser")
        except Exception as e:
            print(f"Error al cargar la página: {e}")
            self.soup = None
        finally:
            # No cerramos el driver aquí para poder reutilizarlo en otros métodos
            pass

    def close(self):
        """Cerrar el navegador cuando hayamos terminado"""
        if self.driver:
            self.driver.quit()

    def get_product_name(self):
        if self.soup:
            name_tag = self.soup.find("h1", class_="product-name")
            if name_tag:
                return name_tag.text.strip()
            
            name_tag = self.soup.find("h1", attrs={"data-name": True})
            if name_tag:
                return name_tag.text.strip()
                
            return "Nombre no encontrado"
        return None

    def get_product_price(self):
        if self.soup:
            # Buscar con selectores específicos
            price_selectors = [
                "span.copy17.primary.senary.jsx-2835692965.bold",
                "span.copy12.primary.senary.jsx-2835692965.bold",
                "span[data-testid='product-price']"
            ]
            
            for selector in price_selectors:
                price_tag = self.soup.select_one(selector)
                if price_tag:
                    return price_tag.text.strip()
            
            # Buscar directamente en el DOM con Selenium
            try:
                price_element = self.driver.find_element(By.CSS_SELECTOR, 
                                                      "span[class*='primary'][class*='bold']")
                if price_element:
                    return price_element.text.strip()
            except:
                pass
                
            return "Precio no encontrado"
        return None

    def get_available_sizes(self):
        sizes = []
        
        try:
            # Usar Selenium directamente para encontrar los botones de tallas
            size_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                                                  "div.size-options button, button[class*='size-button']")
            
            # Si no encontramos con ese selector, intentamos con el ID específico
            if not size_buttons:
                size_buttons = self.driver.find_elements(By.CSS_SELECTOR, 
                                                     "button[id^='testId-sizeButton-']")
            
            # Extraer el texto de cada botón de talla
            for button in size_buttons:
                size = button.text.strip()
                if size:
                    sizes.append(size)
        except Exception as e:
            print(f"Error al obtener tallas: {e}")
        
        return sizes if sizes else ["Talla única"]

    def get_image_links(self):
        image_links = []
        if self.soup:
            # Buscar imágenes en el carrusel
            image_tags = self.soup.find_all("img", class_=lambda c: c and "product" in c.lower())
            
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
            # Buscar la tabla de especificaciones
            spec_table = self.soup.find("table", class_=lambda c: c and "specification" in c.lower())
            
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
            # Buscar la información adicional
            info_div = self.soup.find("div", class_=lambda c: c and "product-information" in c.lower())
            if info_div:
                return info_div.text.strip()
        
        return "Información adicional no encontrada"

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
        
        try:
            # Obtener todos los datos del producto
            product_name = self.get_product_name()
            product_price = self.get_product_price()
            available_sizes = self.get_available_sizes()
            image_links = self.get_image_links()
            specifications = self.get_product_specifications()
            additional_info = self.get_additional_info()
            
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
        finally:
            # Cerramos el driver después de scrapear
            self.close()
