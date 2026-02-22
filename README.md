YouTube Comments Analyzer

A full-stack web application that fetches YouTube comments and performs AI-powered sentiment analysis and summarization using Transformer models.

Overview

This project allows users to:

Paste a YouTube video link
Fetch up to 500 comments (including replies)
Analyze sentiment distribution (Positive / Negative / Neutral)
Generate an AI summary of the overall discussion

The system uses pretrained Transformer models for Natural Language Processing and a FastAPI backend to handle comment extraction and analysis.

Tech Stack

Frontend:
React.js
Axios
CSS

Backend:
Python
FastAPI
Uvicorn
Requests
python-dotenv

Machine Learning:
HuggingFace Transformers
DistilBERT (Sentiment Analysis)
BART or T5 (Text Summarization)

Machine Learning Models Used

Sentiment Analysis
Model: distilbert-base-uncased-finetuned-sst-2-english
Transformer-based model
Fine-tuned on the SST-2 dataset
Classifies text as POSITIVE or NEGATIVE

Neutral percentage is derived from non-positive and non-negative predictions.

Text Summarization
Model: facebook/bart-large-cnn (or a lighter alternative such as T5-small)
Transformer-based abstractive summarization model
Generates a concise summary from multiple comments

Note: Models are pretrained and used for inference only. No model training or fine-tuning is performed in this project.

How It Works

1. The user enters a YouTube link in the frontend.
2. The backend extracts the video ID.
3. The YouTube Data API fetches comment threads and replies.
4. The comments are processed by:
A sentiment analysis model
A summarization model
5. The backend returns structured JSON.
6. The frontend displays:
Total comment count
Sentiment breakdown
AI-generated summary

Features

Fetches up to 500 comments
Includes replies in comment count
Real-time sentiment analysis
AI-powered comment summarization
Clean responsive UI
Error handling and loading states

Limitations

Only YouTube is currently supported
YouTube API quota limits apply
Transformer models increase startup time
Sentiment model only predicts Positive or Negative (Neutral derived)