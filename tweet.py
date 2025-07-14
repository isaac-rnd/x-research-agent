import os
import sys
import logging

import feedparser
import tweepy
from transformers import pipeline

# ---- Configuration ----
RSS_FEED_URL = "http://export.arxiv.org/rss/cs.AI"  # You can change this to any public RSS feed

MAX_TWEET_LENGTH = 280

# Optional: Limit number of articles to process each run
MAX_POSTS = 1

# ---- Logging setup ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def fetch_latest_entries(feed_url, limit=1):
    """
    Fetch latest entries from RSS feed.
    """
    logging.info(f"Fetching RSS feed: {feed_url}")
    feed = feedparser.parse(feed_url)
    entries = feed.entries[:limit]
    logging.info(f"Found {len(entries)} entries")
    return entries

def summarize_text(text, model_name="sshleifer/distilbart-cnn-12-6"):
    """
    Summarize the provided text using a HuggingFace model.
    """
    logging.info("Loading summarization pipeline")
    summarizer = pipeline("summarization", model=model_name)
    logging.info("Running summarization")
    summary = summarizer(text, max_length=60, min_length=20, do_sample=False)[0]['summary_text']
    return summary.strip()

def format_tweet(title, summary, link):
    """
    Format the tweet: Title + TL;DR + link, ensuring <=280 chars.
    """
    base = f"{title}\nTL;DR: {summary}\n{link}"
    if len(base) <= MAX_TWEET_LENGTH:
        return base
    # If too long, truncate summary
    allowed_summary_len = MAX_TWEET_LENGTH - len(title) - len(link) - len("TL;DR: \n\n")
    truncated_summary = summary[:allowed_summary_len - 3].rstrip() + "..."
    tweet = f"{title}\nTL;DR: {truncated_summary}\n{link}"
    if len(tweet) > MAX_TWEET_LENGTH:
        # As last resort, truncate title too
        allowed_title_len = MAX_TWEET_LENGTH - len(truncated_summary) - len(link) - len("TL;DR: \n\n")
        title = title[:allowed_title_len - 3].rstrip() + "..."
        tweet = f"{title}\nTL;DR: {truncated_summary}\n{link}"
    return tweet[:MAX_TWEET_LENGTH]

def post_to_twitter(tweet_text):
    """
    Post the tweet using Tweepy and Twitter API keys from environment.
    """
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_secret = os.environ.get("TWITTER_ACCESS_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        logging.error("Missing Twitter API credentials! Set them as environment variables.")
        sys.exit(1)

    logging.info("Authenticating with Twitter API")
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
    api = tweepy.API(auth)

    logging.info(f"Posting tweet:\n{tweet_text}")
    api.update_status(tweet_text)
    logging.info("Tweet posted successfully.")

def main():
    entries = fetch_latest_entries(RSS_FEED_URL, limit=MAX_POSTS)
    for entry in entries:
        title = entry.title.strip()
        # Prefer summary, fall back to description or content
        content = getattr(entry, "summary", None) or getattr(entry, "description", None) or ""
        link = entry.link

        if not content:
            logging.warning("No summary/content found for entry. Skipping.")
            continue

        summary = summarize_text(content)
        tweet_text = format_tweet(title, summary, link)

        if len(tweet_text) > MAX_TWEET_LENGTH:
            logging.warning("Tweet too long even after truncation, skipping.")
            continue

        post_to_twitter(tweet_text)

if __name__ == "__main__":
    main()