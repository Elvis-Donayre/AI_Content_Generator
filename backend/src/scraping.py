import os
import time
import requests
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.image_describer import ImageGridDescriber


class FalabellaScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._setup_driver()
        self._load_page()
        
    def _setup_driver(self):
        """Configura el driver de Selenium con Chrome en modo headless"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        return webdriver.Chrome(options=chrome_options)
    
    def _load_page(self):
        """Carga la página y espera a que los elementos principales estén disponibles"""
        try:
            self.driver.get(self.url)
            # Esperar a que la página cargue completamente (esperar por el nombre del producto)
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-name"))
            )
            # Dar tiempo adicional para que carguen elementos dinámicos
            time.sleep(3)
        except TimeoutException:
            print("Tiempo de espera agotado al cargar la página")
        except Exception as e:
            print(f"Error al cargar la página: {e}")
    
    def __del__(self):
        """Cierra el driver cuando se destruye el objeto"""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def get_product_name(self):
        """Obtiene el nombre del producto"""
        try:
            name_element = self.driver.find_element(By.CLASS_NAME, "product-name")
            return name_element.text.strip()
        except NoSuchElementException:
            print("No se encontró el nombre del producto")
            return "Nombre no encontrado"
        except Exception as e:
            print(f"Error al obtener el nombre del producto: {e}")
            return "Error al obtener el nombre"

    def get_product_price(self):
        """Obtiene el precio del producto"""
        try:
            # Intentar con diferentes selectores para encontrar el precio
            selectors = [
                "span.copy17.primary.senary.jsx-2835692965.bold",
                "span[data-testid='product-price']",
                "span.copy10.primary.high.jsx-3548557188.normal"
            ]
            
            for selector in selectors:
                try:
                    price_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    return price_element.text.strip()
                except NoSuchElementException:
                    continue
            
            return "Precio no encontrado"
        except Exception as e:
            print(f"Error al obtener el precio del producto: {e}")
            return "Error al obtener el precio"

    def get_image_links(self):
        """Obtiene los enlaces de las imágenes del producto"""
        image_links = []
        try:
            # Buscar imágenes en el carrusel
            image_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.carousel-wrapper img")
            
            for img in image_elements:
                src = img.get_attribute("src")
                if src:
                    # Obtener versión de mayor resolución
                    high_res_url = src.replace("w=100,h=100", "w=500,h=500")
                    image_links.append(high_res_url)
            
            # Si no se encontraron imágenes, intentar con otro selector
            if not image_links:
                image_elements = self.driver.find_elements(By.CSS_SELECTOR, "img.jsx-2487856160")
                for img in image_elements:
                    src = img.get_attribute("src")
                    if src:
                        high_res_url = src.replace("w=100,h=100", "w=500,h=500")
                        image_links.append(high_res_url)
            
            return image_links
        except Exception as e:
            print(f"Error al obtener las imágenes del producto: {e}")
            return []

    def get_product_specifications(self):
        """Obtiene las especificaciones del producto"""
        specifications = {}
        try:
            # Buscar la tabla de especificaciones
            spec_rows = self.driver.find_elements(By.CSS_SELECTOR, "table.specification-table tr")
            
            for row in spec_rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        specifications[key] = value
                except Exception:
                    continue
            
            return specifications
        except Exception as e:
            print(f"Error al obtener las especificaciones del producto: {e}")
            return {}

    def get_additional_info(self):
        """Obtiene información adicional del producto"""
        try:
            # Intentar con diferentes selectores para la información adicional
            selectors = [
                "div.fb-product-information-tab__copy",
                "div.fb-product-information__product-information-tab",
                "div.product-description"
            ]
            
            for selector in selectors:
                try:
                    info_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    return info_element.text.strip()
                except NoSuchElementException:
                    continue
            
            return "Información adicional no encontrada"
        except Exception as e:
            print(f"Error al obtener la información adicional: {e}")
            return "Error al obtener información adicional"

    def get_available_sizes(self):
        """Obtiene las tallas disponibles del producto"""
        sizes = []
        try:
            # Buscar botones de tallas
            size_elements = self.driver.find_elements(By.CSS_SELECTOR, "button.size-button")
            
            for element in size_elements:
                size = element.text.strip()
                if size:
                    sizes.append(size)
            
            # Si no hay tallas, es probablemente un producto sin tallas
            return sizes if sizes else ["Talla única"]
        except Exception as e:
            print(f"Error al obtener las tallas disponibles: {e}")
            return ["Talla única"]

    def get_image_description(self, image_links):
        """Genera una descripción de las imágenes del producto"""
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
        """Extrae todos los datos relevantes del producto"""
        try:
            # Obtener todos los datos del producto
            product_name = self.get_product_name()
            product_price = self.get_product_price()
            image_links = self.get_image_links()
            specifications = self.get_product_specifications()
            additional_info = self.get_additional_info()
            available_sizes = self.get_available_sizes()
            
            # Cerrar el driver para liberar recursos
            self.driver.quit()
            
            # Obtener la descripción de las imágenes
            image_description = self.get_image_description(image_links)
            
            # Compilar todos los datos en un diccionario
            product_data = {
                "title": product_name,
                "price": product_price,
                "description": str(specifications),
                "additional_info": additional_info,
                "available_sizes": ", ".join(available_sizes),
                "image_description": image_description,
                "image_links": image_links
            }
            
            return product_data
        except Exception as e:
            print(f"Error al extraer los datos del producto: {e}")
            # Asegurar que el driver se cierre en caso de error
            if hasattr(self, 'driver'):
                self.driver.quit()
            return {}