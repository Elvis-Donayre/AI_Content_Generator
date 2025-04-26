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