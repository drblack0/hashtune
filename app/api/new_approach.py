import asyncio
import os
import pandas as pd
from dotenv import load_dotenv
from apify_client import ApifyClientAsync

load_dotenv()

TOKEN = os.environ.get("APIFY_KEY")


async def main() -> None:
    # Client initialization with the API token
    apify_client = ApifyClientAsync(token=TOKEN)
    actor_client = apify_client.actor("apify/instagram-hashtag-stats")
    last_run = actor_client.last_run()

    dataset_client = last_run.dataset()

    dataset_data = await dataset_client.list_items()

    df = pd.DataFrame(dataset_data.items)
    df.to_csv("hashtag_stats.csv", index=False)


if __name__ == "__main__":
    asyncio.run(main())
