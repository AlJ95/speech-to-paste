import os
import tempfile
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

# Konfiguration für das Speech-to-Paste Projekt

# Temporäre Datei für die Transkription
TEMP_DIR = os.path.join(os.path.dirname(__file__), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)
TRANSCRIPTION_FILE = os.path.join(TEMP_DIR, "transcription.txt")

# Sound notification files
NOTIFICATION_SOUNDS_ENABLED = True
START_SOUND_FILE = os.path.join(TEMP_DIR, "start_notification.wav")
END_SOUND_FILE = os.path.join(TEMP_DIR, "end_notification.wav")
CLIPBOARD_SOUND_FILE = os.path.join(TEMP_DIR, "clipboard_notification.wav")

# Audio-Einstellungen
SAMPLE_RATE = 16000  # Whisper bevorzugt 16kHz
CHANNELS = 1         # Mono
CHUNK_DURATION = 3   # Sekunden pro Chunk für bessere Reaktionszeit

# Whisper-Einstellungen
WHISPER_MODEL = "large-v3-turbo-q8_0"  # Verwende das große Modell
WHISPER_PATH = os.path.expanduser("~/tools/whisper.cpp")
WHISPER_EXECUTABLE = os.path.join(WHISPER_PATH, "build/bin/whisper-cli")
WHISPER_SERVER_EXECUTABLE = os.path.join(WHISPER_PATH, "build/bin/whisper-server")
WHISPER_SERVER_PORT = 8085  # Verwende Port 8085 für den Whisper-Server

# OpenRouter LLM Einstellungen
OPENROUTER_API_KEY = os.getenv("API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "ibm-granite/granite-4.1-8b" # "mistralai/mistral-nemo"

