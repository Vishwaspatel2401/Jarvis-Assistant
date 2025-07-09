import speech_recognition as sr
import logging
from typing import Optional

class VoiceRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def take_command(self) -> Optional[str]:
        """Listen for and process voice commands"""
        try:
            with sr.Microphone() as source:
                print('Listening...')
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            logging.error(f"Error in take_command: {str(e)}")
            return None 