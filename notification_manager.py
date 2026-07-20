import math
import numpy as np
import pygame
import os
from config import START_SOUND_FILE, END_SOUND_FILE, CLIPBOARD_SOUND_FILE

class NotificationManager:
    _initialized = False

    def __init__(self):
        # Initialize pygame mixer only once
        if not NotificationManager._initialized:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            NotificationManager._initialized = True
        self.generate_notification_sounds()
    
    def generate_tone(self, frequency, duration, sample_rate=22050):
        """
        Generate a sine wave tone
        
        Args:
            frequency: Frequency of the tone in Hz
            duration: Duration of the tone in seconds
            sample_rate: Sample rate for the audio
            
        Returns:
            numpy array containing the audio data
        """
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))  # Stereo array
        
        for i in range(frames):
            wave = 4096 * math.sin(2 * math.pi * frequency * i / sample_rate)
            arr[i][0] = wave  # Left channel
            arr[i][1] = wave  # Right channel
            
        return arr.astype(np.int16)
    
    def save_tone(self, filename, frequency, duration):
        """
        Save a tone to a WAV file
        
        Args:
            filename: Path to save the WAV file
            frequency: Frequency of the tone in Hz
            duration: Duration of the tone in seconds
        """
        tone = self.generate_tone(frequency, duration)
        # Use scipy to save as WAV if available, otherwise skip this functionality
        try:
            from scipy.io.wavfile import write
            write(filename, 22050, tone)
        except ImportError:
            # If scipy is not available, we'll play the tone directly without saving
            pass
    
    def generate_notification_sounds(self):
        """
        Generate standard notification sounds if they don't exist
        """
        # For this implementation, we'll just play tones directly
        pass
    
    def play_start_notification(self):
        """
        Play a short start notification sound
        """
        try:
            # Generate a higher pitch tone for start
            tone = self.generate_tone(800, 0.2)  # 800Hz for 0.2 seconds
            sound = pygame.sndarray.make_sound(tone)
            sound.play()
            pygame.time.wait(250)  # Wait for the sound to finish playing
        except Exception as e:
            print(f"Warning: Could not play start notification: {e}")
    
    def play_end_notification(self):
        """
        Play a short end notification sound
        """
        try:
            # Generate a lower pitch tone for end
            tone = self.generate_tone(400, 0.2)  # 400Hz for 0.2 seconds
            sound = pygame.sndarray.make_sound(tone)
            sound.play()
            pygame.time.wait(250)  # Wait for the sound to finish playing
        except Exception as e:
            print(f"Warning: Could not play end notification: {e}")
    
    def play_clipboard_notification(self):
        """
        Play a notification sound when text is copied to clipboard
        """
        try:
            # Generate a medium pitch tone for clipboard notification (different from start and end)
            tone = self.generate_tone(600, 0.2)  # 600Hz for 0.2 seconds
            sound = pygame.sndarray.make_sound(tone)
            sound.play()
            pygame.time.wait(250)  # Wait for the sound to finish playing
        except Exception as e:
            print(f"Warning: Could not play clipboard notification: {e}")