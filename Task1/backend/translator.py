from googletrans import Translator

translator = Translator()

LANG_MAP = {
    "English": "en",
    "Hindi": "hi",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Japanese": "ja",
    "Auto Detect": "auto"
}

def translate_text(text, source_lang, target_lang):
    src = LANG_MAP.get(source_lang, "auto")
    dest = LANG_MAP.get(target_lang, "en")

    translated = translator.translate(text, src=src, dest=dest)
    return translated.text
