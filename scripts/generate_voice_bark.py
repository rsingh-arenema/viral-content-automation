# scripts/generate_voice_bark.py — Split input & stitch segments

from bark import generate_audio, SAMPLE_RATE
import os
import scipy.io.wavfile
import numpy as np
from textwrap import wrap

def split_text_into_chunks(text, max_length=180):
    # Break into sentence-like chunks
    chunks = wrap(text, width=max_length, break_long_words=False, break_on_hyphens=False)
    return chunks

def generate_bark_voice(input_script="data/voice_script.txt", output_path="data/voice_bark.wav"):
    if not os.path.exists(input_script):
        print("[✖] Script not found.")
        return

    with open(input_script, "r", encoding="utf-8") as f:
        full_text = f.read().replace('"', ' ').replace("\n", " ").strip()

    chunks = split_text_into_chunks(full_text)
    print(f"[ℹ] Splitting into {len(chunks)} Bark chunks...")

    audio_segments = []
    import time

    for i, chunk in enumerate(chunks):
        print(f"[{i+1}/{len(chunks)}] Generating chunk: {chunk[:40]}...")
        start = time.time()
        audio_array = generate_audio(chunk)
        duration = time.time() - start
        print(f"[✔] Chunk {i+1} done in {duration:.1f}s")
        audio_segments.append(audio_array)


    # Concatenate all audio segments
    full_audio = np.concatenate(audio_segments)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    scipy.io.wavfile.write(output_path, rate=SAMPLE_RATE, data=full_audio)
    print(f"[✔] Full voice saved: {output_path}")

# Test run
if __name__ == "__main__":
    generate_bark_voice()
