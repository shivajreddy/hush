# hush

Local speech-to-text with hotkey control. Speak, transcribe, paste.

## Tools

- [Whisper](https://github.com/openai/whisper) - OpenAI's speech recognition
- [pynput](https://github.com/moses-palmer/pynput) - Keyboard/mouse control
- [sounddevice](https://python-sounddevice.readthedocs.io/) - Audio recording
- [pyperclip](https://github.com/asweigart/pyperclip) - Clipboard access

## Setup

```bash
git clone https://github.com/shivajreddy/hush.git
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
winget install --id Gyan.FFmpeg.Essentials -e --source winget
```

## Build

```bash
pyinstaller --onefile src/main.py --name hush --distpath build --workpath .pyinstaller --add-data "venv/Lib/site-packages/whisper/assets;whisper/assets"
```

Output: `build/hush.exe`

## Usage

```bash
hush.exe [model]
```

| Command | Description |
|---------|-------------|
| `hush.exe` | Run with default model (base) |
| `hush.exe tiny` | Fastest, lower accuracy |
| `hush.exe base` | Default, balanced |
| `hush.exe small` | Good accuracy, recommended for non-English |
| `hush.exe medium` | Great accuracy, slower |
| `hush.exe large` | Best accuracy, slowest |

**Hotkeys:**
- `Shift+F10` - Start/stop recording (default)
- After recording stops, text is copied to clipboard and pasted automatically

**Custom Hotkey:**

Create a `keymaps.txt` file next to the executable (or in the project root when running from source) with your preferred hotkey:

```
f7
```

Supported formats:
- `f7` - Single key (F1-F12)
- `shift+f10` - Shift + key
- `ctrl+f5` - Ctrl + key
- `alt+f1` - Alt + key
- `ctrl+shift+f12` - Multiple modifiers

### Run from source

```bash
# English transcription
python src/main.py
python src/main.py small

# Russian/English → English translation
python src/main_russian.py
python src/main_russian.py medium
```

## Models

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| tiny | 75MB | Fastest | Basic |
| base | 150MB | Fast | OK |
| small | 500MB | Medium | Good |
| medium | 1.5GB | Slow | Great |
| large | 3GB | Slowest | Best |

## License

MIT
