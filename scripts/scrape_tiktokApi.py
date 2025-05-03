from TikTokApi import TikTokApi
import asyncio
import os
import csv
from datetime import datetime

# ms_token aus Umgebungsvariable oder direkt hier einfügen
ms_token = os.environ.get("ms_token", "HIER_DEIN_MS_TOKEN_EINFÜGEN")

# Zeitfilter (Epoch-Zeitstempel)
START_DATE = 1682899200  # 1. Mai 2023
END_DATE = 1745961599    # 30. April 2025

# Hashtags definieren
hashtags = ["tsla", "elonmusk", "teslastock", "tslastock"]

# CSV-Datei vorbereiten
output_file = "tiktok_videos.csv"

async def get_videos_for_hashtag(api, tag_name, writer):
    try:
        print(f"🔍 Suche nach: #{tag_name}")
        tag = api.hashtag(name=tag_name)

        async for video in tag.videos(count=200):
            create_time = int(video.create_time.timestamp())

            if START_DATE <= create_time <= END_DATE:
                data = video.as_dict
                print(f"📌 Video von @{data['author']['uniqueId']}, Likes: {data['stats']['diggCount']}, "
                      f"Shares: {data['stats']['shareCount']}, Comments: {data['stats']['commentCount']}, "
                      f"Erstellt am: {datetime.fromtimestamp(create_time)}, "
                      f"Caption: {data.get('desc', '')}")

                writer.writerow([
                    tag_name,
                    data['author']['uniqueId'],
                    data['stats']['diggCount'],
                    data['stats']['shareCount'],
                    data['stats']['commentCount'],
                    datetime.fromtimestamp(create_time),
                    data.get('desc', '')
                ])

    except Exception as e:
        print(f"⚠️ Fehler bei {tag_name}: {e}")

async def main():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hashtag", "Author", "Likes", "Shares", "Comments", "Created", "Caption"])

            for tag in hashtags:
                await get_videos_for_hashtag(api, tag, writer)

if __name__ == "__main__":
    asyncio.run(main())
