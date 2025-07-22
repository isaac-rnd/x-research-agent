import sys
import os
import logging
import tweepy
import google.generativeai as genai
from gnews import GNews
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


def get_latest_ai_news():
    logging.info("Fetching latest AI news from Google News...")
    try:
        google_news = GNews(language='en', country='US', period='1d')
        articles = google_news.get_news('AI technology')

        if articles:
            latest_article = articles[0]
            logging.info(f"News fetched successfully: '{latest_article['title']}'")
            return latest_article
        else:
            logging.warning("Could not find any recent AI news articles.")
            return None
    except Exception as e:
        logging.error(f"An error occurred during Google News call: {e}")
        return None


def summarize_news_for_tweet(news_text: dict) -> str:
    logging.info("Summarizing news with Gemini...")
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        news_content = f"Title: {news_text['title']}\n\nContent: {news_text.get('content') or news_text.get('description', '')}"
        article_url = news_text['url']

        prompt = f"""
        You are an expert AI news analyst. Summarize the following AI news into a
        concise, engaging, and professional tweet.
        The tweet MUST be under 280 characters.
        Include 2-3 relevant and popular hashtags like #AI, #TechNews, #ArtificialIntelligence.
        Do not include any introductory text like "Here's the summary:".
        Just provide the tweet text itself.

        Article URL: {article_url}

        News to summarize:
        ---
        {news_content}
        ---
        """
        response = model.generate_content(prompt)
        tweet_text = response.text.strip()

        if len(tweet_text) > 280:
            logging.warning(f"Gemini generated a tweet longer than 280 characters ({len(tweet_text)}). Truncating.")
            tweet_text = tweet_text[:277] + "..."

        logging.info("Summary generated successfully.")
        return tweet_text
    except Exception as e:
        logging.error(f"An error occurred during Gemini API call: {e}")
        sys.exit(1)

def post_to_twitter(tweet_text: str):
    try:
        client = tweepy.Client(
            access_token=TWITTER_ACCESS_TOKEN,access_token_secret= TWITTER_ACCESS_SECRET,
            consumer_key=TWITTER_API_KEY, consumer_secret=TWITTER_API_SECRET, 
            bearer_token=BEARER_TOKEN
        )
        logging.info("Twitter authentication successful.")
    except tweepy.errors.TweepyException as e:
        logging.error(f"Error during Twitter authentication: {e}")
        sys.exit(1)

    print("Starting to send the tweet")
    try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully.")
        logging.info(f"Tweet ID: {response.data['id']}")
    except tweepy.errors.TweepyException as e:
        logging.error(f"Error posting tweet: {e}")
        sys.exit(1)

def main():
    news_article = get_latest_ai_news()
    print(news_article)
    tweet_content = summarize_news_for_tweet(news_article)
    print(tweet_content)
    if tweet_content:
        post_to_twitter(tweet_content)

if __name__ == "__main__":
    main()