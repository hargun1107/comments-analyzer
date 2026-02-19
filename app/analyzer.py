from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def analyze_sentiments(comment_texts):
    labels = []

    for text in comment_texts:
        if not text:
            continue

        try:
            result = sentiment_model(text[:500])[0]
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


def summarize_comments(comment_texts):
    text = " ".join(comment_texts)

    if len(text) < 50:
        return "Not enough content to summarize."

    text = text[:1000]

    summary = summarizer(
        text,
        max_length=120,
        min_length=40,
        do_sample=False
    )

    return summary[0]["summary_text"]
