from gtts import gTTS
import uuid
import os

def text_to_speech(text):
    os.makedirs("audio", exist_ok=True)
    filename = f"audio_{uuid.uuid4()}.mp3"
    filepath = f"audio/{filename}"

    tts = gTTS(text=text, lang="en")
    tts.save(filepath)

    return filepath
