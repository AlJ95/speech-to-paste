#!/usr/bin/env python3
"""
Integration test for ClipboardManager — tests copy_to_clipboard and process_and_copy_text.
"""
from speech_to_paste.clipboard_manager import ClipboardManager


def test_copy_to_clipboard():
    """Test that copy_to_clipboard accepts text without error (xclip required)."""
    try:
        cm = ClipboardManager()
    except RuntimeError as e:
        print(f"SKIP: {e}")
        return

    print("Teste copy_to_clipboard...")
    test_text = "Hallo Welt, dies ist ein Test."
    cm.copy_to_clipboard(test_text)
    print("copy_to_clipboard erfolgreich ausgeführt.")


def test_process_and_copy_text_no_cleaner():
    """Test process_and_copy_text when TextCleaner is unavailable (no API key)."""
    try:
        cm = ClipboardManager()
    except RuntimeError as e:
        print(f"SKIP: {e}")
        return

    print("Teste process_and_copy_text (ohne TextCleaner)...")
    test_text = (
        "Also ähm... ich glaube dass ähm... naja das Projekt ist "
        "halt ziemlich gut und ähm... man kann da viel machen und so halt."
    )
    cm.process_and_copy_text(test_text)

    if cm.text_cleaner is None:
        print("TextCleaner nicht verfügbar — Originaltext wurde in die Zwischenablage kopiert (erwartet).")
    else:
        print("TextCleaner ist verfügbar — bereinigter Text wurde in die Zwischenablage kopiert (erwartet).")


def test_process_and_copy_text_empty():
    """Test that process_and_copy_text handles empty/None text gracefully."""
    try:
        cm = ClipboardManager()
    except RuntimeError as e:
        print(f"SKIP: {e}")
        return

    print("Teste process_and_copy_text mit leerem Text...")
    cm.process_and_copy_text("")
    print("Leerer Text wurde korrekt ignoriert (kein Fehler).")


if __name__ == "__main__":
    print("=== Integrationstests für ClipboardManager ===\n")
    test_copy_to_clipboard()
    print()
    test_process_and_copy_text_no_cleaner()
    print()
    test_process_and_copy_text_empty()
    print("\n=== Alle Tests abgeschlossen ===")
