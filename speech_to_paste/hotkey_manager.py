import threading
import time
from pynput import keyboard
from .notification_manager import NotificationManager


class HotkeyManager:
    def __init__(self):
        self.notification_manager = NotificationManager()
        self.recording_active = False
        self.on_start_callback = None
        self.on_end_callback = None
        self.listener = None
        self.running = False
        
        # For tracking key combinations
        self.ctrl_pressed = False
        self.shift_pressed = False

    def set_callbacks(self, on_start=None, on_end=None):
        """Set callbacks for start and end recording events"""
        self.on_start_callback = on_start
        self.on_end_callback = on_end

    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            # Track modifier keys
            if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                self.ctrl_pressed = True
            elif key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
                self.shift_pressed = True
            # Check for Ctrl+Shift+P combination
            elif hasattr(key, 'char') and key.char == 'p' and self.ctrl_pressed and self.shift_pressed:
                if not self.recording_active:
                    # Start recording
                    self.recording_active = True
                    print("Ctrl+Shift+P pressed - Starting transcription...")
                    self.notification_manager.play_start_notification()
                    if self.on_start_callback:
                        self.on_start_callback()
                else:
                    # Stop recording
                    self.recording_active = False
                    print("Ctrl+Shift+P pressed - Stopping transcription...")
                    self.notification_manager.play_end_notification()
                    if self.on_end_callback:
                        self.on_end_callback()
            # Check for Pause/Break key (mapped as 'pause' in pynput)
            elif key == keyboard.Key.pause:
                if not self.recording_active:
                    # Start recording
                    self.recording_active = True
                    print("Pause/Break key pressed - Starting transcription...")
                    self.notification_manager.play_start_notification()
                    if self.on_start_callback:
                        self.on_start_callback()
                else:
                    # Stop recording
                    self.recording_active = False
                    print("Pause/Break key pressed - Stopping transcription...")
                    self.notification_manager.play_end_notification()
                    if self.on_end_callback:
                        self.on_end_callback()
        except Exception as e:
            print(f"Error in key press handler: {e}")

    def _on_key_release(self, key):
        """Handle key release events"""
        try:
            # Reset modifier keys when released
            if key in [keyboard.Key.ctrl_l, keyboard.Key.ctrl_r]:
                self.ctrl_pressed = False
            elif key in [keyboard.Key.shift_l, keyboard.Key.shift_r]:
                self.shift_pressed = False
        except Exception as e:
            print(f"Error in key release handler: {e}")

    def start_listening(self):
        """Start listening for hotkey events"""
        if self.running:
            return
            
        self.running = True
        self.listener = keyboard.Listener(
            on_press=self._on_key_press,
            on_release=self._on_key_release
        )
        self.listener.start()
        print("Hotkey manager started - listening for Pause key and Ctrl+Shift+P...")

    def stop_listening(self):
        """Stop listening for hotkey events"""
        self.running = False
        if self.listener:
            self.listener.stop()
        print("Hotkey manager stopped.")