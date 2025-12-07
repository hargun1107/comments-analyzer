import re
from urllib.parse import urlparse, parse_qs
from typing import Optional

# YouTube
YOUTUBE_REGEXS = [
    r"(?:https?://)?(?:www\.)?youtu\.be/(?P<id>[^?&/]+)",
    r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=(?P<id>[^?&/]+)",
    r"(?:https?://)?(?:www\.)?youtube\.com/embed/(?P<id>[^?&/]+)",
    r"(?:https?://)?(?:www\.)?youtube\.com/v/(?P<id>[^?&/]+)"
]

# Instagram (post, reel, tv)
INSTAGRAM_REGEXS = [
    r"(?:https?://)?(?:www\.)?instagram\.com/(?:p|reel|tv)/(?P<id>[^/?&]+)",
]

# X / Twitter
X_REGEXS = [
    r"(?:https?://)?(?:www\.)?twitter\.com/.+/status/(?P<id>\d+)",
    r"(?:https?://)?(?:www\.)?x\.com/.+/status/(?P<id>\d+)"
]

# Facebook
FACEBOOK_REGEXS = [
    r"(?:https?://)?(?:www\.)?facebook\.com/.+/posts/(?P<id>\d+)",
    r"(?:https?://)?(?:www\.)?facebook\.com/permalink\.php\?story_fbid=(?P<id>\d+)",
]

def _match_any(regex_list, url: str) -> Optional[str]:
    for pat in regex_list:
        m = re.search(pat, url)
        if m:
            return m.group("id")
    return None

def extract_youtube_id(url: str) -> Optional[str]:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "v" in qs:
        return qs["v"][0]
    return _match_any(YOUTUBE_REGEXS, url)

def extract_instagram_id(url: str) -> Optional[str]:
    return _match_any(INSTAGRAM_REGEXS, url)

def extract_x_tweet_id(url: str) -> Optional[str]:
    return _match_any(X_REGEXS, url)

def extract_facebook_id(url: str) -> Optional[str]:
    return _match_any(FACEBOOK_REGEXS, url)

def identify_platform(url: str) -> str:
    lower = url.lower()
    if "youtube.com" in lower or "youtu.be" in lower:
        return "youtube"
    if "instagram.com" in lower:
        return "instagram"
    if "twitter.com" in lower or "x.com" in lower:
        return "x"
    if "facebook.com" in lower:
        return "facebook"
    return "unknown"

