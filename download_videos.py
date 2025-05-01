import os
from telethon.sync import TelegramClient
from telethon.errors import RPCError
from telethon.tl.types import MessageMediaDocument, DocumentAttributeVideo

API_ID = xxxxx
API_HASH = ''
SESSION_NAME = ''
CHANNEL = -100
DOWNLOAD_DIR = 'downloaded_videos'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
    try:
        print(f"Downloading videos from channel: {CHANNEL}")
        count = 0

        for message in client.iter_messages(CHANNEL):
            if message.media and isinstance(message.media, MessageMediaDocument):
                attributes = message.media.document.attributes
                is_video = any(
                    isinstance(attr, DocumentAttributeVideo) and not attr.round_message
                    for attr in attributes
                )

                if is_video:
                    count += 1
                    filename = os.path.join(DOWNLOAD_DIR, f"video{count}.mp4")
                    print(f"Downloading video #{count}...")
                    client.download_media(message, file=filename)

        if count == 0:
            print("No videos found in this channel.")
        else:
            print(f"Downloaded {count} videos successfully.")

    except RPCError as e:
        print(f"An error occurred: {e}")
