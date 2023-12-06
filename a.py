import spacy

# Cargar el modelo de Spacy (asegúrate de que sea el modelo actualizado con tus ajustes)
model_path = "C:/Users/Desarrollo2/Pictures/convertidor/Motos/Nueva carpeta/api_new_invoice/modelo_entrenado"
nlp = spacy.load(model_path)

def generar_respuesta_modelo_autonoma(nlp, texto_saludo):
    # Analizar el texto del saludo
    doc = nlp(texto_saludo)

    # Obtener información relevante del análisis
    entidades = [(ent.text, ent.label_) for ent in doc.ents]
    print(entidades)
    if entidades:
        respuesta = f"¡Hola! ¿En qué puedo ayudarte? Entidades detectadas: {entidades}"
    else:
        respuesta = "¡Hola! ¿En qué puedo ayudarte?"

    return respuesta

if __name__ == "__main__":
    # Ejemplo de prueba con saludo
    texto_saludo = "Hola, ¿cómo estás?"

    # Generar respuesta autónoma utilizando el modelo de Spacy
    respuesta_autonoma = generar_respuesta_modelo_autonoma(nlp, texto_saludo)
    print("Respuesta autónoma basada en modelo:", respuesta_autonoma)
