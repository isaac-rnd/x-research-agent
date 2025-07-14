# Daily AI News Tweet Bot

This GitHub Action posts daily summaries of the latest AI research/news from an RSS feed (default: arXiv cs.AI) as concise tweets. Summaries are generated using open-source HuggingFace models.

## Features

- **Automated**: Runs every day at 10 PM IST (16:30 UTC) via GitHub Actions.
- **Summarizes**: Uses HuggingFace's free `transformers` pipeline.
- **Tweets**: Posts to Twitter/X using Tweepy.
- **Secure**: Credentials managed via GitHub Secrets—no paid APIs.

## File Tree

```text
.
├── .github/workflows/daily_tweet.yml   # GitHub Actions workflow
├── README.md
├── requirements.txt
├── tweet.py                            # Main script
├── test_tweet.sh                       # (Optional) Shell script for local testing
```

## Setup & Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Install Python Dependencies

Ensure Python 3.10+ is installed.

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Set up Twitter Developer Credentials

- Create a [Twitter Developer App](https://developer.twitter.com/en/docs/apps/overview).
- Generate your keys/tokens:
  - `TWITTER_API_KEY`
  - `TWITTER_API_SECRET`
  - `TWITTER_ACCESS_TOKEN`
  - `TWITTER_ACCESS_SECRET`

### 4. Add GitHub Secrets

Go to your repo ➔ **Settings** ➔ **Secrets and variables** ➔ **Actions** ➔ **New repository secret**. Add:

- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

### 5. Test Locally (Optional)

Create a `.env` file or export credentials as environment variables:

```bash
export TWITTER_API_KEY=...
export TWITTER_API_SECRET=...
export TWITTER_ACCESS_TOKEN=...
export TWITTER_ACCESS_SECRET=...
python tweet.py
```

Or use the provided script:

```bash
bash test_tweet.sh
```

### 6. Push to GitHub

Commit your changes and push:

```bash
git add .
git commit -m "Initial commit: Daily AI Tweet bot"
git push
```

## Customization

- **Change the RSS feed**: Edit `RSS_FEED_URL` in `tweet.py` to another RSS source.
- **Change posting time**: Modify the `cron` entry in `.github/workflows/daily_tweet.yml`.
- **Model choice**: Update the `summarize_text` function in `tweet.py` for alternative HuggingFace models.

## Troubleshooting

- **Missing dependencies**: Run `pip install -r requirements.txt`.
- **API errors**: Confirm all credentials are set and correct.
- **Tweet too long?**: Script auto-truncates, but review logs for skipped posts.

## License

MIT