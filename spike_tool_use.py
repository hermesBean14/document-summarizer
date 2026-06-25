from anthropic import Anthropic
from dotenv import load_dotenv

## Función que usaremos como tool
def count_words(text):

    return len(text.split())


## Diccionario de herramientas disponibles
available = {
    "count_words": count_words, ## Mapeo del nombre de la función en caso de usar varias tools.
}


load_dotenv()

client = Anthropic()

## El diccionario para que el LLM sepa lo que hace
count_words_tool = {

    "name": "count_words",

    "description": "Esta función recibe un texto y cuenta las palabras, luego devuelve un entero con el número de palabras. Es conveniente usar esta función cuando sea necesario contar el número de palabras que tiene un texto.",

    "input_schema": {
        "type": "object",            # siempre 'object': un conjunto de parámetros con nombre
        "properties": {
            "text": {            # el NOMBRE del parámetro
                "type": "string",
                "description": "El texto que se le pasa a la función para contar el número de palabras que tiene."
            }
        },
        "required": ["text"]     # cuáles son obligatorios
    }
}

model = "claude-haiku-4-5"
max_tokens = 1000
prompt = "¿Cuántas palabras contiene este texto?: En el verano de 1987 ocurrió un trágico accidente en las bahamas. Un coche amarillo con las puertas verdes atropelló a una pantera de camino al supermercado."

messages = [{"role": "user", "content": f"{prompt}"}]

##Primera llamada a la API

response = client.messages.create(max_tokens=max_tokens,model=model,tools=[count_words_tool],messages=messages)

## MONTAMOS EL WHILE DESPUES DE LA PRIMERA LLAMADA.

counter = 0 #Inicializamos el contador

while response.stop_reason == "tool_use" and counter < 5:

    ## Asumo un único tool_use por turno; generalizar a varios cuando toque

    block = response.content[0]
    function = available[block.name]
    result = function(**block.input)
   
    ## Usando el dict para usar la herramienta correspondiente

    tool_result = {
        "type": "tool_result",
        "tool_use_id": block.id,
        "content": str(result)
    }

    ## Actualizar os messages

    messages.append({"role": "assistant", "content": response.content})
    messages.append({  "role": "user", "content": [tool_result]}) #Habría que añadir aquí algo en content, sería un nuevo append?

    ## Llamar de nuevo a la función create

    response = client.messages.create(max_tokens=max_tokens,model=model,tools=[count_words_tool],messages=messages)

    counter += 1 #Actualizamos el counter al final de cada iteración


if response.stop_reason == "tool_use":

    print("Incomplete, not finished, reached iteration limit")

else:

    print(response.content[0].text)


