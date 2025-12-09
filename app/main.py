from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()

from app.utils import (
    identify_platform,
    extract_youtube_id,
    extract_instagram_id,
    extract_x_tweet_id,
    extract_facebook_id,
)

from app.youtube_fetcher import fetch_youtube_comments

app = FastAPI(title="Comments Analyzer API")

class LinkIn(BaseModel):
    url: str

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/parse-link")
def parse_link(payload: LinkIn):
    url = payload.url.strip()
    platform = identify_platform(url)

    result = {"platform": platform, "url": url}

    # YouTube
    if platform == "youtube":
        result["id"] = extract_youtube_id(url)
        result["id_type"] = "video_id"
        return result

    # Instagram
    if platform == "instagram":
        result["id"] = extract_instagram_id(url)
        result["id_type"] = "shortcode"
        return result

    # Twitter/X
    if platform == "x":
        result["id"] = extract_x_tweet_id(url)
        result["id_type"] = "tweet_id"
        return result

    # Facebook
    if platform == "facebook":
        result["id"] = extract_facebook_id(url)
        result["id_type"] = "post_id"
        return result

    # Unknown / unsupported
    result["id"] = None
    return result

@app.post("/fetch-comments")
def fetch_comments(payload: LinkIn):
    url = payload.url.strip()
    platform = identify_platform(url)

    if platform != "youtube":
        raise HTTPException(status_code=400, detail="Only YouTube supported for now")

    video_id = extract_youtube_id(url)
    comments = fetch_youtube_comments(video_id)

    return {
        "platform": platform,
        "video_id": video_id,
        "total_comments": len(comments),
        "comments": comments
    }

