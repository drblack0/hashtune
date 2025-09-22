import datetime
import pandas as pd
import os
from google import genai
from dotenv import load_dotenv
from flask import jsonify
from apify_client.clients import ActorClientAsync
from app.utils.apify_client_singleton import ApifyClientSingleton
from app.utils.config import APIFY_KEY
from itertools import chain

load_dotenv()


async def get_scraper(scraper: str) -> ActorClientAsync:
    """Return an Apify actor client for the given scraper."""
    apify_client = ApifyClientSingleton(token=APIFY_KEY).get_client()
    return apify_client.actor(scraper)


def collect_toppost_values(df, column="topPosts_cleaned", unique=False):
    """Collect types, captions, and hashtags from a dataframe column of post dictionaries."""
    types = set() if unique else []
    captions = set() if unique else []
    hashtags = set() if unique else []

    for row in df[column].dropna():  # skip NaN rows
        if not isinstance(row, list):
            continue
        for d in row:
            if not isinstance(d, dict):
                continue
            if unique:
                types.add(d.get("type"))
                captions.add(d.get("caption", ""))
                hashtags.update(d.get("hashtags", []))
            else:
                types.append(d.get("type"))
                captions.append(d.get("caption", ""))
                hashtags.extend(d.get("hashtags", []))

    return types, captions, hashtags


async def get_last_run_hash_stats():
    """Fetch last run hashtag stats from Apify and extract captions + hashtags."""
    actor = await get_scraper("apify/instagram-hashtag-stats")
    last_run = actor.last_run()  # <-- ensure awaited
    dataset_client = last_run.dataset()

    dataset_data = await dataset_client.list_items()
    df = pd.DataFrame(dataset_data.items)

    _, captions, hashtags = collect_toppost_values(df, column="topPosts")
    return list(captions), list(hashtags)


def get_captions_and_hashtags_for_posts(df):
    """Extract captions and flatten hashtags safely from dataframe."""
    captions = df["caption"].dropna().tolist()
    hashtags_col = df["hashtags"].dropna().tolist()

    # keep only lists
    hashtags_col = [h for h in hashtags_col if isinstance(h, list)]
    hashtags = list(chain.from_iterable(hashtags_col))

    return captions, hashtags


async def get_last_run_posts():
    """Fetch last run posts from Apify and extract captions + hashtags."""
    actor = await get_scraper("apify/instagram-post-scraper")
    last_run = actor.last_run()
    dataset_client = last_run.dataset()

    dataset_data = await dataset_client.list_items()
    df = pd.DataFrame(dataset_data.items)

    captions, hashtags = get_captions_and_hashtags_for_posts(df)
    return captions, hashtags


def get_default_date():
    """Return yesterday's date in YYYY-MM-DD format."""
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
