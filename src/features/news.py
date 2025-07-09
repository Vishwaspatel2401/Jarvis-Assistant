import requests
import logging
import wikipedia
from typing import List
from src.utils.config_manager import ConfigManager

class NewsService:
    def __init__(self, config: ConfigManager):
        self.config = config
        wikipedia.set_lang("en")

    def get_news(self, category: str = "general") -> str:
        """Get news headlines for a category"""
        api_key = self.config.get('news_api_key')
        if not api_key:
            return "News API key not configured"
        
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                articles = data.get('articles', [])
                headlines = [article['title'] for article in articles[:5]]
                return "Here are the latest headlines: " + ". ".join(headlines)
            return "Could not fetch news"
        except Exception as e:
            logging.error(f"News API error: {str(e)}")
            return "Error fetching news"

    def search_wikipedia(self, query: str, sentences: int = 2) -> str:
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