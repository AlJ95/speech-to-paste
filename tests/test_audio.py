import pyaudio
import wave

# Audio-Einstellungen
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5

audio = pyaudio.PyAudio()

# Starte die Audioaufnahme
stream = audio.open(format=FORMAT,
                   channels=CHANNELS,
                   rate=RATE,
                   input=True,
                   frames_per_buffer=CHUNK)

print("Starte Aufnahme für 5 Sekunden...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK, exception_on_overflow=False)
    frames.append(data)

print("Aufnahme beendet.")

# Stoppe die Aufnahme
stream.stop_stream()
stream.close()
audio.terminate()

# Speichere die Aufnahme in einer WAV-Datei
wf = wave.open("test.wav", 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

print("Aufnahme gespeichert als test.wav")