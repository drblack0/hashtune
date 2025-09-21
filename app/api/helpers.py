import datetime
import pandas as pd
import os
from google import genai
from dotenv import load_dotenv
from flask import jsonify
from apify_client.clients import ActorClientAsync
from app.utils.apify_client_singleton import ApifyClientSingleton
from app.utils.config import APIFY_KEY

load_dotenv()


async def get_scraper(scraper: str) -> ActorClientAsync:
    apify_client = ApifyClientSingleton(token=APIFY_KEY).get_client()
    return apify_client.actor(scraper)


def collect_toppost_values(df, column="topPosts_cleaned", unique=False):
    types = set() if unique else []
    captions = set() if unique else []
    hashtags = set() if unique else []

    for row in df[column]:
        for d in row:
            if unique:
                types.add(d["type"])
                captions.add(d["caption"])
                hashtags.update(d["hashtags"])
            else:
                types.append(d["type"])
                captions.append(d["caption"])
                hashtags.extend(d["hashtags"])

    return types, captions, hashtags


async def get_last_run_hash_stats():
    actor = await get_scraper("apify/instagram-hashtag-stats")
    last_run = actor.last_run()
    dataset_client = last_run.dataset()

    dataset_data = await dataset_client.list_items()

    df = pd.DataFrame(dataset_data.items)
    _, captions, hashtags = collect_toppost_values(df, column="topPosts")
    return captions, hashtags


def get_captions_and_hashtags_for_posts(df):
    captions = df["caption"].tolist()
    hashtags = sum(df["hashtags"].tolist(), [])  # flattens the list of lists
    return captions, hashtags


async def get_last_run_posts():
    actor = await get_scraper("apify/instagram-post-scraper")
    last_run = actor.last_run()
    dataset_client = last_run.dataset()

    dataset_data = await dataset_client.list_items()

    df = pd.DataFrame(dataset_data.items)
    df.to_csv("posts.csv", index=False)
    captions, hashtags = get_captions_and_hashtags_for_posts(df)
    return captions, hashtags


def get_default_date():
    return (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
