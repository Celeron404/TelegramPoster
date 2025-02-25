from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)


def load_envs():
    env_dict = dict()

    api_id = None
    api_id_str = os.getenv("TELEGRAM_API_ID", "NONE")
    if api_id_str != "NONE":
        try:
            api_id = int(api_id_str)
        except ValueError:
            logger.error("Error: api_id_str is not int.")
    else:
        raise ValueError("TELEGRAM_API_ID was not set.")
    env_dict["TELEGRAM_API_ID"] = api_id

    api_hash = os.getenv("TELEGRAM_API_HASH", "NONE")
    if api_hash == "NONE":
        raise ValueError("TELEGRAM_API_HASH was not set.")
    env_dict["TELEGRAM_API_HASH"] = api_hash

    main_dialog_id = None
    main_dialog_id_str = os.getenv("MAIN_DIALOG_ID", "NONE")
    if main_dialog_id_str != "NONE":
        try:
            main_dialog_id = int(main_dialog_id_str)
        except ValueError:
            logger.error("Error: main_dialog_id_str is not int.")
    else:
        raise ValueError("MAIN_DIALOG_ID was not set.")
    env_dict["MAIN_DIALOG_ID"] = main_dialog_id

    dialogs_to_post_ids = None
    dialogs_to_post_ids_str = os.getenv("DIALOGS_TO_POST_IDS", "NONE").split(",")
    if dialogs_to_post_ids_str != "NONE":
        try:
            dialogs_to_post_ids = list(map(int, dialogs_to_post_ids_str))
        except ValueError:
            logger.error("Error: dialogs_to_post_ids_str not contains int or contains not only int.")
    else:
        raise ValueError("DIALOGS_TO_POST_IDS was not set.")
    env_dict["DIALOGS_TO_POST_IDS"] = dialogs_to_post_ids

    sleep_between_send_messages = None
    sleep_between_send_messages_str = os.getenv("SLEEP_BETWEEN_SEND_MESSAGES", "NONE")
    if sleep_between_send_messages_str != "NONE":
        try:
            sleep_between_send_messages = int(sleep_between_send_messages_str)
        except ValueError:
            logger.error("Error: SLEEP_BETWEEN_SEND_MESSAGES is not int.")
    else:
        raise ValueError("SLEEP_BETWEEN_SEND_MESSAGES was not set.")
    env_dict["SLEEP_BETWEEN_SEND_MESSAGES"] = sleep_between_send_messages

    return env_dict
