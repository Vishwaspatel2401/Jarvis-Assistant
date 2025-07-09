import os
import platform
import logging
import webbrowser
from typing import Optional
from src.utils.config_manager import ConfigManager

class SystemController:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.system = platform.system().lower()

    def control_system(self, command: str) -> bool:
        """Control system settings like volume and brightness"""
        try:
            if "volume" in command:
                if "up" in command or "increase" in command:
                    if self.system == "darwin":  # macOS
                        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 10)'")
                    elif self.system == "windows":
                        os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys([char]175)")
                elif "down" in command or "decrease" in command:
                    if self.system == "darwin":
                        os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 10)'")
                    elif self.system == "windows":
                        os.system("powershell -c (New-Object -ComObject WScript.Shell).SendKeys([char]174)")
            
            elif "brightness" in command:
                if self.system == "darwin":
                    if "up" in command or "increase" in command:
                        os.system("brightness 0.1")
                    elif "down" in command or "decrease" in command:
                        os.system("brightness -0.1")
                elif self.system == "windows":
                    # Windows brightness control requires additional setup
                    logging.warning("Brightness control not implemented for Windows")
                    return False
            
            return True
        except Exception as e:
            logging.error(f"Error controlling system: {str(e)}")
            return False

    def open_website(self, command: str) -> bool:
        """Open a website in the default browser"""
        try:
            # Extract website name from command
            if "open" in command:
                website = command.split("open")[-1].strip()
                if "wikipedia" in website:
                    webbrowser.open("https://www.wikipedia.org")
                elif "google" in website:
                    webbrowser.open("https://www.google.com")
                elif "youtube" in website:
                    webbrowser.open("https://www.youtube.com")
                else:
                    # Try to open as a direct URL
                    if not website.startswith(('http://', 'https://')):
                        website = 'https://' + website
                    webbrowser.open(website)
                return True
            return False
        except Exception as e:
            logging.error(f"Error opening website: {str(e)}")
            return False

    def shutdown(self) -> bool:
        """Shutdown the system"""
        try:
            if self.system == "windows":
                os.system("shutdown /s /t 1")
            else:
                os.system("shutdown -h now")
            return True
        except Exception as e:
            logging.error(f"Error shutting down system: {str(e)}")
            return False

    def restart(self) -> bool:
        """Restart the system"""
        try:
            if self.system == "windows":
                os.system("shutdown /r /t 1")
            else:
                os.system("shutdown -r now")
            return True
        except Exception as e:
            logging.error(f"Error restarting system: {str(e)}")
            return False

    def sleep(self) -> bool:
        """Put system to sleep"""
        try:
            if self.system == "windows":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            else:
                os.system("pmset sleepnow")
            return True
        except Exception as e:
            logging.error(f"Error putting system to sleep: {str(e)}")
            return False

    def get_system_info(self) -> str:
        """Get system information"""
        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        return f"System: {info['system']} {info['release']}\nProcessor: {info['processor']}\nMachine: {info['machine']}" 