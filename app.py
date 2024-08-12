import json
import os
import gradio as gr
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv

load_dotenv()

cog_key = os.getenv('COG_SERVICE_KEY')
cog_reg = os.getenv('COG_SERVICE_REGION')

with open('code_languages.json', 'r') as file:
    languages_data = json.load(file)
language_names = list(languages_data.keys())

def translator(audio_file, language_input):

    try:
        translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_reg)
        translation_config.speech_recognition_language = "es-ES"

        target_language = languages_data[language_input]["code"][:2]
        print("target_language", target_language)
        translation_config.add_target_language(target_language)

        audio_config = speech_sdk.AudioConfig(filename=audio_file)
        translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
        result = translator.recognize_once_async().get()
        print(f"texto '{result.text}'")

        translation_text = result.translations[target_language]
        print(f"Traduccion a {language_input}: {translation_text}")

        language_save_file_path = text_to_speach(translation_text, language_input)


    except Exception as ex:
        raise gr.Error("Se ha producido un error traducirndo el texto" + str(ex))

    return translation_text, language_save_file_path

def text_to_speach(text: str, language: str):


    try:
        # Synthesize translation
        voice = languages_data[language]["voice"]

        speech_config = speech_sdk.SpeechConfig(cog_key, cog_reg)
        speech_config.speech_synthesis_voice_name = voice

        save_file_path = f"audios/{language}.mp3"
        audio_output = speech_sdk.AudioConfig(filename=save_file_path)

        speeck_synthesis = speech_sdk.SpeechSynthesizer(speech_config, audio_output)
        speak = speeck_synthesis.speak_text_async(text).get()

        if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
            print(speak.reason)

    except Exception as ex:
        raise gr.Error("Se ha producido un error creando el audio:" + str(ex))

    return save_file_path


app = gr.Interface(
    fn=translator,
    inputs=[
        gr.Audio(sources=["microphone"],type="filepath",label="Español"),
        gr.Dropdown(choices=language_names, label="Seleccciona el idioma a traducir")
    ],
    outputs=[
        gr.Textbox(label="Traduccion de texto"),
        gr.Audio(label="Traduccion en audio"),
        ],
    title="Traductor de voz",
    description="Traductor de voz con IA a varios idiomas"
)

app.launch()