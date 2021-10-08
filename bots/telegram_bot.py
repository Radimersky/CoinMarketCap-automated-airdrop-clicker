# make sure to have telethon and python-dotenv installed
# create a file called .env in the current directory from where you are running the script
# put API_ID and  API_HASH in the .env file in the following format
# VARIABLE=VALUE


from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import FloodWaitError

import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
index = "2"

# CHANNELS = ['GeoDBgroup', 'GeoDataBlock']  # the channels you want to join


async def join_telegram_channel(channels_list, session_file_name, api_id, api_hash):
    async with TelegramClient(session_file_name, api_id, api_hash) as client:
        for channel in channels_list:
            try:
                # user =  await client.get_me()
                # print(user.first_name)
                # print(user.last_name)
                # await client.send_message('me', 'Hello to myselfs!')
                await client(JoinChannelRequest(channel))
            except FloodWaitError as fwe:
                print(f'Telegram Waiting for {fwe}')
                await asyncio.sleep(delay=fwe.seconds)
            except Exception as err:
                print(f"Telegram Encountered an error while joining {channel}\n{err}")

# asyncio.run(join_telegram_channel([id], 'tg_session_' + index, os.getenv('TELEGRAM_API_ID_' + index), os.getenv('TELEGRAM_API_HASH_' + index)))