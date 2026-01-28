import pyperclip
from pynput import keyboard
from pynput.keyboard import Key, Controller as KeyboardController
from pynput.mouse import Button as MouseButton, Controller as MouseCountroller
import time
import whisper
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write as write_wav
from pathlib import Path

SAMPLE_RATE = 16000  # Whisper expects 16kHz audio
OUTPUT_DIR = Path(__file__).parent.parent / "recordings"
OUTPUT_FILE = OUTPUT_DIR / "latest_record.wav"
# Available options in order "tiny", "base", small", "medium", or "large" as needed
MODEL_NAME = "small"


class SpeechToText:
    def __init__(self):
        self.recording = False
        self.start_time = None
        self.audio_data = []
        self.stream = None
        self.mouse_controller = MouseCountroller()
        self.keyboard_controller = KeyboardController()
        self.shift_pressed = False

        # Ensure output directory exists
        OUTPUT_DIR.mkdir(exist_ok=True)

        # Load Whisper model once at startup
        print(f"Loading Whisper '{MODEL_NAME}' model...")
        self.model = whisper.load_model(MODEL_NAME)
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
        if key == Key.shift_l or key == Key.shift_r:
            self.shift_pressed = True

        if key == Key.f10 and self.shift_pressed:
            if not self.recording:
                self.recording = True
                self.start_recording()
            else:
                self.recording = False
                self.stop_recording()

    def on_key_release(self, key):
        if key == Key.shift_l or key == Key.shift_r:
            self.shift_pressed = False

    def run(self):
        print("\nHotkeys:")
        print("  Shift+F10 - Start/stop recording")
        print("\nPress Ctrl+C to exit.\n")

        with keyboard.Listener(
            on_press=self.on_key_press, on_release=self.on_key_release
        ) as listener:
            listener.join()


if __name__ == "__main__":
    app = SpeechToText()
    app.run()
