import os
import subprocess
import tempfile
import requests
import time
from .config import WHISPER_PATH, WHISPER_EXECUTABLE, WHISPER_SERVER_EXECUTABLE, WHISPER_MODEL, WHISPER_SERVER_PORT
import wave

class Transcriber:
    def __init__(self):
        self.model_path = os.path.join(WHISPER_PATH, f"models/ggml-{WHISPER_MODEL}.bin")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Whisper Modell nicht gefunden: {self.model_path}")
            
        # Starte den Whisper-Server-Prozess
        self.server_process = None
        self._start_server()
    
    def _start_server(self):
        """Startet den Whisper-Server-Prozess"""
        import socket
        
        # Prüfe, ob der Port bereits verwendet wird
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('localhost', WHISPER_SERVER_PORT))
                print(f"Port {WHISPER_SERVER_PORT} ist bereits belegt. Bitte wählen Sie einen anderen Port.")
                raise Exception(f"Port {WHISPER_SERVER_PORT} ist bereits belegt")
            except ConnectionRefusedError:
                # Port ist frei, das ist gut
                pass
        
        try:
            # Starte den Whisper-Server als Hintergrundprozess
            cmd = [
                WHISPER_SERVER_EXECUTABLE,
                "--model", self.model_path,
                "--port", str(WHISPER_SERVER_PORT),
                "--language", "de"
            ]
            print(f"Starte Whisper-Server mit Befehl: {' '.join(cmd)}")
            
            # Starte den Server und leite Ausgaben weiter
            self.server_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Warte kurz, damit der Server starten kann
            time.sleep(5)  # Länger warten, damit der Server vollständig starten kann
            
            # Prüfe, ob der Prozess noch läuft
            if self.server_process.poll() is not None:
                # Der Prozess ist bereits beendet, lies Fehlermeldung
                _, stderr = self.server_process.communicate()
                print(f"Whisper-Server konnte nicht gestartet werden: {stderr.decode()}")
                raise Exception(f"Whisper-Server konnte nicht gestartet werden: {stderr.decode()}")
            
            print(f"Whisper-Server erfolgreich auf Port {WHISPER_SERVER_PORT} gestartet.")
            
        except Exception as e:
            print(f"Fehler beim Starten des Whisper-Servers: {e}")
            raise e
    
    def _stop_server(self):
        """Stoppt den Whisper-Server-Prozess"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("Whisper-Server gestoppt.")
    
    def transcribe_file(self, audio_file_path):
        """Transkribiert eine Audiodatei mit Whisper unter Verwendung des Servers.
        Falls die Datei zu lang ist, wird sie in Blöcke aufgeteilt."""
        # Überprüfe die Länge der Audiodatei
        duration = self._get_audio_duration(audio_file_path)
        
        # Wenn die Datei länger als 5 Minuten ist, teile sie in Blöcke
        if duration > 300:  # 5 Minuten in Sekunden
            print(f"Audiodatei ist {duration} Sekunden lang, wird in Blöcke aufgeteilt...")
            return self._transcribe_large_file(audio_file_path)
        else:
            return self._transcribe_single_file(audio_file_path)
    
    def _get_audio_duration(self, file_path):
        """Berechnet die Dauer einer Audiodatei in Sekunden"""
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = frames / float(rate)
            return duration
    
    def _split_audio_file(self, file_path, chunk_duration=300):  # 5 Minuten pro Chunk
        """Teilt eine Audiodatei in kleinere Blöcke"""
        import math
        
        duration = self._get_audio_duration(file_path)
        total_chunks = math.ceil(duration / chunk_duration)
        
        chunk_paths = []
        with wave.open(file_path, 'rb') as original_wf:
            channels = original_wf.getnchannels()
            sample_width = original_wf.getsampwidth()
            frame_rate = original_wf.getframerate()
            
            for i in range(total_chunks):
                start_frame = int(i * chunk_duration * frame_rate)
                end_frame = min(int((i + 1) * chunk_duration * frame_rate), original_wf.getnframes())
                num_frames = end_frame - start_frame
                
                # Erstelle temporäre Datei für den Chunk
                chunk_filename = os.path.join(os.path.dirname(file_path), f"chunk_{i}_{os.path.basename(file_path)}")
                
                with wave.open(chunk_filename, 'wb') as chunk_wf:
                    chunk_wf.setnchannels(channels)
                    chunk_wf.setsampwidth(sample_width)
                    chunk_wf.setframerate(frame_rate)
                    
                    # Gehe zur Startposition und lese Frames
                    original_wf.setpos(start_frame)
                    frames_data = original_wf.readframes(num_frames)
                    chunk_wf.writeframes(frames_data)
                
                chunk_paths.append(chunk_filename)
        
        return chunk_paths
    
    def _transcribe_large_file(self, audio_file_path):
        """Transkribiert eine große Audiodatei durch Aufteilung in Blöcke"""
        # Teile die Datei in Blöcke
        chunk_paths = self._split_audio_file(audio_file_path)
        
        transcriptions = []
        
        try:
            # Transkribiere jeden Block
            for i, chunk_path in enumerate(chunk_paths):
                print(f"Transkribiere Chunk {i+1}/{len(chunk_paths)}...")
                chunk_transcription = self._transcribe_single_file(chunk_path)
                transcriptions.append(chunk_transcription)
                
                # Lösche den temporären Chunk nach der Transkription
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
        
        except Exception as e:
            print(f"Fehler bei der Verarbeitung der großen Datei: {e}")
            # Lösche alle verbleibenden Chunks im Fehlerfall
            for chunk_path in chunk_paths:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)
            return ""
        
        # Kombiniere alle Transkriptionen zu einem Text
        full_transcription = " ".join(transcriptions).strip()
        return full_transcription
    
    def _transcribe_single_file(self, audio_file_path):
        """Transkribiert eine einzelne Audiodatei über den Server"""
        try:
            # Sende die Audiodatei an den Whisper-Server
            with open(audio_file_path, 'rb') as audio_file:
                files = {'file': audio_file}
                # Die Anfrageparameter an die verfügbaren Optionen anpassen
                response = requests.post(
                    f"http://localhost:{WHISPER_SERVER_PORT}/inference",
                    files=files,
                    data={
                        'language': 'de',
                        'task': 'transcribe'  # Standard-Task
                    }
                )
                
            if response.status_code == 200:
                # Prüfe, ob die Antwort bereits im richtigen Format vorliegt
                result = response.text.strip()
                
                # Falls die Antwort im JSON-Format vorliegt, extrahiere den Text
                if result.startswith('{') and result.endswith('}'):
                    import json
                    try:
                        json_response = json.loads(result)
                        # Versuche verschiedene mögliche Felder für den Text
                        if 'text' in json_response:
                            return json_response['text']
                        elif 'data' in json_response and isinstance(json_response['data'], str):
                            return json_response['data']
                        else:
                            # Wenn unbekanntes Format, gib die Rohantwort zurück
                            return str(json_response)
                    except json.JSONDecodeError:
                        # Wenn keine gültige JSON-Datei, gib Rohantwort zurück
                        return result
                else:
                    # Wenn keine JSON-Antwort, gib einfach den Text zurück
                    return result
            else:
                print(f"Fehler bei der Server-Transkription: {response.status_code} - {response.text}")
                return ""
                
        except Exception as e:
            print(f"Fehler bei der Server-Transkription: {e}")
            return ""
    
    def transcribe_audio(self, audio_data):
        """Transkribiert Audio-Daten mit Whisper (kompatibilitätshalber)"""
        # Erstelle temporäre WAV-Datei
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav_path = temp_wav.name
            
        # Speichere Audio-Daten als WAV
        self._save_as_wav(audio_data, temp_wav_path)
        
        # Nutze die neue Methode
        result = self.transcribe_file(temp_wav_path)
        
        # Lösche temporäre WAV-Datei
        if os.path.exists(temp_wav_path):
            os.remove(temp_wav_path)
            
        return result
    
    def _save_as_wav(self, audio_data, filename):
        """Speichert Audio-Daten als WAV-Datei"""
        import wave
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(16000)  # 16kHz
            wf.writeframes(audio_data)
    
    def cleanup(self):
        """Stoppt den Server und bereinigt Ressourcen"""
        self._stop_server()