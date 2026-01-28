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
pip install -r requirements.txt
```

FFmpeg is required:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Windows (winget)
winget install ffmpeg
```

## Usage

### Run from source

```bash
# English transcription (default: base model)
python src/main.py

# Specify model size
python src/main.py small

# Russian/English → English translation
python src/main_russian.py
python src/main_russian.py medium
```

### Run as binary

```bash
# Default (base model)
./build/hush.exe

# With model argument
./build/hush.exe small
```

**Hotkeys:**
- `Shift+F10` - Start/stop recording
- After recording stops, text is copied to clipboard and pasted automatically

## Build

```bash
pyinstaller --onefile src/main.py --name hush --distpath build --workpath .pyinstaller --add-data "venv/Lib/site-packages/whisper/assets;whisper/assets"
```

Output: `build/hush.exe`

## Models

Pass as argument: `hush.exe small` or `python src/main.py small` (default: `base`)

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 75MB | Fastest | Basic |
| base | 150MB | Fast | OK |
| small | 500MB | Medium | Good |
| medium | 1.5GB | Slow | Great |
| large | 3GB | Slowest | Best |

## License

MIT
