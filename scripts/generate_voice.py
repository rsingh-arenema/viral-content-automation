# scripts/generate_voice.py

from gtts import gTTS
import os
import re

def generate_voice_from_script(script_path="data/voice_script.txt", output_path="data/voice.mp3", lang="en"):
    if not os.path.exists(script_path):
        print(f"[✖] Script not found at {script_path}")
        return

    with open(script_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        line = line.strip()
        # Skip direction lines like (Cut to...), timestamps, or narrator tags
        if (
            line.startswith("(") or
            line.startswith("**[") or
            "Narrator" in line or
            line.lower().startswith("here's a script")
        ):
            continue
        if line:
            cleaned_lines.append(line)

    text = " ".join(cleaned_lines)

    if not text.strip():
        print("[✖] Script is empty after cleaning")
        return

    print(f"[...] Generating voice for {len(text.split())} words...")

    tts = gTTS(text=text, lang=lang, slow=False)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tts.save(output_path)

    print(f"[✔] Voice saved to {output_path}")

# For testing
if __name__ == "__main__":
    generate_voice_from_script()
