# test_scraper.py
import sys
import os
import json
import time
from dotenv import load_dotenv

# Definir rutas absolutas para asegurar que las importaciones funcionen
# Base en la ruta donde está este script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Añadir la ruta del backend al path para poder importar los módulos
BACKEND_PATH = os.path.join(CURRENT_DIR, 'backend')
sys.path.append(BACKEND_PATH)

# También añadimos el directorio src al path
SRC_PATH = os.path.join(BACKEND_PATH, 'src')
sys.path.append(SRC_PATH)

# Cargar variables de entorno
load_dotenv()

# Importar el scraper (ahora debería funcionar con las rutas correctas)
try:
    # Intento 1: Importar directamente desde backend.src
    from backend.src.scraping import FalabellaScraper
    print("Módulo importado desde backend.src.scraping")
except ImportError:
    try:
        # Intento 2: Importar solo desde src
        from src.scraping import FalabellaScraper
        print("Módulo importado desde src.scraping")
    except ImportError:
        try:
            # Intento 3: Importar directamente
            from scraping import FalabellaScraper
            print("Módulo importado desde scraping")
        except ImportError:
            print("\nERROR DE IMPORTACIÓN")
            print(f"No se puede importar FalabellaScraper. Verificando rutas:")
            print(f"- Directorio actual: {CURRENT_DIR}")
            print(f"- Path de Python: {sys.path}")
            print(f"- ¿Existe backend?: {os.path.exists(BACKEND_PATH)}")
            print(f"- ¿Existe src?: {os.path.exists(SRC_PATH)}")
            if os.path.exists(SRC_PATH):
                print(f"- Contenido de src: {os.listdir(SRC_PATH)}")
            if os.path.exists(BACKEND_PATH):
                print(f"- Contenido de backend: {os.listdir(BACKEND_PATH)}")
            
            raise ImportError("No se pudo importar FalabellaScraper. Revisa las rutas e importaciones.")

def test_scraper(url):
    """Prueba el scraper con una URL específica e imprime los resultados."""
    print(f"Probando scraper con URL: {url}")
    
    # Crear instancia del scraper
    start_time = time.time()
    print("Inicializando scraper...")
    scraper = FalabellaScraper(url)
    print(f"Scraper inicializado en {time.time() - start_time:.2f} segundos")
    
    try:
        # Obtener datos básicos para verificar que funciona
        print("\nProbando métodos individuales:")
        
        # Nombre del producto
        start_time = time.time()
        product_name = scraper.get_product_name()
        print(f"Nombre del producto: {product_name}")
        print(f"  Tiempo: {time.time() - start_time:.2f} segundos")
        
        # Precio del producto
        start_time = time.time()
        product_price = scraper.get_product_price()
        print(f"Precio del producto: {product_price}")
        print(f"  Tiempo: {time.time() - start_time:.2f} segundos")
        
        # Tallas disponibles
        start_time = time.time()
        sizes = scraper.get_available_sizes()
        print(f"Tallas disponibles: {', '.join(sizes)}")
        print(f"  Tiempo: {time.time() - start_time:.2f} segundos")
        
        # Probar obtención de imágenes
        start_time = time.time()
        images = scraper.get_image_links()
        print(f"Enlaces de imágenes encontrados: {len(images)}")
        for i, img in enumerate(images[:2]):  # Mostrar solo las primeras 2 imágenes
            print(f"  Imagen {i+1}: {img[:100]}...")
        print(f"  Tiempo: {time.time() - start_time:.2f} segundos")
        
        # Probar especificaciones
        start_time = time.time()
        specs = scraper.get_product_specifications()
        print(f"Especificaciones encontradas: {len(specs)}")
        for key, value in list(specs.items())[:3]:  # Mostrar solo las primeras 3 especificaciones
            print(f"  {key}: {value}")
        print(f"  Tiempo: {time.time() - start_time:.2f} segundos")
        
        # Probar información adicional
        start_time = time.time()
        additional_info = scraper.get_additional_info()
        print(f"Información adicional:")
        print(f"  {additional_info[:150]}..." if len(additional_info) > 150 else f"  {additional_info}")
        print(f"  Tiempo: {time.time() - start_time:.2f} segundos")
        
        # Probar descripción de imágenes (esta operación puede ser lenta)
        if images and input("¿Generar descripción de imágenes? (s/n): ").lower() == 's':
            start_time = time.time()
            image_description = scraper.get_image_description(images)
            print(f"Descripción de imágenes:")
            print(f"  {image_description[:200]}..." if len(image_description) > 200 else f"  {image_description}")
            print(f"  Tiempo: {time.time() - start_time:.2f} segundos")
        else:
            print("Descripción de imágenes omitida.")
            image_description = "Descripción omitida por el usuario"
        
        # Probar scraping completo
        print("\nProbando método de scraping completo:")
        start_time = time.time()
        data = scraper.scrape()
        print(f"Scraping completo realizado en {time.time() - start_time:.2f} segundos")
        
        # Guardar los datos en un archivo para revisión
        output_file = 'scraper_test_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"\nResultados guardados en '{output_file}'")
        print("\nResumen de los datos extraídos:")
        for key, value in data.items():
            if key == "image_links":
                print(f"  {key}: {len(value)} enlaces encontrados")
            elif key == "image_description":
                if value and len(value) > 100:
                    print(f"  {key}: {value[:100]}...")
                else:
                    print(f"  {key}: {value}")
            else:
                if isinstance(value, str) and len(value) > 50:
                    print(f"  {key}: {value[:50]}...")
                else:
                    print(f"  {key}: {value}")
        
        return data
    
    except Exception as e:
        print(f"ERROR: Se produjo una excepción durante las pruebas: {e}")
        return None
    
    finally:
        # Asegurarse de cerrar el driver de Selenium
        print("\nCerrando el scraper...")
        scraper.close()
        print("Scraper cerrado correctamente")

def main():
    """Función principal para ejecutar las pruebas."""
    print("=== PRUEBA DEL SCRAPER DE FALABELLA ===")
    print("Puede proporcionar una URL de Falabella para probar el scraper")
    
    test_url = input("Introduce la URL del producto de Falabella: ")
    
    if not test_url:
        print("Por favor, proporciona una URL válida.")
        return
    
    # Validar la URL básicamente
    if not test_url.startswith("http"):
        print("La URL debe comenzar con http:// o https://")
        return
    
    if "falabella" not in test_url.lower():
        print("ADVERTENCIA: La URL proporcionada no parece ser de Falabella.")
        if input("¿Desea continuar de todos modos? (s/n): ").lower() != 's':
            return
    
    # Ejecutar las pruebas
    test_scraper(test_url)

if __name__ == "__main__":
    main()