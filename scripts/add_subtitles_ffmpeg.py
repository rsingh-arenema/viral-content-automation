# scripts/add_subtitles_ffmpeg.py - Fixed to use MoviePy's FFmpeg

import os
import subprocess
import imageio_ffmpeg

def add_subtitles_ffmpeg(input_video="uploads/final_video.mp4",
                         subtitle_file="data/subtitles.srt",
                         output_video="uploads/final_video_subtitled.mp4"):
    if not os.path.exists(input_video):
        print("[✖] Input video not found.")
        return
    if not os.path.exists(subtitle_file):
        print("[✖] Subtitles file not found.")
        return

    # Get the same FFmpeg that MoviePy uses
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    print(f"[ℹ] Using FFmpeg: {ffmpeg_exe}")

    # Fix subtitle file path for Windows (use forward slashes)
    subtitle_file_fixed = subtitle_file.replace("\\", "/")

    cmd = [
        ffmpeg_exe,  # Use full path instead of just "ffmpeg"
        "-y",
        "-i", input_video,
        "-vf", f"subtitles={subtitle_file_fixed}",
        "-c:a", "copy",
        output_video
    ]

    print(f"[...] Adding subtitles to video...")
    try:
        subprocess.run(cmd, check=True)
        print(f"[✔] Subtitled video saved: {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"[✖] FFmpeg error: {e}")

# Run directly
if __name__ == "__main__":
    add_subtitles_ffmpeg()