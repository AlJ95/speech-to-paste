import threading
import time
import os
from .config import TRANSCRIPTION_FILE
from .clipboard_manager import ClipboardManager

class TranscriptionMonitor:
    def __init__(self):
        self.clipboard_manager = ClipboardManager()
        self.monitoring = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Startet die kontinuierliche Überwachung der Transkriptionsdatei"""
        if self.monitoring:
            return
            
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("Überwachung der Transkriptionsdatei gestartet...")
        
    def stop_monitoring(self):
        """Stoppt die Überwachung der Transkriptionsdatei"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        print("Überwachung der Transkriptionsdatei gestoppt.")
        
    def _monitor_loop(self):
        """Hauptüberwachungsschleife"""
        while self.monitoring:
            try:
                # Simply clear the transcription file periodically
                if os.path.exists(TRANSCRIPTION_FILE):
                    with open(TRANSCRIPTION_FILE, "w") as f:
                        f.write("")  # Clear the file content
                        
            except Exception as e:
                print(f"Fehler bei der Überwachung: {e}")
                
            time.sleep(0.25)  # 0.25 Sekunden Intervall