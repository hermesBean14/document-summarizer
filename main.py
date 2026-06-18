from dotenv import load_dotenv
import os
from anthropic import Anthropic

load_dotenv()

# key = os.getenv("ANTHROPIC_API_KEY") Esto no es necesario se lee solo

client = Anthropic()

model = "claude-haiku-4-5"
max_tokens = 100
messages = [{"role": "user", "content": "Di hola en una frase."}]


response = client.messages.create(model=model,max_tokens=max_tokens,messages=messages)

print(response)

print(response.content[0].text)