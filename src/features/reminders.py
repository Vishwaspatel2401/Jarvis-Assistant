import json
import logging
from datetime import datetime
from typing import List, Dict
from src.utils.config_manager import ConfigManager

class ReminderManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.reminders_file = "reminders.json"
        self.reminders = self.load_reminders()

    def load_reminders(self) -> List[Dict]:
        """Load reminders from file"""
        try:
            with open(self.reminders_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_reminders(self):
        """Save reminders to file"""
        try:
            with open(self.reminders_file, 'w') as f:
                json.dump(self.reminders, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving reminders: {str(e)}")

    def add_reminder(self, text: str, time: str) -> bool:
        """Add a new reminder"""
        try:
            reminder = {
                "text": text,
                "time": time,
                "created": datetime.now().isoformat()
            }
            self.reminders.append(reminder)
            self.save_reminders()
            return True
        except Exception as e:
            logging.error(f"Error adding reminder: {str(e)}")
            return False

    def get_reminders(self) -> List[Dict]:
        """Get all reminders"""
        return self.reminders

    def delete_reminder(self, index: int) -> bool:
        """Delete a reminder by index"""
        try:
            if 0 <= index < len(self.reminders):
                self.reminders.pop(index)
                self.save_reminders()
                return True
            return False
        except Exception as e:
            logging.error(f"Error deleting reminder: {str(e)}")
            return False 