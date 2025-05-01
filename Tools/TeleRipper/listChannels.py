from telethon.sync import TelegramClient
from telethon.errors import RPCError

# Replace these with your credentials from my.telegram.org
API_ID = 
API_HASH = ''


# Use a unique name for session storage
session_name = ''

with TelegramClient(session_name, API_ID, API_HASH) as client:
    try:
        print("Channels your account has joined:")

        for dialog in client.iter_dialogs():
            if dialog.is_channel:
                channel = dialog.entity
                print(f"Name: {channel.title}, ID: {channel.id}")

    except RPCError as e:
        print(f"An error occurred: {e}")
