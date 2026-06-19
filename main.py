from dotenv import load_dotenv
from anthropic import Anthropic
import sys
import json

#sys.argv:  Son los argumentos al lanzar el código

with open(sys.argv[1], encoding="utf-8") as f:
    contenido = f.read()
# aquí fuera del bloque, el archivo ya está cerrado
#print(len(contenido))


# LLAMADA A API CON HOLA MUNDO:

load_dotenv()

# key = os.getenv("ANTHROPIC_API_KEY") Esto no es necesario se lee solo

client = Anthropic()

model = "claude-haiku-4-5"
max_tokens = 1000
prompt = "Resume el siguiente texto y devuelve tu respuesta únicamente como un objeto JSON con estas tres claves exactas: 'titulo' (un string), 'puntos_clave' (una lista de 5-6 strings con las ideas principales) y 'conclusion' (un string). No incluyas ningún texto fuera del JSON, ni explicaciones, ni vallas de markdown. Texto:"

messages = [{"role": "user", "content": f"{prompt}\n\n{contenido}"}]

response = client.messages.create(model=model,max_tokens=max_tokens,messages=messages)

# Convertimos a texto la respuesta:

text = response.content[0].text

# Primero hay que parsear el JSON

left_index = text.find("{")
right_index = text.rfind("}")

json_text = text[left_index:right_index+1]

resumen = json.loads(json_text)

# Los campos demandados son "titulo" "puntos_clave" "conclusion"

print(resumen["titulo"])
print("\n")

for idx,punto in enumerate(resumen["puntos_clave"],start=1):
    print(f"{idx}. {punto}.\n")


print(resumen["conclusion"])

#print(response.content[0].text)