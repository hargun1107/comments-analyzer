import os
import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def fetch_youtube_comments(video_id: str, max_results: int = 50):

    if not YOUTUBE_API_KEY:
        raise ValueError("Missing YOUTUBE_API_KEY in environment")

    url = "https://www.googleapis.com/youtube/v3/commentThreads"

    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(url, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(f"YouTube API Error (status {response.status_code}): {response.text}")

    data = response.json()

    comments = []
    for item in data.get("items", []):
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "author": snippet.get("authorDisplayName"),
            "text": snippet.get("textOriginal"),
            "likes": snippet.get("likeCount", 0),
            "published_at": snippet.get("publishedAt"),
        })

    return comments
