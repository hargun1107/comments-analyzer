import os
import requests
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def fetch_youtube_comments(video_id: str, max_results: int = 500):
    if not YOUTUBE_API_KEY:
        raise ValueError("Missing YOUTUBE_API_KEY")

    url = "https://www.googleapis.com/youtube/v3/commentThreads"

    comments = []
    next_page_token = None

    while len(comments) < max_results:
        params = {
            "part": "snippet,replies",
            "videoId": video_id,
            "maxResults": min(100, max_results - len(comments)),
            "key": YOUTUBE_API_KEY,
        }

        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(url, params=params)

        if response.status_code != 200:
            raise Exception(f"YouTube API Error: {response.text}")

        data = response.json()

        for item in data.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]

            comments.append({
                "author": top_comment.get("authorDisplayName"),
                "text": top_comment.get("textOriginal"),
                "likes": top_comment.get("likeCount", 0),
                "published_at": top_comment.get("publishedAt"),
            })
            replies = item.get("replies", {}).get("comments", [])

            if item["snippet"].get("totalReplyCount", 0) > 0:
                replies = item.get("replies", {}).get("comments", [])
                for reply in replies:
                    reply_snippet = reply["snippet"]
                    comments.append({
                        "author": reply_snippet.get("authorDisplayName"),
                        "text": reply_snippet.get("textOriginal"),
                        "likes": reply_snippet.get("likeCount", 0),
                        "published_at": reply_snippet.get("publishedAt"),
                    })


        next_page_token = data.get("nextPageToken")

        if not next_page_token:
            break

    return comments
