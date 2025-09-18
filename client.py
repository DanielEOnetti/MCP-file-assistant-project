# client.py
import os
import requests
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- Configuración y Conexión con Gemini ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: No se encontró la clave GEMINI_API_KEY en el archivo .env.")
    exit()

genai.configure(api_key=API_KEY)
# Confirma la versión para la depuración
print(f"Versión de google-generativeai: {genai.__version__}")

# URL de tu servidor Django
SERVER_URL = "http://127.0.0.1:8000/api"

# --- Funciones Auxiliares ---
def get_tools_manifest():
    """Obtiene el manifiesto de herramientas de nuestro servidor MCP."""
    try:
        response = requests.get(f"{SERVER_URL}/tools/manifest")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el manifiesto: {e}")
        return None

def execute_tool_call(tool_name, parameters):
    """Ejecuta una herramienta en el servidor MCP y devuelve la respuesta."""
    try:
        # Si la herramienta es 'list_files', usa GET.
        if tool_name == 'list_files':
            response = requests.get(f"{SERVER_URL}/tools/{tool_name}")
        # Para el resto de herramientas, usa POST.
        else:
            response = requests.post(f"{SERVER_URL}/tools/{tool_name}", json=parameters)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al ejecutar la herramienta '{tool_name}': {e}")
        return {"error": str(e)}

# --- Lógica principal del agente MCP ---
def chat_with_agent():
    """Bucle principal de la conversación con el agente."""
    tools_manifest = get_tools_manifest()
    if not tools_manifest:
        return

    # Crear herramientas para Gemini
    try:
        gemini_tools = [
            genai.types.FunctionDeclaration(
                name=tool_name,
                description=tool_data.get("description", f"Herramienta {tool_name}"),
                parameters=tool_data.get("input_schema", {"type": "object", "properties": {}})
            )
            for tool_name, tool_data in tools_manifest.items()
        ]
    except Exception as e:
        print(f"Error al crear herramientas: {e}")
        return

    model = genai.GenerativeModel("gemini-1.5-flash", tools=gemini_tools)
    # 🤖 Inicia una nueva sesión de chat.
    chat = model.start_chat()
    
    print("MCP Agent iniciado. Escribe 'salir' para terminar.")
    
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == 'salir':
            print("Agente MCP desconectado.")
            break

        try:
            # ➡️ Envía el mensaje del usuario al chat.
            response = chat.send_message(user_input)

            # Procesa las partes de la respuesta en un solo bucle.
            for part in response.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    tool_name = part.function_call.name
                    parameters = dict(part.function_call.args)
                    
                    print(f"[Agente]: Llamando a la herramienta '{tool_name}' con parámetros {parameters}")
                    
                    try:
                        # 🔄 Ejecuta la herramienta.
                        tool_response = execute_tool_call(tool_name, parameters)

                        # ↩️ Envía el resultado de la herramienta de vuelta al chat.
                        # El modelo ahora usa este resultado para generar una respuesta para el usuario.
                        chat_response = chat.send_message(
                            genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=tool_name,
                                    response=tool_response
                                )
                            )
                        )
                        # 📝 Imprime la respuesta final que el modelo genera.
                        print(f"[Agente]: {chat_response.text}")
                    except Exception as e:
                        print(f"[Agente]: Error al ejecutar la herramienta: {e}")
                elif hasattr(part, 'text') and part.text:
                    # Si no hay llamada a herramienta, imprime la respuesta directamente.
                    print(f"[Agente]: {part.text}")
                else:
                    # Manejo de otros tipos de respuesta no esperados
                    print("[Agente]: No pude procesar la respuesta del modelo.")

        except Exception as e:
            print(f"Error en la conversación con Gemini: {e}")
            print(f"Tipo de error: {type(e).__name__}")

if __name__ == "__main__":
    chat_with_agent()