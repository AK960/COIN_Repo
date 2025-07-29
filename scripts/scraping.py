from TikTokApi import TikTokApi
import asyncio
import os
import csv
from datetime import datetime

# Dein ms_token hier setzen
ms_token = os.environ.get("ms_token", "DnPevDvWymMENd_458mGZy7KhxR1RaMauCRQqViCWQI-3lSevRZxz_OBq6vnNXGfSzTT2h7jFCr1f9ScKE4eOJ3AaY3M0F6eKN02pdU4foezaxaFEhsgiwlLu_Zvy_UVnJFkWgBBPK8FWDz4pmNPSZb-kg==")

# Zeitgrenzen als UNIX-Zeit (Epoch)
START_DATE = 1682899200  # 1. Mai 2023
END_DATE = 1745961599    # 30. April 2025

hashtags = ["tsla", "teslashares", "teslastock", "tslastock"]

output_file = "tiktok_videos2.csv"

async def get_videos_for_hashtag(api, tag_name, writer):
    try:
        print(f"🔍 Suche nach: #{tag_name}")
        tag = api.hashtag(name=tag_name)

        async for video in tag.videos(count=200):
            create_time = int(video.create_time.timestamp())  # ✅ korrekt eingerückt
            if START_DATE <= create_time <= END_DATE:
                data = video.as_dict
                video_url = f"https://www.tiktok.com/@{data['author']['uniqueId']}/video/{data['id']}"

                print(f"📌 @{data['author']['uniqueId']}, Likes: {data['stats']['diggCount']}, "
                      f"Erstellt: {datetime.fromtimestamp(create_time)}, URL: {video_url}")

                writer.writerow([
                    tag_name,
                    data['author']['uniqueId'],
                    data['stats']['diggCount'],
                    data['stats']['shareCount'],
                    data['stats']['commentCount'],
                    datetime.fromtimestamp(create_time),
                    data.get('desc', ''),
                    video_url
                ])
    except Exception as e:
        print(f"⚠️ Fehler bei {tag_name}: {e}")

async def main():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

        with open(output_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hashtag", "Author", "Likes", "Shares", "Comments", "Created", "Caption", "URL"])

            for tag in hashtags:
                await get_videos_for_hashtag(api, tag, writer)

if __name__ == "__main__":
    asyncio.run(main())
