from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.utils import (
    identify_platform,
    extract_youtube_id,
    extract_instagram_id,
    extract_x_tweet_id,
    extract_facebook_id,
)

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
