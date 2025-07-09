import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from src.utils.config_manager import ConfigManager

class EmailService:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send an email"""
        try:
            email = self.config.get('email')
            password = self.config.get('email_password')
            
            if not email or not password:
                logging.error("Email credentials not configured")
                return False

            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(email, password)
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            return False

    def send_bulk_email(self, to_emails: List[str], subject: str, body: str) -> bool:
        """Send email to multiple recipients"""
        success = True
        for email in to_emails:
            if not self.send_email(email, subject, body):
                success = False
        return success

    def handle_email_command(self, command: str, speech_engine) -> None:
        """Handle email-related voice commands"""
        try:
            if "send email" in command:
                # Extract email components from command
                parts = command.split("to")
                if len(parts) != 2:
                    speech_engine.speak("Please specify the recipient email address")
                    return

                recipient = parts[1].strip()
                if "@" not in recipient:
                    speech_engine.speak("Please provide a valid email address")
                    return

                speech_engine.speak("What should be the subject of the email?")
                subject = input("Subject: ")

                speech_engine.speak("What message would you like to send?")
                body = input("Message: ")

                if self.send_email(recipient, subject, body):
                    speech_engine.speak("Email sent successfully")
                else:
                    speech_engine.speak("Failed to send email. Please check your email configuration")

        except Exception as e:
            logging.error(f"Error handling email command: {str(e)}")
            speech_engine.speak("Error processing email command") 