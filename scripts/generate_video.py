# scripts/generate_video.py - Fixed duration handling

import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_text_image(text, size, fontsize=60, color=(255, 255, 255)):
    """Create text image using PIL instead of ImageMagick"""
    img = Image.new('RGBA', size, (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", fontsize)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Calculate text position for centering
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = size[1] - text_height - 100  # Position near bottom
    
    draw.text((x, y), text, font=font, fill=color)
    
    return np.array(img)

def generate_video(
    broll_dir="data/pexels/",
    audio_path="data/voice_bark.wav",
    text_path="data/voice_script.txt",
    output_path="uploads/final_video.mp4",
    resolution=(1080, 1920)
):
    print("[...] Building final video...")

    # 1. Load audio first to get its duration
    if not os.path.exists(audio_path):
        print(f"[✖] Voice file not found: {audio_path}")
        return
    
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    print(f"[ℹ] Audio duration: {audio_duration:.2f} seconds")

    # 2. Collect B-roll clips
    clips = []
    total_video_duration = 0
    
    for file in sorted(os.listdir(broll_dir)):
        if file.endswith(".mp4"):
            clip = VideoFileClip(os.path.join(broll_dir, file)).resize(resolution)
            
            # Determine how much of this clip to use
            remaining_duration = audio_duration - total_video_duration
            if remaining_duration <= 0:
                break  # We have enough video
            
            clip_duration = min(5, remaining_duration, clip.duration)  # Max 5 seconds per clip
            clip = clip.subclip(0, clip_duration)
            clips.append(clip)
            total_video_duration += clip_duration
            
            print(f"[ℹ] Added clip: {file} ({clip_duration:.2f}s)")

    if not clips:
        print("[✖] No video clips found in", broll_dir)
        return

    # 3. Create final video
    final_video = concatenate_videoclips(clips)
    video_duration = final_video.duration
    print(f"[ℹ] Video duration: {video_duration:.2f} seconds")

    # 4. Handle duration mismatch
    if video_duration < audio_duration:
        print(f"[!] Video shorter than audio. Looping video to match audio duration.")
        # Loop the video to match audio duration
        loop_count = int(audio_duration / video_duration) + 1
        final_video = concatenate_videoclips([final_video] * loop_count).subclip(0, audio_duration)
    elif video_duration > audio_duration:
        print(f"[!] Video longer than audio. Trimming video to match audio duration.")
        # Trim video to match audio duration
        final_video = final_video.subclip(0, audio_duration)

    # 5. Set audio (now durations should match)
    final_video = final_video.set_audio(audio)
    print(f"[ℹ] Final duration: {final_video.duration:.2f} seconds")

    # 6. Add text overlay using PIL (optional)
    if os.path.exists(text_path):
        with open(text_path, "r", encoding="utf-8") as f:
            subtitle = f.read().strip()

        print("[...] Creating text overlay with PIL...")
        from moviepy.editor import ImageClip
        text_img = create_text_image(subtitle, resolution)
        txt_clip = ImageClip(text_img, ismask=False).set_duration(final_video.duration)
        
        final_video = CompositeVideoClip([final_video, txt_clip])

    # 7. Save final output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    final_video.write_videofile(output_path, fps=24)
    print(f"[✔] Final video saved: {output_path}")

# Run directly
if __name__ == "__main__":
    generate_video()