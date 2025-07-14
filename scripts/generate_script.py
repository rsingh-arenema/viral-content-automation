from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
import json
# Force load the correct .env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

# Force correct base_url and key (for Groq)
client = OpenAI(
    base_url=os.getenv("GROQ_API_BASE_URL"),
    api_key=os.getenv("GROQ_API_KEY")
)

print("[debug] GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))

def generate_video_script(topic, save_path="data/script.txt"):
    prompt = (
        f"Write a short 60-90 second viral video script in an informal tone, "
        f"suitable for YouTube Shorts or Reels, about the topic: '{topic}'. "
        f"Make it faceless, engaging, copyright-safe, and interesting to a general audience. "
        f"Avoid any brand names unless used generically. Use short, punchy lines."
    )

    try:
        print(f"[...] Generating script for: {topic}")
        response = client.chat.completions.create(
          model="llama3-70b-8192",
          messages=[{"role": "user", "content": prompt}],
          temperature=0.7,
          max_tokens=500,
    )


        script = response.choices[0].message.content.strip()

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(script)

        print(f"[✔] Script saved to {save_path}")
        return script

    except Exception as e:
        print(f"[✖] Error generating script: {e}")
        return None

# Test run
if __name__ == "__main__":
    with open("data/trending.json", "r", encoding="utf-8") as f:
        trends = json.load(f)["topics"]
    if trends:
        generate_video_script(trends[0])
