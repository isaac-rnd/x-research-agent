#!/bin/bash
# Local test script: requires Twitter API keys set as env vars

export TWITTER_API_KEY=${TWITTER_API_KEY:-"your_api_key"}
export TWITTER_API_SECRET=${TWITTER_API_SECRET:-"your_api_secret"}
export TWITTER_ACCESS_TOKEN=${TWITTER_ACCESS_TOKEN:-"your_access_token"}
export TWITTER_ACCESS_SECRET=${TWITTER_ACCESS_SECRET:-"your_access_secret"}
export GEMINI_API_KEY=${GEMINI_API_KEY:-"your_api_key"}
export BEARER_TOKEN=${BEARER_TOKEN:-"your_bearer_token_from_x"}

python tweet.py