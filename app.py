import asyncio
import os
import logging
from aiogram import Bot

from back.table_manager import MakeTable
from back.config_manager import _get_current_config


SCRIPT_PATH = os.path.realpath(__file__)[:-7]
CURRENT_CONFIG = _get_current_config(SCRIPT_PATH)
DOWNLOAD_LINK = CURRENT_CONFIG["DOWNLOAD_LINK"]
REL_FONT_PATH = CURRENT_CONFIG["FONT_PATH"]

logging.basicConfig(
    filename=f"{SCRIPT_PATH}/misc/logfile.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


async def send_message_to_user(user_id, message=None, image_value=None, bot=None):

    if message != None and image_value == None:
        await bot.send_message(user_id, message)
    elif message == None and image_value != None:
        await bot.send_photo(user_id, photo=image_value)
    else:
        raise ValueError
    session = await bot.get_session()
    await session.close()


def _get_telegram_bot_key():
    global SCRIPT_PATH
    with open(f"{SCRIPT_PATH}/telegram_bot_key.txt", "r") as f:
        return f.read()


async def generate_targetgroup_timetable(
    target_group, SCRIPT_PATH, DOWNLOAD_LINK, REL_FONT_PATH
):
    table = MakeTable(
        target_group,
        SCRIPT_PATH=SCRIPT_PATH,
        DOWNLOAD_LINK=DOWNLOAD_LINK,
        REL_FONT_PATH=REL_FONT_PATH,
    )
    await table._init()

    return await table.make_timetable_image_buff()


async def send_table_to_user(timetable_image_buff, telegram_id, bot=None):
    await send_message_to_user(
        user_id=telegram_id,
        image_value=timetable_image_buff,
        bot=bot,
    )


async def main(SCRIPT_PATH, REL_FONT_PATH, DOWNLOAD_LINK):

    bot = Bot(token=_get_telegram_bot_key())

    event_loop_tasks = []
    for target_group, telegram_ids in CURRENT_CONFIG["TELEGRAM_GROUPS"].items():
        timetable_image_buff = await generate_targetgroup_timetable(
            target_group=target_group,
            SCRIPT_PATH=SCRIPT_PATH,
            REL_FONT_PATH=REL_FONT_PATH,
            DOWNLOAD_LINK=DOWNLOAD_LINK,
        )
        for telegram_id in telegram_ids:

            event_loop_tasks.append(
                asyncio.ensure_future(
                    send_table_to_user(timetable_image_buff, telegram_id, bot=bot)
                )
            )
            logging.info(f"sended to {telegram_id} for group {target_group}")

    for event_loop_task in event_loop_tasks:
        await event_loop_task

    if bot != None:
        session = await bot.get_session()
        await session.close()


asyncio.run(
    main(
        SCRIPT_PATH=SCRIPT_PATH,
        DOWNLOAD_LINK=DOWNLOAD_LINK,
        REL_FONT_PATH=REL_FONT_PATH,
    )
)

# ,
#         "466262044" : ["ХХБО-04-19", "ХХБО-03-19"]
