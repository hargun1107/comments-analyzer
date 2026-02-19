from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

from app.analyzer import analyze_sentiments, summarize_comments


app = FastAPI(title="Comments Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],          
    allow_headers=["*"],      
)


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

    if platform == "youtube":
        result["id"] = extract_youtube_id(url)
        result["id_type"] = "video_id"
        return result

    if platform == "instagram":
        result["id"] = extract_instagram_id(url)
        result["id_type"] = "shortcode"
        return result

    if platform == "x":
        result["id"] = extract_x_tweet_id(url)
        result["id_type"] = "tweet_id"
        return result

    if platform == "facebook":
        result["id"] = extract_facebook_id(url)
        result["id_type"] = "post_id"
        return result

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
        "comments": comments,
    }


@app.post("/analyze")
def analyze(payload: LinkIn):
    url = payload.url.strip()
    platform = identify_platform(url)

    if platform != "youtube":
        raise HTTPException(status_code=400, detail="Only YouTube analysis supported for now")

    video_id = extract_youtube_id(url)
    comments = fetch_youtube_comments(video_id)
    comment_texts = [c["text"] for c in comments if c.get("text")]
    sentiment = analyze_sentiments(comment_texts)
    summary = summarize_comments(comment_texts)

    return {
        "platform": platform,
        "video_id": video_id,
        "total_comments": len(comments),
        "sentiment_analysis": sentiment,
        "summary": summary,
    }
