# Voice Translator con Azure Speech y Gradio

Este proyecto es una aplicación de traducción de voz que utiliza el servicio de Azure Speech para transcribir y traducir audio en varios idiomas. La interfaz gráfica es proporcionada por la librería Gradio, lo que permite una interacción fácil y rápida con la aplicación desde un navegador web.

## Características

- **Transcripción de Audio**: Convierte el audio hablado en texto utilizando Azure Speech.
- **Traducción**: Traduce el texto transcrito a varios idiomas (Inglés, Portugués, Francés).
- **Síntesis de Voz**: Convierte el texto traducido de vuelta a audio, permitiendo escuchar la traducción en diferentes voces.
- **Interfaz de Usuario**: La librería Gradio facilita una interfaz de usuario web, lo que permite cargar archivos de audio y recibir las traducciones en forma de texto y audio.

## Requisitos

- Python 3.9 o superior
- Una cuenta de Microsoft Azure con acceso al servicio Azure Speech.
- Las siguientes librerías de Python:

```bash
pip install -r requirements.txt
```

## Uso

```bash
python -u app.py
```
