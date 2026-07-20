import pyaudio
import wave
import threading
import time
import os
from .config import SAMPLE_RATE, CHANNELS

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.is_recording = False
        self.stream = None
        self.frames = []
        
    def start_recording(self):
        """Startet die Audioaufnahme nach Hotkey-Druck"""
        if self.is_recording:
            return
            
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                frames_per_buffer=1024
            )
            self.is_recording = True
            self.frames = []  # Leere den Frame-Puffer
            
            print("Audioaufnahme gestartet...")
        except Exception as e:
            print(f"Fehler beim Starten der Audioaufnahme: {e}")
            raise e
        
    def stop_recording(self):
        """Stoppt die Audioaufnahme und sammelt alle Frames"""
        if not self.is_recording or not self.stream:
            return
            
        # Stoppe den Stream und sammle alle verbleibenden Frames
        self.is_recording = False
        
        # Lies alle verbleibenden Frames aus dem Stream
        while self.stream.get_read_available() > 0:
            try:
                data = self.stream.read(1024, exception_on_overflow=False)
                self.frames.append(data)
            except:
                break
        
        self.stream.stop_stream()
        self.stream.close()
        
        print("Audioaufnahme gestoppt.")
        
    def save_recording_to_temp_file(self, temp_path):
        """Speichert die aufgenommenen Frames in einer temporären WAV-Datei"""
        if not self.frames:
            print("Keine Audio-Daten zum Speichern vorhanden.")
            return False
            
        try:
            with wave.open(temp_path, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(b''.join(self.frames))
            
            print(f"Audiodatei gespeichert unter: {temp_path}")
            return True
        except Exception as e:
            print(f"Fehler beim Speichern der Audiodatei: {e}")
            return False
            
    def get_recording_frames(self):
        """Gibt die aktuellen Aufnahme-Frames zurück"""
        return self.frames.copy()
        
    def cleanup(self):
        """Bereinigt die Audio-Ressourcen"""
        if self.stream and not self.stream.is_stopped():
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()