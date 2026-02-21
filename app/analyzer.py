from transformers import pipeline

sentiment_model = pipeline("sentiment-analysis")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


def analyze_sentiments(comments):
    labels = []

    for c in comments:
        text = c.get("text", "")
        if not text:
            continue

        try:
            result = sentiment_model(text[:300])[0]
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
    texts = [c.get("text", "") for c in comments if c.get("text")]

    if not texts:
        return "No valid comments to summarize."

    chunks = []
    current_chunk = ""

    for text in texts:
        if len(current_chunk) + len(text) < 800:
            current_chunk += " " + text
        else:
            chunks.append(current_chunk.strip())
            current_chunk = text

    if current_chunk:
        chunks.append(current_chunk.strip())

    partial_summaries = []

    for chunk in chunks[:3]:  # reduce for stability
        try:
            summary = summarizer(
                chunk,
                max_length=100,
                min_length=30,
                do_sample=False
            )
            partial_summaries.append(summary[0]["summary_text"])
        except:
            continue

    if not partial_summaries:
        return "Could not generate summary."

    final_input = " ".join(partial_summaries)

    try:
        final_summary = summarizer(
            final_input,
            max_length=120,
            min_length=40,
            do_sample=False
        )
        return final_summary[0]["summary_text"]
    except:
        return partial_summaries[0]
