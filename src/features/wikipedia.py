import wikipedia
import logging
from typing import Optional
from src.utils.config_manager import ConfigManager

class WikipediaService:
    def __init__(self, config: ConfigManager):
        self.config = config
        wikipedia.set_lang("en")

    def search(self, query: str, sentences: int = 2) -> str:
        """Search Wikipedia for information"""
        try:
            result = wikipedia.summary(query, sentences=sentences)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found. Please be more specific. Options: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return "No results found"
        except Exception as e:
            logging.error(f"Wikipedia search error: {str(e)}")
            return "Error searching Wikipedia"

    def get_random_article(self) -> str:
        """Get a random Wikipedia article"""
        try:
            title = wikipedia.random()
            summary = wikipedia.summary(title, sentences=2)
            return f"Random article: {title}\n{summary}"
        except Exception as e:
            logging.error(f"Error getting random article: {str(e)}")
            return "Error getting random article" 