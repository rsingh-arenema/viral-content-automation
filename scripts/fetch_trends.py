import os
from dotenv import load_dotenv
import praw
import json
from datetime import datetime

load_dotenv()

def fetch_reddit_trending(subreddit="popular", top_n=5, save_path="data/trending.json"):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )

    topics = []
    for post in reddit.subreddit(subreddit).hot(limit=top_n):
        topics.append(post.title)

    data = {
        "timestamp": datetime.now().isoformat(),
        "source": f"reddit:r/{subreddit}",
        "topics": topics
    }

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"[✔] Fetched {len(topics)} Reddit trending topics: {topics}")
    return topics

# Run test
if __name__ == "__main__":
    fetch_reddit_trending()
