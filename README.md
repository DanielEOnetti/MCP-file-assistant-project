Asistente de Archivos de IA
Este proyecto es un agente de inteligencia artificial conversacional que utiliza la API de Google Gemini para interactuar con el sistema de archivos local. Demuestra la capacidad de los modelos de IA para utilizar herramientas externas y ejecutar acciones en un entorno controlado.

La arquitectura del proyecto está dividida en dos partes:

Un backend desarrollado en Django que expone las funcionalidades del sistema de archivos a través de una API REST.

Un cliente que se conecta a la API de Gemini, entiende las peticiones del usuario y, si es necesario, llama a las herramientas de nuestro backend para completar la tarea.

Características 🛠️
Lectura de archivos: El agente puede leer el contenido de archivos de texto (.txt) y documentos de Word (.docx).

Escritura de archivos: Permite al usuario crear nuevos archivos de texto o modificar los existentes.

Listado de archivos: Muestra la lista de todos los archivos permitidos en el directorio de trabajo (/files).

Seguridad mejorada: El backend incluye validación de rutas para prevenir ataques de "path traversal" y restringe los tipos de archivos que pueden ser manipulados.

Código eficiente: El cliente utiliza un historial de conversación para una interacción fluida con Gemini, reduciendo la latencia y el uso de la API.

Tecnologías Utilizadas
Backend: Python, Django, Django REST Framework, python-docx.

Cliente de IA: Google Gemini API (SDK de Python), requests, python-dotenv.

Gestión de código: Git, GitHub.

Configuración del Entorno 🚀
Sigue estos pasos para configurar y ejecutar el proyecto localmente.

1. Clonar el Repositorio
Abre tu terminal y clona este repositorio:

Bash

git clone https://github.com/DanielEOnetti/MCP-file-assistant-project.git
cd tu_repositorio
2. Crear y Activar el Entorno Virtual
Es fundamental trabajar en un entorno virtual para gestionar las dependencias del proyecto de forma aislada.

Bash

python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
3. Instalar Dependencias
Instala todas las bibliotecas necesarias usando el archivo requirements.txt:

Bash

pip install -r requirements.txt
4. Configurar la Clave de API
Crea un archivo llamado .env en la carpeta raíz del proyecto y añade tu clave de API de Gemini:

Fragmento de código

GEMINI_API_KEY=tu_clave_de_api
Uso del Agente 🤖
Una vez que hayas completado la configuración, puedes iniciar el agente.

1. Iniciar el Servidor del Backend
Abre tu primera terminal y ejecuta el servidor de Django. Esto hará que la API de herramientas esté disponible.

Bash

python manage.py runserver
2. Iniciar el Cliente de IA
Abre una segunda terminal y ejecuta el cliente. Se conectará automáticamente al servidor que acabas de iniciar.

Bash

python client.py
Ahora puedes interactuar con el agente en esta terminal.

Licencia
Este proyecto está bajo la Licencia MIT.
