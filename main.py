import asyncio
from telethon import TelegramClient

from get_os_envs import load_envs
import logging


env_dict = load_envs()

client = TelegramClient('test_tg', env_dict["TELEGRAM_API_ID"], env_dict["TELEGRAM_API_HASH"])

# Config
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
grouped_ids = dict()
sent_grouped_ids = set()


async def forward_simple_message(message):
    for dialog_id in env_dict["DIALOGS_TO_POST_IDS"]:
        try:
            await (client.forward_messages(dialog_id, message))
            logger.debug(f"Message was forwarded to dialog {dialog_id}: \n\t message = {message}")

            await asyncio.sleep(env_dict["SLEEP_BETWEEN_SEND_MESSAGES"])
        except Exception as e:
            logger.error(f"Error trying forward simple message to dialog {dialog_id}: {e}")


async def forward_albums():
    for group_id, messages in grouped_ids.items():
        media_list = [msg.media for msg in messages if msg.media]
        caption = ""
        for message in messages:
            if message.text != "" and message.text is not None:
                caption += message.text

        for dialog_id in env_dict["DIALOGS_TO_POST_IDS"]:
            try:
                await client.send_file(dialog_id, media_list, caption=caption)
                logger.debug(f"Album was forwarded: \n\t to dialog: {dialog_id} \n\t grouped_id: {group_id} \n\t caption: {caption[0:119]} \n\t media_list: {media_list}")
            except Exception as e:
                print(f"Error trying forward album with grouped_id {group_id} to dialog {dialog_id}: {e}")

            await asyncio.sleep(env_dict["SLEEP_BETWEEN_SEND_MESSAGES"])


async def forward_messages():
    logger.info("Starting forward messages")

    # Getting main dialog
    main_dialog = None
    client_dialogs = await client.get_dialogs()
    for dialog in client_dialogs:
        if dialog.entity.id == env_dict["MAIN_DIALOG_ID"]:
            main_dialog = dialog
            logger.info(f'Main dialog with id {env_dict["MAIN_DIALOG_ID"]} was found')
            break
    if main_dialog is None:
        logger.error(f'Main dialog with id {env_dict["MAIN_DIALOG_ID"]} was not found')
        return

    # Getting all messages for sending
    messages = await client.get_messages(main_dialog, limit=100)

    # Sending messages and getting albums
    for message in messages:
        if message.grouped_id:
            group_id = message.grouped_id
            if group_id in sent_grouped_ids:
                continue

            if group_id not in grouped_ids:
                grouped_ids[group_id] = []

            grouped_ids[group_id].append(message)
        else:
            await forward_simple_message(message)

    # Forwarding albums
    await forward_albums()

    logger.info("Task completed.")


client.start()
client.loop.run_until_complete(forward_messages())
