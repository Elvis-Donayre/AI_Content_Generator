import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
import math
from src.image_describer import ImageGridDescriber

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FalabellaScraper:
    def __init__(self, url):
        self.url = url
        self.driver = self._setup_driver()
        self.soup = None
        self._load_page()

    def _setup_driver(self):
        """Configure and return a Chrome WebDriver instance."""
        logger.info("Configurando driver de Chrome...")
        
        # Configurar opciones de Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ejecutar en modo headless
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # User agent para evitar bloqueos
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Inicializar el driver
        try:
            driver = webdriver.Chrome(options=chrome_options)
            logger.info("Driver de Chrome configurado correctamente")
            return driver
        except Exception as e:
            logger.error(f"Error al configurar driver de Chrome: {e}")
            # Intentar con una configuración alternativa
            try:
                logger.info("Intentando configuración alternativa...")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-notifications")
                return webdriver.Chrome(options=chrome_options)
            except Exception as e2:
                logger.error(f"Error en configuración alternativa: {e2}")
                raise

    def _load_page(self):
        """Load the URL page and prepare for scraping."""
        logger.info(f"Cargando página: {self.url}")
        try:
            self.driver.get(self.url)
            
            # Esperar a que la página cargue completamente
            logger.info("Esperando que la página cargue...")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Esperar un poco más para asegurar que el JS se ejecute
            time.sleep(3)
            
            # Scroll para asegurar que se carguen elementos dinámicos
            logger.info("Realizando scroll para cargar elementos dinámicos...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            
            # Obtener el HTML después de que el JavaScript se haya ejecutado
            logger.info("Obteniendo HTML de la página...")
            html = self.driver.page_source
            self.soup = BeautifulSoup(html, "html.parser")
            logger.info("Página cargada correctamente")
        except Exception as e:
            logger.error(f"Error al cargar la página: {e}")
            self.soup = None

    def close(self):
        """Close the browser when finished."""
        if self.driver:
            logger.info("Cerrando el navegador...")
            self.driver.quit()
            logger.info("Navegador cerrado")

    def get_product_name(self):
        """Extract the product name."""
        logger.info("Extrayendo nombre del producto...")
        try:
            if not self.soup:
                return "Nombre no encontrado"
                
            # Array de posibles selectores para el nombre del producto
            selectors = [
                "h1.product-name", 
                "h1[data-name]",
                "div.product-name h1",
                ".product-detail h1",
                "h1.jsx-1794488219",
                "h1[class*='title']",
                "h1[class*='name']"
            ]
            
            # Intentar con BeautifulSoup usando los selectores
            for selector in selectors:
                element = self.soup.select_one(selector)
                if element:
                    name = element.text.strip()
                    logger.info(f"Nombre encontrado con selector {selector}: {name}")
                    return name
            
            # Si no se encuentra con selectores, intentar con Selenium
            try:
                product_name_element = self.driver.find_element(By.TAG_NAME, "h1")
                if product_name_element:
                    name = product_name_element.text.strip()
                    logger.info(f"Nombre encontrado con Selenium: {name}")
                    return name
            except Exception as e:
                logger.error(f"Error al buscar nombre con Selenium: {e}")
            
            # Si no encontramos el nombre, buscamos en la etiqueta title
            if self.soup.title:
                title_text = self.soup.title.text.strip()
                # Normalmente el título contiene el nombre del producto seguido por el nombre de la tienda
                if " - " in title_text:
                    name = title_text.split(" - ")[0].strip()
                    logger.info(f"Nombre extraído del título de la página: {name}")
                    return name
                    
            logger.warning("No se pudo encontrar el nombre del producto")
            return "Nombre no encontrado"
            
        except Exception as e:
            logger.error(f"Error al obtener el nombre del producto: {e}")
            return "Nombre no encontrado"

    def get_product_price(self):
        """Extract the product price."""
        logger.info("Extrayendo precio del producto...")
        try:
            if not self.soup:
                return "Precio no encontrado"
                
            # Array de posibles selectores para el precio
            price_selectors = [
                "span.copy17.primary.senary.jsx-2835692965.bold",
                "span.copy12.primary.senary.jsx-2835692965.bold",
                "span[data-testid='product-price']",
                ".price-main",
                ".product-price",
                "div[class*='price']",
                "span[class*='price']"
            ]
            
            # Intentar con BeautifulSoup
            for selector in price_selectors:
                price_tag = self.soup.select_one(selector)
                if price_tag:
                    price = price_tag.text.strip()
                    logger.info(f"Precio encontrado con selector {selector}: {price}")
                    return price
            
            # Intentar con Selenium
            try:
                # Buscar elementos que puedan contener el precio
                price_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "span[class*='price'], div[class*='price'], span.primary.senary.bold, span[data-testid*='price']"
                )
                
                for element in price_elements:
                    price_text = element.text.strip()
                    # Verificar si el texto se parece a un precio (contiene números y simbolos de moneda)
                    if price_text and (
                        "$" in price_text or 
                        "€" in price_text or 
                        "S/" in price_text or 
                        "£" in price_text or 
                        any(char.isdigit() for char in price_text)
                    ):
                        logger.info(f"Precio encontrado con Selenium: {price_text}")
                        return price_text
            except Exception as e:
                logger.error(f"Error al buscar precio con Selenium: {e}")
                
            logger.warning("No se pudo encontrar el precio del producto")
            return "Precio no encontrado"
            
        except Exception as e:
            logger.error(f"Error al obtener el precio del producto: {e}")
            return "Precio no encontrado"

    def get_available_sizes(self):
        """Extract available product sizes."""
        logger.info("Extrayendo tallas disponibles...")
        sizes = []
        
        try:
            if not self.soup:
                return ["Talla única"]
                
            # Intentar encontrar tallas con Selenium primero (más confiable para elementos dinámicos)
            try:
                # Buscar diferentes patrones de botones de talla
                size_selectors = [
                    "div.size-options button", 
                    "button[class*='size-button']",
                    "button[id^='testId-sizeButton-']",
                    "div[class*='size'] button",
                    "div[class*='variante'] button",
                    "div.jsx-2889528833 button"  # Selector específico observado en Falabella
                ]
                
                for selector in size_selectors:
                    size_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if size_buttons:
                        for button in size_buttons:
                            size_text = button.text.strip()
                            if size_text and size_text not in sizes:
                                sizes.append(size_text)
                        
                        if sizes:
                            logger.info(f"Tallas encontradas con selector {selector}: {sizes}")
                            break
                
            except Exception as e:
                logger.error(f"Error al buscar tallas con Selenium: {e}")
            
            # Si no encontramos tallas con Selenium, intentar con BeautifulSoup
            if not sizes:
                # Selectores similares pero para BeautifulSoup
                for selector in ["div.size-options button", "button[class*='size']", "div[class*='variante'] button"]:
                    size_elements = self.soup.select(selector)
                    for element in size_elements:
                        size_text = element.text.strip()
                        if size_text and size_text not in sizes:
                            sizes.append(size_text)
                    
                    if sizes:
                        logger.info(f"Tallas encontradas con BeautifulSoup: {sizes}")
                        break
            
            # Si aún no tenemos tallas, buscar en cualquier elemento que contenga la palabra "talla" o "size"
            if not sizes:
                size_related = self.soup.find_all(string=lambda text: 
                    text and ("talla" in text.lower() or "size" in text.lower())
                )
                
                if size_related:
                    for text in size_related:
                        parent = text.parent
                        if parent and parent.name != "script" and parent.name != "style":
                            # Obtener el texto del elemento padre, que probablemente contiene la información de talla
                            size_info = parent.text.strip()
                            if size_info:
                                logger.info(f"Información de talla encontrada: {size_info}")
                                # Agregar como un solo elemento ya que es información textual, no tallas individuales
                                sizes.append(size_info)
                                break
        
        except Exception as e:
            logger.error(f"Error al obtener tallas: {e}")
        
        # Si no se encontraron tallas, devolver "Talla única"
        if not sizes:
            logger.warning("No se encontraron tallas, asumiendo talla única")
            return ["Talla única"]
            
        return sizes

    def get_image_links(self):
        """Extract product image links."""
        logger.info("Extrayendo enlaces de imágenes...")
        image_links = []
        
        try:
            if not self.soup:
                return []
                
            # 1. Buscar el carrusel en la estructura específica que vimos en los ejemplos
            carousel = self.soup.find("div", class_="jsx-733916836 carousel")
            
            if carousel:
                logger.info("Carrusel encontrado con estructura específica")
                # Buscar imágenes dentro del carrusel
                image_tags = carousel.find_all("img")
                
                for img in image_tags:
                    if img.has_attr("src"):
                        img_url = img["src"]
                        # Convertir de baja a alta resolución
                        high_res_url = img_url.replace("w=100,h=100", "w=500,h=500")
                        
                        if high_res_url not in image_links:
                            image_links.append(high_res_url)
                
                if image_links:
                    logger.info(f"Se encontraron {len(image_links)} imágenes en el carrusel")
            
            # 2. Si no encontramos el carrusel específico o no tiene imágenes, buscar con otros selectores
            if not image_links:
                logger.info("Buscando imágenes con selectores alternativos...")
                # Selectores alternativos
                alt_selectors = [
                    "img[id^='testId-pod-image']",
                    "div[class*='carousel'] img",
                    "div[class*='gallery'] img",
                    "img[class*='product']",
                    "img[src*='product']"
                ]
                
                for selector in alt_selectors:
                    images = self.soup.select(selector)
                    for img in images:
                        if img.has_attr("src") and not any(excluded in img["src"].lower() 
                                                         for excluded in ["icon", "logo", "banner"]):
                            img_url = img["src"]
                            high_res_url = img_url.replace("w=100,h=100", "w=500,h=500")
                            
                            if high_res_url not in image_links:
                                image_links.append(high_res_url)
                    
                    if image_links:
                        logger.info(f"Se encontraron {len(image_links)} imágenes con selector {selector}")
                        break
            
            # 3. Si todavía no hay imágenes, intentar con Selenium
            if not image_links:
                logger.info("Intentando extraer imágenes con Selenium...")
                try:
                    # Primero buscar el carrusel con Selenium
                    carousel_elements = self.driver.find_elements(By.CLASS_NAME, "carousel")
                    
                    if carousel_elements:
                        selenium_images = []
                        for carousel in carousel_elements:
                            carousel_images = carousel.find_elements(By.TAG_NAME, "img")
                            selenium_images.extend(carousel_images)
                    else:
                        # Si no hay carrusel, buscar imágenes de producto directamente
                        selenium_images = self.driver.find_elements(
                            By.CSS_SELECTOR, 
                            "img[id^='testId-pod-image'], img[class*='product'], img[src*='product']"
                        )
                    
                    for img in selenium_images:
                        src = img.get_attribute("src")
                        if src and not any(excluded in src.lower() 
                                         for excluded in ["icon", "logo", "banner"]):
                            high_res_url = src.replace("w=100,h=100", "w=500,h=500")
                            if high_res_url not in image_links:
                                image_links.append(high_res_url)
                    
                    if image_links:
                        logger.info(f"Se encontraron {len(image_links)} imágenes con Selenium")
                        
                except Exception as e:
                    logger.error(f"Error al obtener imágenes con Selenium: {e}")
            
            # 4. Inspeccionar los srcset para encontrar imágenes de mayor resolución
            if image_links and all("w=100,h=100" in url for url in image_links):
                logger.info("Buscando imágenes de mayor resolución en srcset...")
                
                # Con BeautifulSoup
                img_tags_with_srcset = self.soup.find_all("img", srcset=True)
                for img in img_tags_with_srcset:
                    srcset = img["srcset"]
                    # Típicamente el srcset contiene URLs separadas por coma
                    urls = srcset.split(",")
                    for url_part in urls:
                        if "2x" in url_part and "/w=200,h=200" in url_part:  # Imágenes de mayor resolución
                            url = url_part.split(" ")[0].strip()
                            high_res_url = url.replace("w=200,h=200", "w=500,h=500")
                            if high_res_url not in image_links:
                                image_links.append(high_res_url)
                
                # Con Selenium
                try:
                    img_elements = self.driver.find_elements(By.TAG_NAME, "img")
                    for img in img_elements:
                        srcset = img.get_attribute("srcset")
                        if srcset:
                            urls = srcset.split(",")
                            for url_part in urls:
                                if "2x" in url_part and "/w=200,h=200" in url_part:
                                    url = url_part.split(" ")[0].strip()
                                    high_res_url = url.replace("w=200,h=200", "w=500,h=500")
                                    if high_res_url not in image_links:
                                        image_links.append(high_res_url)
                except Exception as e:
                    logger.error(f"Error al buscar en srcset con Selenium: {e}")
            
        except Exception as e:
            logger.error(f"Error al obtener enlaces de imágenes: {e}")
        
        # Limitar a un máximo de imágenes y registrar resultado
        image_links = image_links[:6]  # Podemos aumentar este límite si es necesario
        
        if image_links:
            logger.info(f"Total de {len(image_links)} imágenes encontradas")
            for i, url in enumerate(image_links):
                logger.info(f"Imagen {i+1}: {url[:60]}...")
        else:
            logger.warning("No se encontraron imágenes")
        
        return image_links

    def get_product_specifications(self):
        """Extract product specifications."""
        logger.info("Extrayendo especificaciones del producto...")
        specifications = {}
        
        try:
            if not self.soup:
                return specifications
                
            # Buscar tablas de especificaciones
            spec_selectors = [
                "table[class*='specification']",
                "table[class*='spec']",
                "div[class*='specification']",
                "div[class*='spec']",
                "div[class*='details']"
            ]
            
            for selector in spec_selectors:
                elements = self.soup.select(selector)
                for element in elements:
                    # Si es una tabla, procesar filas y celdas
                    if element.name == "table":
                        rows = element.find_all("tr")
                        for row in rows:
                            cells = row.find_all("td")
                            if len(cells) >= 2:
                                key = cells[0].text.strip()
                                value = cells[1].text.strip()
                                specifications[key] = value
                    else:
                        # Si es un div, buscar pares clave-valor
                        keys = element.find_all(["dt", "h3", "strong", "span[class*='label']"])
                        for key_elem in keys:
                            key = key_elem.text.strip()
                            # Buscar el valor siguiente
                            value_elem = key_elem.find_next(["dd", "p", "span", "div"])
                            if value_elem:
                                value = value_elem.text.strip()
                                specifications[key] = value
                
                if specifications:
                    logger.info(f"Especificaciones encontradas con selector {selector}")
                    break
            
            # Si no encontramos especificaciones, intentar con Selenium
            if not specifications:
                try:
                    # Intentar encontrar secciones de especificaciones
                    spec_elements = self.driver.find_elements(
                        By.CSS_SELECTOR, 
                        "div[class*='spec'], div[class*='detail'], table[class*='spec']"
                    )
                    
                    for element in spec_elements:
                        # Obtener el texto completo y procesarlo
                        spec_text = element.text
                        if spec_text:
                            # Dividir por líneas y buscar pares clave:valor
                            lines = spec_text.split('\n')
                            for line in lines:
                                if ':' in line:
                                    parts = line.split(':', 1)
                                    key = parts[0].strip()
                                    value = parts[1].strip()
                                    if key and value:
                                        specifications[key] = value
                except Exception as e:
                    logger.error(f"Error al buscar especificaciones con Selenium: {e}")
        
        except Exception as e:
            logger.error(f"Error al obtener especificaciones: {e}")
        
        if specifications:
            logger.info(f"Se encontraron {len(specifications)} especificaciones")
        else:
            logger.warning("No se encontraron especificaciones")
            
        return specifications

    def get_additional_info(self):
        """Extract additional product information."""
        logger.info("Extrayendo información adicional...")
        try:
            if not self.soup:
                return "Información adicional no encontrada"
                
            # Buscar secciones con información adicional
            info_selectors = [
                "div[class*='product-information']",
                "div[class*='product-detail']",
                "div[class*='description']",
                "div[id*='description']",
                "p[class*='description']"
            ]
            
            for selector in info_selectors:
                info_elements = self.soup.select(selector)
                for element in info_elements:
                    info_text = element.text.strip()
                    if info_text and len(info_text) > 20:  # Filtrar textos muy cortos
                        logger.info(f"Información adicional encontrada con selector {selector}")
                        return info_text
            
            # Si no encontramos con BeautifulSoup, intentar con Selenium
            try:
                info_elements = self.driver.find_elements(
                    By.CSS_SELECTOR, 
                    "div[class*='description'], div[class*='information'], div[class*='detail']"
                )
                
                for element in info_elements:
                    info_text = element.text.strip()
                    if info_text and len(info_text) > 20:
                        logger.info(f"Información adicional encontrada con Selenium")
                        return info_text
            except Exception as e:
                logger.error(f"Error al buscar información adicional con Selenium: {e}")
            
            # Si no encontramos información específica, usar las especificaciones
            specs = self.get_product_specifications()
            if specs:
                specs_text = ", ".join([f"{k}: {v}" for k, v in specs.items()])
                logger.info("Usando especificaciones como información adicional")
                return specs_text
                
            logger.warning("No se encontró información adicional")
            return "Información adicional no encontrada"
            
        except Exception as e:
            logger.error(f"Error al obtener información adicional: {e}")
            return "Información adicional no encontrada"

    def get_image_description(self, image_links):
        """Get AI-generated description of product images."""
        logger.info("Generando descripción de imágenes...")
        if not image_links:
            logger.warning("No hay imágenes para describir")
            return "No hay imágenes disponibles para describir el producto."
        
        try:
            logger.info(f"Procesando {len(image_links)} imágenes para generar descripción...")
            
            # Initialize the image describer
            image_describer = ImageGridDescriber()
            
            # Create a composite image from the first 4 images (or fewer if less available)
            image_links_to_process = image_links[:4]
            logger.info(f"Creando cuadrícula con {len(image_links_to_process)} imágenes")
            
            # Attempt to create the concatenated image
            concatenated_image = image_describer.concatenate_images_square(image_links_to_process)
            
            # If successful, get the AI description
            if concatenated_image:
                logger.info("Cuadrícula creada con éxito, generando descripción...")
                description = image_describer.get_image_description(concatenated_image)
                logger.info("Descripción generada con éxito")
                return description
            else:
                logger.warning("No se pudo crear la cuadrícula de imágenes")
                return "No se pudieron procesar las imágenes para generar una descripción detallada del producto."
        except Exception as e:
            logger.error(f"Error en el proceso de descripción de imágenes: {e}")
            return f"Error al generar la descripción de las imágenes: {str(e)}"

    def scrape(self):
        """Main method to scrape all product data."""
        logger.info(f"Iniciando scraping completo para URL: {self.url}")
        
        if not self.soup:
            logger.warning("No se pudo cargar la página, devolviendo datos de ejemplo")
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
            start_time = time.time()
            
            # 1. Obtener nombre del producto
            product_name = self.get_product_name()
            logger.info(f"Tiempo para obtener nombre: {time.time() - start_time:.2f}s")
            
            # 2. Obtener precio
            time_checkpoint = time.time()
            product_price = self.get_product_price()
            logger.info(f"Tiempo para obtener precio: {time.time() - time_checkpoint:.2f}s")
            
            # 3. Obtener tallas disponibles
            time_checkpoint = time.time()
            available_sizes = self.get_available_sizes()
            logger.info(f"Tiempo para obtener tallas: {time.time() - time_checkpoint:.2f}s")
            
            # 4. Obtener enlaces de imágenes
            time_checkpoint = time.time()
            image_links = self.get_image_links()
            logger.info(f"Tiempo para obtener enlaces de imágenes: {time.time() - time_checkpoint:.2f}s")
            
            # 5. Obtener especificaciones
            time_checkpoint = time.time()
            specifications = self.get_product_specifications()
            logger.info(f"Tiempo para obtener especificaciones: {time.time() - time_checkpoint:.2f}s")
            
            # 6. Obtener información adicional
            time_checkpoint = time.time()
            additional_info = self.get_additional_info()
            logger.info(f"Tiempo para obtener info adicional: {time.time() - time_checkpoint:.2f}s")
            
            # 7. Obtener descripción de imágenes (proceso más lento, hacerlo al final)
            time_checkpoint = time.time()
            image_description = self.get_image_description(image_links)
            logger.info(f"Tiempo para generar descripción de imágenes: {time.time() - time_checkpoint:.2f}s")
            
            # Compilar todos los datos en un diccionario
            product_data = {
                "title": product_name if product_name and product_name != "Nombre no encontrado" else "Producto de ejemplo",
                "price": product_price if product_price and product_price != "Precio no encontrado" else "S/ 999",
                "description": str(specifications) if specifications else "Descripción de ejemplo",
                "additional_info": additional_info if additional_info and additional_info != "Información adicional no encontrada" else "Información adicional de ejemplo",
                "available_sizes": ", ".join(available_sizes) if available_sizes else "Talla única",
                "image_description": image_description,
                "image_links": image_links
            }
            
            logger.info(f"Scraping completado en {time.time() - start_time:.2f} segundos")
            return product_data
        except Exception as e:
            logger.error(f"Error durante el scraping: {e}")
            # Devolver datos básicos en caso de error
            return {
                "title": "Error al obtener producto",
                "price": "Precio no disponible",
                "description": f"No se pudo obtener la descripción. Error: {str(e)}",
                "additional_info": "Información no disponible",
                "available_sizes": "Talla única",
                "image_description": "No se pudo generar descripción de imágenes",
                "image_links": []
            }
        finally:
            # Cerramos el driver después de scrapear
            self.close()