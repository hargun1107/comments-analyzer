from transformers import pipeline

# Load sentiment model once
sentiment_model = pipeline("sentiment-analysis")

# Summarizer model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def analyze_sentiments(comments):
    labels = []

    for c in comments:
        text = c.get("text", "")
        if not text:
            continue

        try:
            result = sentiment_model(text[:500])[0]  # limit length
            labels.append(result["label"])
        except:
            labels.append("NEUTRAL")

    total = len(labels)
    pos = labels.count("POSITIVE")
    neg = labels.count("NEGATIVE")
    neu = total - pos - neg

    return {
        "summary": "Sentiment stats for YouTube comments",
        "total": total,
        "positive": round(pos / total * 100, 2) if total else 0,
        "negative": round(neg / total * 100, 2) if total else 0,
        "neutral": round(neu / total * 100, 2) if total else 0,
    }


def summarize_comments(comments):
    text = " ".join(c.get("text", "") for c in comments)

    if len(text) < 50:
        return "Not enough content to summarize."

    text = text[:1000]  # keep within model limits

    summary = summarizer(
        text,
        max_length=120,
        min_length=40,
        do_sample=False
    )

    return summary[0]["summary_text"]
