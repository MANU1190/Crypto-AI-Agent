# translation_tool.py
import logging
from transformers import pipeline
from langdetect import detect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TranslationTool:
    def __init__(self, model_name="Helsinki-NLP/opus-mt-en-es"):  # English to Spanish as default
        self.translator = pipeline("translation", model=model_name)

    def translate(self, text, target_language='en'):
        try:
            translated = self.translator(text, max_length=512)[0]['translation_text']
            return translated
        except Exception as e:
            logging.error(f"Translation failed: {str(e)}")
            return f"Translation failed: {str(e)}"

def is_english(text):
    try:
        lang = detect(text)
        return lang == 'en'
    except:
        return True  # Default to True if language detection fails
