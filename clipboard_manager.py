import subprocess
import os
from notification_manager import NotificationManager
from text_cleaner import TextCleaner

class ClipboardManager:
    def __init__(self):
        # Prüfe, ob xclip verfügbar ist
        if not self._is_xclip_available():
            raise RuntimeError("xclip ist nicht verfügbar. Bitte installieren Sie xclip.")
        
        # Initialisiere TextCleaner für die Textbereinigung
        try:
            self.text_cleaner = TextCleaner()
        except ValueError as e:
            print(f"Warnung: {e}")
            print("Textbereinigung wird deaktiviert.")
            self.text_cleaner = None
        
        # Initialize notification manager for audio feedback
        self.notification_manager = NotificationManager()
    
    def _is_xclip_available(self):
        """Prüft, ob xclip verfügbar ist"""
        try:
            subprocess.run(["which", "xclip"], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def copy_to_clipboard(self, text):
        """Kopiert Text in die Zwischenablage"""
        try:
            process = subprocess.Popen(["xclip", "-selection", "clipboard"], 
                                     stdin=subprocess.PIPE, 
                                     text=True)
            process.communicate(input=text)
            if process.returncode == 0:
                print(f"Text in Zwischenablage kopiert ({len(text)} Zeichen)")
            else:
                print("Fehler beim Kopieren in die Zwischenablage")
        except Exception as e:
            print(f"Fehler beim Kopieren in die Zwischenablage: {e}")
    
    def process_and_copy_text(self, text):
        """
        Bereinigt den Text und kopiert ihn in die Zwischenablage
        
        Args:
            text (str): Der zu bereinigende und kopierende Text
        """
        # Bereinige den Text mit dem LLM, falls verfügbar
        if text and self.text_cleaner:
            print("Bereinige den Text mit OpenRouter LLM...")
            cleaned_text = self.text_cleaner.clean_text(text)
            print(f"Bereinigung abgeschlossen. Ursprüngliche Länge: {len(text)}, Bereinigte Länge: {len(cleaned_text)}")
            
            # Kopiere bereinigten Text in Zwischenablage
            self.copy_to_clipboard(cleaned_text)
            # Play notification when text is copied to clipboard
            self.notification_manager.play_clipboard_notification()
        elif text and not self.text_cleaner:
            # Falls TextCleaner nicht verfügbar, kopiere Originaltext
            self.copy_to_clipboard(text)
            # Play notification when text is copied to clipboard
            self.notification_manager.play_clipboard_notification()