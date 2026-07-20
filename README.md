# Speech-to-Paste

Local speech recognition with automatic clipboard integration and LLM-based text cleaning.

Record audio with a hotkey, transcribe with Whisper, optionally clean the text with an LLM via OpenRouter, and paste the result anywhere with Ctrl+V.

## Features

- Continuous audio recording from microphone via hotkey (Break key or Ctrl+Shift+P)
- Real-time transcription using [whisper.cpp](https://github.com/ggerganov/whisper.cpp) server mode
- Optional AI text cleaning via OpenRouter (removes filler words, fixes grammar)
- Automatic clipboard copy (uses `xclip`)
- Audio feedback tones on start/stop/clipboard

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (fast Python package installer)
- System packages:
  ```bash
  sudo apt-get install portaudio19-dev xclip ffmpeg
  ```
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp) with CUDA support (see below)

## Installation

### 1. Install whisper.cpp

```bash
git clone https://github.com/ggerganov/whisper.cpp ~/tools/whisper.cpp
cd ~/tools/whisper.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build -j --target whisper-server
```

Download a model (e.g. large-v3-turbo Q8_0):

```bash
cd ~/tools/whisper.cpp
./models/download-ggml-model.sh large-v3-turbo-q8_0
```

### 2. Set up Python environment

```bash
# Navigate to the project
cd ~/tools/repos/speech-to-paste

# Create virtual environment with uv
uv venv

# Activate it
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Install PyAudio separately (native extension that sometimes needs manual handling)
uv pip install pyaudio
```

### 3. Configure API key

```bash
cp .env.example .env
# Edit .env and add your OpenRouter API key:
#   API_KEY="sk-or-v1-..."
```

## Usage

```bash
cd ~/tools/repos/speech-to-paste
source .venv/bin/activate
python3 -m speech_to_paste
```

**Hotkeys:**
- Press **Pause/Break** — start/stop recording
- Press **Ctrl+Shift+P** — alternative start/stop

Once stopped, the audio is transcribed, optionally cleaned by the LLM, and the result lands in your clipboard — just paste with Ctrl+V.

## Project Structure

```
speech-to-paste/
├── speech_to_paste/
│   ├── __main__.py          # Application entry point (run via `python -m speech_to_paste`)
│   ├── config.py            # Central configuration and environment
│   ├── audio_recorder.py    # Microphone recording via PyAudio
│   ├── transcriber.py       # Whisper transcription via server endpoint
│   ├── clipboard_manager.py # xclip integration + text cleaning orchestration
│   ├── text_cleaner.py      # OpenRouter LLM call for text cleaning
│   ├── hotkey_manager.py    # Pause/Break and Ctrl+Shift+P hotkey handling
│   ├── notification_manager.py  # Audio feedback tones (pygame)
│   ├── transcription_monitor.py # File-based monitoring helper
│   └── utils.py             # String similarity utilities (Jaccard, Levenshtein)
├── tests/
│   ├── test_text_cleaning.py   # Tests for text cleaning
│   ├── test_integration.py     # Integration tests for clipboard manager
│   └── test_audio.py           # Quick audio recording test
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

Run tests:

```bash
cd ~/tools/repos/speech-to-paste
PYTHONPATH=. python3 -m pytest tests/
```
