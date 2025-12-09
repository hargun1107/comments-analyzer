from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables (.env)
load_dotenv()

# Import utilities
from app.utils import (
    identify_platform,
    extract_youtube_id,
    extract_instagram_id,
    extract_x_tweet_id,
    extract_facebook_id,
)

# YouTube comment fetcher
from app.youtube_fetcher import fetch_youtube_comments

# Sentiment + summarization
from app.analyzer import analyze_sentiments, summarize_comments


app = FastAPI(title="Comments Analyzer API")


# Model for input request
class LinkIn(BaseModel):
    url: str


@app.get("/")
def root():
    return {"message": "API is running"}


# ---------------------------
#  LINK PARSING ENDPOINT
# ---------------------------
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

    # Twitter / X
    if platform == "x":
        result["id"] = extract_x_tweet_id(url)
        result["id_type"] = "tweet_id"
        return result

    # Facebook
    if platform == "facebook":
        result["id"] = extract_facebook_id(url)
        result["id_type"] = "post_id"
        return result

    # Unknown platform
    result["id"] = None
    return result


# ---------------------------
#  FETCH YOUTUBE COMMENTS
# ---------------------------
@app.post("/fetch-comments")
def fetch_comments(payload: LinkIn):
    url = payload.url.strip()
    platform = identify_platform(url)

    if platform != "youtube":
        raise HTTPException(status_code=400, detail="Only YouTube supported for now")

    video_id = extract_youtube_id(url)

    # Fetch raw comments
    comments = fetch_youtube_comments(video_id)

    return {
        "platform": platform,
        "video_id": video_id,
        "total_comments": len(comments),
        "comments": comments,
    }


# ---------------------------
#  FULL ANALYSIS ENDPOINT
# ---------------------------
@app.post("/analyze")
def analyze(payload: LinkIn):
    url = payload.url.strip()
    platform = identify_platform(url)

    if platform != "youtube":
        raise HTTPException(status_code=400, detail="Only YouTube analysis supported for now")

    video_id = extract_youtube_id(url)
    comments = fetch_youtube_comments(video_id)

    # Sentiment stats
    sentiment = analyze_sentiments(comments)

    # Summary of all comments
    summary = summarize_comments(comments)

    return {
        "platform": platform,
        "video_id": video_id,
        "total_comments": len(comments),
        "sentiment_analysis": sentiment,
        "summary": summary,
    }
