import tempfile
import pygame
import time
import logging
from gtts import gTTS
from src.utils.config_manager import ConfigManager

class SpeechEngine:
    def __init__(self, config: ConfigManager):
        self.config = config
        pygame.mixer.init()
        self.voice_cache = {}

    def speak(self, text: str) -> None:
        """Convert text to speech using gTTS"""
        try:
            # Check if we have this text in cache
            if text in self.voice_cache:
                audio_file = self.voice_cache[text]
            else:
                # Create a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    audio_file = fp.name
                
                # Generate speech
                tts = gTTS(text=text, lang=self.config.get('language', 'en'), 
                          slow=self.config.get('slow', False))
                tts.save(audio_file)
                
                # Cache the file
                self.voice_cache[text] = audio_file

            # Play the audio
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for audio to finish playing
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

        except Exception as e:
            logging.error(f"Speech error: {str(e)}")
            print(f"Error in speech: {str(e)}")

    def cleanup(self):
        """Clean up temporary audio files"""
        for audio_file in self.voice_cache.values():
            try:
                import os
                os.unlink(audio_file)
            except:
                pass
        pygame.mixer.quit() 