# hush

Local speech-to-text with hotkey control. Speak, transcribe, paste.

## Tools

- [Whisper](https://github.com/openai/whisper) - OpenAI's speech recognition
- [pynput](https://github.com/moses-palmer/pynput) - Keyboard/mouse control
- [sounddevice](https://python-sounddevice.readthedocs.io/) - Audio recording
- [pyperclip](https://github.com/asweigart/pyperclip) - Clipboard access

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/hush.git
cd hush
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install openai-whisper pynput sounddevice scipy numpy pyperclip
```

FFmpeg is required:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (winget)
winget install ffmpeg
```

## Usage

```bash
# English transcription
python main.py

# Russian/English → English translation
python main_russian.py
```

**Hotkeys:**
- `Shift+F10` - Start/stop recording
- After recording stops, text is copied to clipboard and pasted automatically

## Models

Change `MODEL_NAME` in the script:

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 75MB | Fastest | Basic |
| base | 150MB | Fast | OK |
| small | 500MB | Medium | Good |
| medium | 1.5GB | Slow | Great |
| large | 3GB | Slowest | Best |

## License

MIT
