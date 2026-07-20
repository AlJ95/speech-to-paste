# Speech-to-Paste

Eine lokale Anwendung zur kontinuierlichen Spracherkennung mit Zwischenablage-Funktionalität.

## Funktionen

- Kontinuierliche Audioaufnahme vom Mikrofon
- Echtzeit-Spracherkennung mit Whisper
- Steuerung per Hotkey (Break-Taste)
- Automatisches Kopieren des transkribierten Textes in die Zwischenablage
- Textbereinigung mit OpenRouter LLM vor dem Kopieren in die Zwischenablage

## Installation

1. Stellen Sie sicher, dass folgende Abhängigkeiten installiert sind:
   - Python 3.13+
   - FFmpeg
   - xclip
   - whisper.cpp (in ~/tools/whisper.cpp)
   - PortAudio-Entwicklungspaket (für PyAudio)

2. Installieren Sie die Systemabhängigkeiten:
   ```bash
   sudo apt-get install portaudio19-dev xclip
   ```

3. Erstellen Sie eine virtuelle Python-Umgebung:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. Installieren Sie die Python-Abhängigkeiten:
   ```bash
   pip3 install -r requirements.txt
   ```

5. Installieren Sie PyAudio manuell:
   ```bash
   pip3 install pyaudio
   ```

6. Laden Sie das Whisper-Modell herunter:
   ```bash
   cd ~/tools/whisper.cpp
   ./models/download-ggml-model.sh large-v3-turbo-q8_0
   ```

7. Richten Sie die OpenRouter-Umgebungsvariablen ein:
   ```bash
   # Erstellen Sie eine .env Datei mit Ihrem API-Key
   cp .env.example .env
   # Bearbeiten Sie die .env Datei und fügen Sie Ihren OpenRouter API-Key ein
   nano .env  # oder verwenden Sie Ihren bevorzugten Editor
   ```

## Verwendung

1. Starten Sie die Anwendung:
   ```bash
   source .venv/bin/activate
   python3 main.py
   ```

2. Verwenden Sie die Hotkey-Steuerung:
   - Drücken Sie einmal die **Pause/Break**-Taste, um die Transkription zu starten
   - Sprechen Sie Ihren Text
   - Drücken Sie erneut die **Pause/Break**-Taste, um die Transkription zu stoppen und den Text in die Zwischenablage zu kopieren

3. Fügen Sie den Text mit STRG+V in Ihre Anwendung ein.

## Alternative Tastenkombination

Falls die Break-Taste auf Ihrem System nicht funktioniert, können Sie alternativ **Ctrl+Shift+P** verwenden, um die Aufnahme zu starten und zu stoppen.