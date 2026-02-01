from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from translator import translate_text
from tts import text_to_speech

app = FastAPI()

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Request Models ----------
class TranslateRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str

class TTSRequest(BaseModel):
    text: str

# ---------- Routes ----------
@app.post("/translate")
def translate(req: TranslateRequest):
    translated = translate_text(req.text, req.source_lang, req.target_lang)
    return {"translated_text": translated}

@app.post("/tts")
def tts(req: TTSRequest):
    audio_path = text_to_speech(req.text)
    return {"audio_url": f"http://localhost:8000/audio/{audio_path.split('/')[-1]}"}

# Serve audio files
if os.path.exists("audio"):
    app.mount("/audio", StaticFiles(directory="audio"), name="audio")

