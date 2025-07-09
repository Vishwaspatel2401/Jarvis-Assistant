import logging
from typing import Optional
from src.features.speech import SpeechEngine
from src.features.voice_recognition import VoiceRecognizer
from src.features.reminders import ReminderManager
from src.features.news import NewsService
from src.features.weather import WeatherService
from src.features.email import EmailService
from src.features.system import SystemController
from src.utils.config_manager import ConfigManager

class JarvisAssistant:
    def __init__(self):
        self.config = ConfigManager()
        self.speech = SpeechEngine(self.config)
        self.voice_recognizer = VoiceRecognizer()
        self.reminder_manager = ReminderManager(self.config)
        self.news_service = NewsService(self.config)
        self.weather_service = WeatherService(self.config)
        self.email_service = EmailService(self.config)
        self.system_controller = SystemController(self.config)
        self.is_listening = True

    def wish_me(self) -> None:
        """Greet user based on time of day"""
        from datetime import datetime
        hour = datetime.now().hour
        greeting = "Good Morning" if 0 <= hour < 12 else "Good Afternoon" if 12 <= hour < 18 else "Good Evening"
        self.speech.speak(f"{greeting}. I am Jarvis, your personal assistant. How may I help you today?")

    def process_command(self, query: str) -> None:
        """Process and execute voice commands"""
        if not query:
            return

        try:
            if "wikipedia" in query:
                self.speech.speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = self.news_service.search_wikipedia(query)
                self.speech.speak("According to Wikipedia")
                print(results)
                self.speech.speak(results)

            elif "weather" in query:
                city = query.split("weather in ")[-1] if "weather in " in query else "London"
                weather_info = self.weather_service.get_weather(city)
                self.speech.speak(weather_info)

            elif "volume" in query or "brightness" in query:
                self.system_controller.control_system(query)
                self.speech.speak("System settings adjusted")

            elif "time" in query:
                from datetime import datetime
                str_time = datetime.now().strftime("%H:%M:%S")
                self.speech.speak(f"The current time is {str_time}")

            elif "open" in query:
                self.system_controller.open_website(query)

            elif "system" in query and "info" in query:
                system_info = self.system_controller.get_system_info()
                self.speech.speak(system_info)

            elif "news" in query:
                category = "general"
                if "tech" in query:
                    category = "technology"
                elif "sports" in query:
                    category = "sports"
                elif "business" in query:
                    category = "business"
                news = self.news_service.get_news(category)
                self.speech.speak(news)

            elif "reminder" in query:
                self.reminder_manager.handle_reminder_command(query)

            elif "email" in query:
                self.email_service.handle_email_command(query, self.speech)

        except Exception as e:
            logging.error(f"Error processing command: {str(e)}")
            self.speech.speak("I encountered an error processing that command")

    def run(self):
        """Main loop for the assistant"""
        try:
            self.wish_me()
            
            while self.is_listening:
                query = self.voice_recognizer.take_command()
                if query:
                    if query.lower() == 'quit':
                        self.is_listening = False
                    else:
                        self.process_command(query)
        finally:
            self.speech.cleanup() 