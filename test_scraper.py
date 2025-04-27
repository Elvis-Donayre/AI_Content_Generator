# test_scraper.py
import sys
import os
import json
from dotenv import load_dotenv

# Añadir la ruta del backend al path para poder importar los módulos
sys.path.append('./backend')

# Cargar variables de entorno
load_dotenv()

# Importar el scraper
from src.scraping import FalabellaScraper

def test_scraper(url):
    """Prueba el scraper con una URL específica e imprime los resultados."""
    print(f"Probando scraper con URL: {url}")
    
    # Crear instancia del scraper
    scraper = FalabellaScraper(url)
    
    # Obtener datos básicos para verificar que funciona
    print("\nProbando métodos individuales:")
    print(f"Nombre del producto: {scraper.get_product_name()}")
    print(f"Precio del producto: {scraper.get_product_price()}")
    
    # Probar obtención de imágenes
    images = scraper.get_image_links()
    print(f"Enlaces de imágenes encontrados: {len(images)}")
    for i, img in enumerate(images[:2]):  # Mostrar solo las primeras 2 imágenes
        print(f"  Imagen {i+1}: {img[:100]}...")
    
    # Probar especificaciones
    specs = scraper.get_product_specifications()
    print(f"Especificaciones encontradas: {len(specs)}")
    for key, value in list(specs.items())[:3]:  # Mostrar solo las primeras 3 especificaciones
        print(f"  {key}: {value}")
    
    # Probar tallas disponibles
    sizes = scraper.get_available_sizes()
    print(f"Tallas disponibles: {', '.join(sizes)}")
    
    # Probar scraping completo
    print("\nProbando método de scraping completo:")
    data = scraper.scrape()
    
    # Guardar los datos en un archivo para revisión
    with open('scraper_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nResultados guardados en 'scraper_test_results.json'")
    print("\nResumen de los datos extraídos:")
    for key, value in data.items():
        if key == "image_links":
            print(f"  {key}: {len(value)} enlaces encontrados")
        elif key == "image_description":
            print(f"  {key}: {value[:100]}..." if value and len(value) > 100 else f"  {key}: {value}")
        else:
            print(f"  {key}: {value[:50]}..." if isinstance(value, str) and len(value) > 50 else f"  {key}: {value}")
    
    return data

if __name__ == "__main__":
    # URL de ejemplo de Falabella (reemplazar con una URL real)
    test_url = input("Introduce la URL del producto de Falabella: ")
    
    if not test_url:
        print("Por favor, proporciona una URL válida.")
        sys.exit(1)
    
    test_scraper(test_url)