# Jarvis Voice Assistant

A Python-based voice assistant that can perform various tasks through voice commands.

## Features

- Voice interaction
- Wikipedia searches
- Weather information
- System controls (volume, brightness)
- Web browser control
- Time information
- Configurable voice settings

## Setup

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. For macOS users, you might need to install portaudio:
   ```bash
   brew install portaudio
   ```

## Configuration

1. Create a `config.json` file (will be created automatically on first run)
2. Add your OpenWeatherMap API key to get weather information
3. Adjust voice settings as needed:
   - voice_index: Index of the voice to use
   - speech_rate: Speed of speech
   - volume: Volume level (0.0 to 1.0)

## Usage

Run the assistant:
```bash
python jarvis.py
```

### Voice Commands

- "Wikipedia [topic]" - Search Wikipedia
- "Weather in [city]" - Get weather information
- "Volume up/down" - Adjust system volume
- "Brightness up/down" - Adjust screen brightness
- "Open [website]" - Open websites (youtube, google, stackoverflow)
- "Time" - Get current time
- "Quit" - Exit the assistant

## Logging

Logs are stored in `jarvis.log` for debugging purposes.

## Contributing

Feel free to submit issues and enhancement requests!
