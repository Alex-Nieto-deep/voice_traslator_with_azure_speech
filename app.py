import os
import gradio as gr
import azure.cognitiveservices.speech as speech_sdk
from dotenv import load_dotenv

load_dotenv()

cog_key = os.getenv('COG_SERVICE_KEY')
cog_reg = os.getenv('COG_SERVICE_REGION')

def translator(audio_file):

    try:
        translation_config = speech_sdk.translation.SpeechTranslationConfig(cog_key, cog_reg)
        translation_config.speech_recognition_language = "es-ES"

        translation_config.add_target_language("pt")
        translation_config.add_target_language("fr")
        translation_config.add_target_language("en")

        audio_config = speech_sdk.AudioConfig(filename=audio_file)
        translator = speech_sdk.translation.TranslationRecognizer(translation_config, audio_config=audio_config)
        result = translator.recognize_once_async().get()
        print(f"texto '{result.text}'")

        translation_fr = result.translations['fr']
        print(f"Traduccion a Frances: {translation_fr}")

        translation_pt = result.translations['pt']
        print(f"Traduccion a Portugues: {translation_pt}")

        translation_en = result.translations['en']
        print(f"Traduccion a Ingles: {translation_en}")

        fr_save_file_path = text_to_speach(translation_fr, 'fr')
        pt_save_file_path = text_to_speach(translation_pt, 'pt')
        en_save_file_path = text_to_speach(translation_en, 'en')

    except Exception as ex:
        raise gr.Error("Se ha producido un error traducirndo el texto" + str(ex))

    return fr_save_file_path, pt_save_file_path, en_save_file_path

def text_to_speach(text: str, language: str):


    try:
        # Synthesize translation
        voices = {
            "fr": "fr-FR-HenriNeural",
            "en": "en-US-GuyNeural",
            "pt": "pt-BR-AntonioNeural",
        }

        speech_config = speech_sdk.SpeechConfig(cog_key, cog_reg)
        speech_config.speech_synthesis_voice_name = voices.get(language)

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
    inputs=gr.Audio(
        sources=["microphone"],
        type="filepath",
        label="Español"
    ),
    outputs=[
        gr.Audio(label="Frances"),
        gr.Audio(label="Portugues"),
        gr.Audio(label="Ingles"),
        ],
    title="Traductor de voz",
    description="Traductor de voz con IA a varios idiomas"
)

app.launch()