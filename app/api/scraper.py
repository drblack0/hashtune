import asyncio
import os
from flask import jsonify
from dotenv import load_dotenv
from google import genai
from .helpers import (
    get_last_run_hash_stats,
    get_last_run_posts,
    get_scraper,
    get_default_date,
)

load_dotenv()

async def scrape(hashtags, profiles):
    if not hashtags and not profiles:
        return jsonify(
            {
                "message": "No hashtags or profiles used",
                "status": "error",
            }
        )
    hashtag_result, profile_result = None, None
    if hashtags:
        hashtag_result = await scrape_hastag(hashtags)
    if profiles:
        profile_result = await scrape_profiles(profiles)
    return {
        "hashtag_result": hashtag_result,
        "profile_result": profile_result,
    }

async def scrape_hastag(hastags):
    actor = await get_scraper("apify/instagram-hashtag-stats")
    input_data = {"hashtags": hastags}
    result = await actor.call(run_input=input_data, timeout_secs=60)
    return result


async def scrape_profiles(
    usernames,
    only_newer_than=None,
    results_limit=5,
    skip_pinned_posts=False,
):
    actor = await get_scraper("apify/instagram-post-scraper")

    if not only_newer_than:
        only_newer_than = get_default_date()
    input_data = {
        "onlyPostsNewerThan": only_newer_than,
        "resultsLimit": results_limit,
        "skipPinnedPosts": skip_pinned_posts,
        "username": usernames,
    }

    result = await actor.call(run_input=input_data, timeout_secs=60)
    return result


async def get_gemini_response(hashtags_used=False, posts_used=False):
    if not hashtags_used and not posts_used:
        return jsonify(
            {
                "message": "No hashtags or posts used",
                "status": "error",
            }
        )
    all_caps, all_hashtags = [], []
    if hashtags_used:
        captions, hashtags = await get_last_run_hash_stats()
        all_caps.extend(captions)
        all_hashtags.extend(hashtags)

    if posts_used:
        captions, hashtags = await get_last_run_posts()
        all_caps.extend(captions)
        all_hashtags.extend(hashtags)

    prompt = "These are the captions and hashtags used in popular posts and hashtags which I associate my business account with: "
    content_string = " ".join(all_caps)
    content_string += " ".join(all_hashtags)

    prompt += content_string

    prompt += "Can you tell me 5 post ideas and scripts for them which I can use to create trending posts? Also include which hashtags I should be using with which post"
    gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt],
    )

    return jsonify({"markdown_string": response.text, "status": "success"})
