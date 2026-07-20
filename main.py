#!/usr/bin/env python3

import threading
import time
import signal
import sys
import os
import tempfile
import config
from audio_recorder import AudioRecorder
from transcriber import Transcriber
from hotkey_manager import HotkeyManager
from clipboard_manager import ClipboardManager

class SpeechToPaste:
    def __init__(self):
        self.audio_recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.hotkey_manager = HotkeyManager()
        self.clipboard_manager = ClipboardManager()
        self.running = False
        
    def start(self):
        """
        Startet die speech-to-paste Anwendung
        """
        print("Starte Speech-to-Paste Anwendung...")
        
        # Signalhandler für sauberes Beenden
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Setup hotkey callbacks
        self.hotkey_manager.set_callbacks(
            on_start=self._start_recording,
            on_end=self._end_recording
        )
        
        # Start hotkey manager
        self.hotkey_manager.start_listening()
        self.running = True
        
        print("Anwendung gestartet. Drücken Sie STRG+C oder die Break-Taste zum Beenden.")
        print("Drücken Sie die Break-Taste, um die Audioaufnahme zu starten/stoppen.")
        
        try:
            # Warte auf Signale - keine kontinuierliche Aufnahme
            while self.running:
                time.sleep(0.1)
        except Exception as e:
            print(f"Fehler in der Hauptloop: {e}")
        finally:
            self.stop()
            
    def _start_recording(self):
        """
        Startet die Audioaufnahme
        """
        print("Starte Audioaufnahme...")
        self.audio_recorder.start_recording()
        
    def _end_recording(self):
        """
        Beendet die Audioaufnahme und verarbeitet den Text
        """
        print("Beende Audioaufnahme und starte Verarbeitung...")
        
        # Stoppe die Aufnahme
        self.audio_recorder.stop_recording()
        
        # Erstelle temporäres Verzeichnis, falls nicht vorhanden
        os.makedirs(config.TEMP_DIR, exist_ok=True)

        # Speichere die Aufnahme in einer temporären Datei
        temp_filename = tempfile.mktemp(suffix=".wav", dir=config.TEMP_DIR)
        
        if self.audio_recorder.save_recording_to_temp_file(temp_filename):
            try:
                # Transkribiere die Audiodatei
                transcription = self.transcriber.transcribe_file(temp_filename)
                
                if transcription:
                    # Verarbeite und kopiere den Text in die Zwischenablage
                    self.clipboard_manager.process_and_copy_text(transcription)
                    print(f"Transkribierter Text verarbeitet und in Zwischenablage kopiert: {transcription[:100]}{'...' if len(transcription) > 100 else ''}")
                else:
                    print("Kein Text zum Verarbeiten gefunden.")
            finally:
                # Lösche die temporäre Datei nach der Verarbeitung
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
        else:
            print("Fehler beim Speichern der Audiodatei.")
        
    def stop(self):
        """
        Stoppt die Anwendung sauber
        """
        print("\nStoppe Anwendung...")
        self.running = False
        self.audio_recorder.cleanup()
        self.transcriber.cleanup()  # Bereinige den Transcriber (stoppe den Server)
        self.hotkey_manager.stop_listening()
        print("Anwendung gestoppt.")
        
    def _signal_handler(self, signum, frame):
        """
        Signalhandler für sauberes Beenden
        """
        print("\nEmpfangenes Signal, beende Anwendung...")
        self.stop()
        sys.exit(0)

if __name__ == "__main__":
    app = SpeechToPaste()
    app.start()