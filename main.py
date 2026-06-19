from dotenv import load_dotenv
from anthropic import Anthropic, APIError
import json
import argparse
import sys
from pypdf import PdfReader
from pypdf.errors import PdfReadError

#sys.argv:  Son los argumentos al lanzar el código -> Lo hacemos con argparse, es mejor.

parser = argparse.ArgumentParser(description='Recibe un texto y devuelve un resumen estructurado llamando a un LLM por API')

parser.add_argument("archivo", help='La ruta al archivo que se desea resumir')

args = parser.parse_args()

#Esto solamente es funcional para .pdf y .txt

text_total = ""

if args.archivo.endswith(".pdf"):

    try:
        reader = PdfReader(args.archivo)

        for page in reader.pages:
            text_total += page.extract_text()

    except FileNotFoundError:
        print("No se ha podido encontrar el archivo")
        sys.exit(1)

    except PdfReadError as e:
        print(f"Fallo en la lectura del PDF: {e}")
        sys.exit(1)


else:

    try:
        with open(args.archivo, encoding="utf-8") as f:
            text_total = f.read()
    except FileNotFoundError:
        print("No se ha podido encontrar el archivo")
        sys.exit(1)
# aquí fuera del bloque, el archivo ya está cerrado


# LLAMADA A API CON HOLA MUNDO:

load_dotenv()

# key = os.getenv("ANTHROPIC_API_KEY") Esto no es necesario se lee solo

client = Anthropic()

model = "claude-haiku-4-5"
max_tokens = 1000
prompt = "Resume el siguiente texto y devuelve tu respuesta únicamente como un objeto JSON con estas tres claves exactas: 'titulo' (un string), 'puntos_clave' (una lista de 5-6 strings con las ideas principales) y 'conclusion' (un string). No incluyas ningún texto fuera del JSON, ni explicaciones, ni vallas de markdown. Texto:"

messages = [{"role": "user", "content": f"{prompt}\n\n{text_total}"}]

try:
    response = client.messages.create(model=model,max_tokens=max_tokens,messages=messages)
except APIError as e:
    print(f"Fallo en la llamada a la API: {e}")
    sys.exit(1)

# Convertimos a texto la respuesta:

text = response.content[0].text

# Primero hay que parsear el JSON
try:
    left_index = text.find("{")
    right_index = text.rfind("}")
    json_text = text[left_index:right_index+1]
    summary = json.loads(json_text)

except json.JSONDecodeError as e: 
    print(f"Error en el parseo a JSON: {e}")
    sys.exit(1)

# Los campos demandados son "titulo" "puntos_clave" "conclusion"

print(summary["titulo"])
print("\n")

for idx,punto in enumerate(summary["puntos_clave"],start=1):
    print(f"{idx}. {punto}.\n")


print(summary["conclusion"])

#print(response.content[0].text)