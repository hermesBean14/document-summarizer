from anthropic import Anthropic
from dotenv import load_dotenv

## Función que usaremos como tool
def count_words(text):

    return len(text.split())


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

n_words = count_words(response.content[0].input["text"])

##Segunda llamada a la API

tool_result = {
    "type": "tool_result",
    "tool_use_id": response.content[0].id,
    "content": str(n_words)
}

messages_final = [{

        "role": "user",
        "content": f"{prompt}"
    },
    {
        "role": "assistant",
        "content": response.content
    },
    {
        "role": "user",
        "content": [tool_result]
    }
]

response2 = client.messages.create(max_tokens=max_tokens,model=model,tools=[count_words_tool],messages=messages_final)

#print(n_words)

#print("\n")

print(response2.content[0].text)