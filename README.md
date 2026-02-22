YouTube Comments Analyzer

A full-stack web application that fetches YouTube comments and performs AI-powered sentiment analysis and summarization using Transformer models.

Overview

This project allows users to:

Paste a YouTube video link, Fetch up to 500 comments (including replies), Analyze sentiment distribution (Positive / Negative / Neutral), Generate an AI summary of the overall discussion

The system uses pretrained Transformer models for Natural Language Processing and a FastAPI backend to handle comment extraction and analysis.

Tech Stack

Frontend:
1. React.js
2. Axios
3. CSS

Backend:
1. Python
2. FastAPI
3. Uvicorn
4. Requests
5. python-dotenv

Machine Learning:
1. HuggingFace Transformers
2. DistilBERT (Sentiment Analysis)
3. BART or T5 (Text Summarization)

Machine Learning Models Used

Sentiment Analysis
Model: 
1. distilbert-base-uncased-finetuned-sst-2-english
2. Transformer-based model
3. Fine-tuned on the SST-2 dataset
4. Classifies text as POSITIVE or NEGATIVE

Neutral percentage is derived from non-positive and non-negative predictions.

Text Summarization
Model: 
1. facebook/bart-large-cnn (or a lighter alternative such as T5-small)
2. Transformer-based abstractive summarization model
3. Generates a concise summary from multiple comments

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

1. Fetches up to 500 comments
2. Includes replies in comment count
3. Real-time sentiment analysis
4. AI-powered comment summarization
5. Clean responsive UI
6. Error handling and loading states

Limitations

1. Only YouTube is currently supported
2. YouTube API quota limits apply
3. Transformer models increase startup time
4. Sentiment model only predicts Positive or Negative (Neutral derived)