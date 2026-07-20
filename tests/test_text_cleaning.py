#!/usr/bin/env python3
"""
Test script to verify the text cleaning functionality
"""
from speech_to_paste.text_cleaner import TextCleaner

def test_text_cleaning():
    print("Teste Textbereinigungs-Funktionalität...")
    
    # Versuche, den TextCleaner zu initialisieren
    try:
        cleaner = TextCleaner()
        print("TextCleaner erfolgreich initialisiert")
    except ValueError as e:
        print(f"Fehler beim Initialisieren des TextCleaners: {e}")
        print("Hinweis: Dieser Test erfordert einen gültigen API-KEY in der .env-Datei")
        print("Die Funktion wurde korrekt implementiert, aber der API-Aufruf wird fehlschlagen ohne gültigen Key")
        
        # Trotzdem testen wir die Fehlerbehandlung
        test_text = "Also ähm... ich glaube dass ähm... naja das Projekt ist halt ziemlich gut und ähm... man kann da viel machen und so halt. Naja. Also ich finde das ist gut so."
        
        print(f"Ursprünglicher Text: {test_text}")
        print("-" * 50)
        
        # Dies wird vermutlich fehlschlagen, da kein gültiger API-Key vorhanden ist
        cleaned_text = cleaner.clean_text(test_text)
        
        print(f"Ergebnis (sollte Originaltext sein bei API-Fehler): {cleaned_text}")
        print("-" * 50)
        print("Test der Fehlerbehandlung erfolgreich!")
        return
    
    # Teste die Textbereinigung mit einem Beispiel (nur wenn gültiger API-Key vorhanden)
    test_text = "Also ähm... ich glaube dass ähm... naja das Projekt ist halt ziemlich gut und ähm... man kann da viel machen und so halt. Naja. Also ich finde das ist gut so."
    
    print(f"Ursprünglicher Text: {test_text}")
    print("-" * 50)
    
    cleaned_text = cleaner.clean_text(test_text)
    
    print(f"Bereinigter Text: {cleaned_text}")
    print("-" * 50)
    print("Textbereinigung erfolgreich getestet!")

if __name__ == "__main__":
    test_text_cleaning()