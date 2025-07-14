# scripts/generate_subtitles.py - Cleaned & Wrapped for Final Subtitles

import whisper
import srt
import os
from datetime import timedelta
import imageio_ffmpeg
from textwrap import fill

def transcribe_to_srt(audio_path="data/voice_bark.wav", output_srt="data/subtitles.srt"):
    print("[...] Transcribing with Whisper...")

    # Get FFmpeg path from imageio_ffmpeg (same as MoviePy uses)
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"[ℹ] Using FFmpeg: {ffmpeg_path}")

    # Ensure Whisper sees the right FFmpeg path
    os.environ['PATH'] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get('PATH', '')

    # Patch Whisper's audio loader to use that path
    import whisper.audio
    original_load_audio = whisper.audio.load_audio

    def patched_load_audio(file, sr=16000):
        import subprocess
        import numpy as np

        cmd = [
            ffmpeg_path,
            "-nostdin", "-threads", "0",
            "-i", file,
            "-f", "s16le", "-ac", "1",
            "-acodec", "pcm_s16le", "-ar", str(sr),
            "-"
        ]

        try:
            out = subprocess.run(cmd, capture_output=True, check=True).stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

    whisper.audio.load_audio = patched_load_audio

    # Load Whisper model and transcribe
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    # Filter and clean up transcript segments
    filtered_segments = []
    for seg in result["segments"]:
        text = seg["text"].strip()

        # Skip unwanted system lines or Bark meta
        if any([
            text.lower().startswith("here's a script"),
            "suitable for" in text.lower(),
            len(text.strip()) < 5
        ]):
            continue

        # Wrap text to 2 lines max (for better visual layout)
        wrapped = fill(text, width=45)
        filtered_segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": wrapped
        })

    # Build final SRT
    subtitles = [
        srt.Subtitle(
            index=i + 1,
            start=timedelta(seconds=seg["start"]),
            end=timedelta(seconds=seg["end"]),
            content=seg["text"]
        )
        for i, seg in enumerate(filtered_segments)
    ]

    srt_output = srt.compose(subtitles)
    os.makedirs(os.path.dirname(output_srt), exist_ok=True)

    with open(output_srt, "w", encoding="utf-8") as f:
        f.write(srt_output)

    print(f"[✔] Subtitles saved: {output_srt}")
    return output_srt

# Test run
if __name__ == "__main__":
    transcribe_to_srt()
