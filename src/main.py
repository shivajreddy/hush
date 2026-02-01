import pyperclip
from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button as MouseButton, Controller as MouseCountroller
import sys
import time
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write as write_wav
from pathlib import Path

SAMPLE_RATE = 16000  # Whisper expects 16kHz audio

# Determine base directory (next to executable if bundled, or project root if running from source)
if getattr(sys, "frozen", False):
    # Running as PyInstaller bundle - use directory containing the executable
    BASE_DIR = Path(sys.executable).parent
else:
    # Running from source - use project root (parent of src/)
    BASE_DIR = Path(__file__).parent.parent

OUTPUT_DIR = BASE_DIR / "recordings"
OUTPUT_FILE = OUTPUT_DIR / "latest_record.wav"
KEYMAP_FILE = BASE_DIR / "keymaps.txt"
VALID_MODELS = ["tiny", "base", "small", "medium", "large"]

# Mapping of string names to pynput Key objects
KEY_MAP = {
    "f1": Key.f1, "f2": Key.f2, "f3": Key.f3, "f4": Key.f4,
    "f5": Key.f5, "f6": Key.f6, "f7": Key.f7, "f8": Key.f8,
    "f9": Key.f9, "f10": Key.f10, "f11": Key.f11, "f12": Key.f12,
    "shift": "shift", "ctrl": "ctrl", "alt": "alt",
}


def parse_keymap(keymap_str):
    """Parse a keymap string like 'shift+f10' or 'f7' into modifiers and key."""
    parts = keymap_str.lower().strip().split("+")
    modifiers = set()
    trigger_key = None

    for part in parts:
        part = part.strip()
        if part in ("shift", "ctrl", "alt"):
            modifiers.add(part)
        elif part in KEY_MAP:
            trigger_key = KEY_MAP[part]

    return modifiers, trigger_key


def load_keymap():
    """Load keymap from file, returns (modifiers, trigger_key)."""
    default_modifiers = {"shift"}
    default_key = Key.f10

    if not KEYMAP_FILE.exists():
        return default_modifiers, default_key

    try:
        keymap_str = KEYMAP_FILE.read_text().strip().split("\n")[0]
        modifiers, trigger_key = parse_keymap(keymap_str)
        if trigger_key is None:
            print(f"Invalid keymap '{keymap_str}', using default shift+f10")
            return default_modifiers, default_key
        return modifiers, trigger_key
    except Exception as e:
        print(f"Error reading keymap file: {e}, using default shift+f10")
        return default_modifiers, default_key


class SpeechToText:
    def __init__(self, model_name="base"):
        self.recording = False
        self.start_time = None
        self.audio_data = []
        self.stream = None
        self.mouse_controller = MouseCountroller()
        self.keyboard_controller = KeyboardController()

        # Load keymap configuration
        self.modifiers, self.trigger_key = load_keymap()
        self.modifier_states = {"shift": False, "ctrl": False, "alt": False}

        # Ensure output directory exists
        OUTPUT_DIR.mkdir(exist_ok=True)

        # Load Whisper model once at startup
        print(f"Loading Whisper '{model_name}' model...")
        self.model = whisper.load_model(model_name)
        print("Model loaded. Ready!")

    def audio_callback(self, indata, frames, time_info, status):
        if self.recording:
            self.audio_data.append(indata.copy())

    def start_recording(self):
        self.audio_data = []
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE, channels=1, callback=self.audio_callback
        )
        self.stream.start()
        self.start_time = time.time()
        print("Recording started...")

    def stop_recording(self):
        self.stream.stop()
        self.stream.close()

        duration = time.time() - self.start_time

        if self.audio_data:
            audio = np.concatenate(self.audio_data, axis=0)
            write_wav(OUTPUT_FILE, SAMPLE_RATE, audio)
            print(f"Recording stopped. Duration: {duration:.2f}s")
            self.transcribe(duration)
        else:
            print("No audio recorded.")

    def transcribe(self, duration):
        print("Transcribing...")
        result = self.model.transcribe(str(OUTPUT_FILE))
        text = result["text"].strip()

        # Calculate words per minute
        word_count = len(text.split())
        wpm = (word_count / duration) * 60 if duration > 0 else 0

        # print("\n--- Transcription ---")
        # print(text)
        # print("---------------------")
        # print(f"Words: {word_count} | Duration: {duration:.1f}s | WPM: {wpm:.0f}\n")

        pyperclip.copy(text)
        print("Copied to clipboard")
        print(f"WPM: {wpm:.0f}")
        # print("Simulating mouse middle click")
        # self.simulate_mouse_middleclick()
        print("Simulating ctrl+shift+v")
        self.simulate_ctrl_shift_v()
        print("---------------------")

    def simulate_mouse_middleclick(self):
        # small delay
        time.sleep(0.5)
        # press & release mouse middle button
        self.mouse_controller.press(MouseButton.middle)
        self.mouse_controller.release(MouseButton.middle)

    def simulate_ctrl_shift_v(self):
        time.sleep(0.2)
        # press ctrl+shift+v
        kb = self.keyboard_controller
        with kb.pressed(Key.ctrl):
            with kb.pressed(Key.shift):
                kb.press("v")
                kb.release("v")

    def on_key_press(self, key):
        # Track modifier states
        if key == Key.shift_l or key == Key.shift_r:
            self.modifier_states["shift"] = True
        if key == Key.ctrl_l or key == Key.ctrl_r:
            self.modifier_states["ctrl"] = True
        if key == Key.alt_l or key == Key.alt_r:
            self.modifier_states["alt"] = True

        # Check if trigger key is pressed with required modifiers
        if key == self.trigger_key:
            modifiers_match = all(
                self.modifier_states[mod] for mod in self.modifiers
            )
            if modifiers_match:
                if not self.recording:
                    self.recording = True
                    self.start_recording()
                else:
                    self.recording = False
                    self.stop_recording()

    def on_key_release(self, key):
        if key == Key.shift_l or key == Key.shift_r:
            self.modifier_states["shift"] = False
        if key == Key.ctrl_l or key == Key.ctrl_r:
            self.modifier_states["ctrl"] = False
        if key == Key.alt_l or key == Key.alt_r:
            self.modifier_states["alt"] = False

    def run(self):
        # Build hotkey display string
        hotkey_parts = list(self.modifiers) + [self.trigger_key.name.upper()]
        hotkey_str = "+".join(part.capitalize() for part in hotkey_parts)

        print("\nHotkeys:")
        print(f"  {hotkey_str} - Start/stop recording")
        print("\nPress Ctrl+C to exit.\n")

        with keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release
        ) as listener:
            listener.join()


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "base"

    if model_name not in VALID_MODELS:
        print(f"Invalid model: {model_name}")
        print(f"Valid options: {', '.join(VALID_MODELS)}")
        sys.exit(1)

    app = SpeechToText(model_name)
    app.run()
