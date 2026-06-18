from dotenv import load_dotenv
from anthropic import Anthropic
import sys

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
prompt = "Resume el siguiente texto en castellano, recogiendo sus ideas principales y puntos clave en un párrafo conciso (4-6 frases). Texto:"

messages = [{"role": "user", "content": f"{prompt}\n\n{contenido}"}]

response = client.messages.create(model=model,max_tokens=max_tokens,messages=messages)

print(response)

print(response.content[0].text)