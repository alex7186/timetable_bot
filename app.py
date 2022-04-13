import asyncio
import sys
import json
from aiogram import Bot
from make_table import MakeTable
import logging

bot = None
SCRIPT_PATH = list(sys.argv)[1]
logging.basicConfig(
    filename=f"{SCRIPT_PATH}/misc/logfile.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


async def send_message_to_user(
    user_id, message=None, image_value=None, TELEGRAM_KEY=None, bot=None
):
    if bot == None:
        bot = Bot(token=TELEGRAM_KEY)
        # dp = Dispatcher(bot)

    if message != None and image_value == None:
        await bot.send_message(user_id, message)
    elif message == None and image_value != None:
        await bot.send_photo(user_id, photo=image_value)
    else:
        raise ValueError
    # await bot.session.close()

    return bot


# operating with config.json file
def _get_current_config(SCRIPT_PATH):
    with open(f"{SCRIPT_PATH}/misc/config.json", "r") as f:
        return json.load(f)


def _get_telegram_bot_key():
    global SCRIPT_PATH
    with open(f"{SCRIPT_PATH}/telegram_bot_key.txt", "r") as f:
        return f.read()


def _set_current_config(SCRIPT_PATH, current_config: dict):
    with open(f"{SCRIPT_PATH}/misc/config.json", "w") as f:
        f.write(json.dump(current_config))


CURRENT_CONFIG = _get_current_config(SCRIPT_PATH)
DOWNLOAD_LINK = CURRENT_CONFIG["DOWNLOAD_LINK"]
FONT_PATH = CURRENT_CONFIG["FONT_PATH"]


async def generate_targetgroup_timetable(target_group):
    table = MakeTable(
        target_group,
        SCRIPT_PATH=SCRIPT_PATH,
        DOWNLOAD_LINK=DOWNLOAD_LINK,
        FONT_PATH=FONT_PATH,
    )
    await table._init()

    return await table.make_timetable_image_buff()


async def send_table_to_user(timetable_image_buff, telegram_id):
    global bot
    bot = await send_message_to_user(
        user_id=telegram_id,
        image_value=timetable_image_buff,
        TELEGRAM_KEY=_get_telegram_bot_key(),
        bot=bot,
    )


async def main():
    global SCRIPT_PATH

    event_loop_tasks = []
    for target_group, telegram_ids in CURRENT_CONFIG["TELEGRAM_GROUPS"].items():
        timetable_image_buff = await generate_targetgroup_timetable(target_group)
        for telegram_id in telegram_ids:

            event_loop_tasks.append(
                asyncio.ensure_future(
                    send_table_to_user(timetable_image_buff, telegram_id)
                )
            )
            logging.info(f"sended to {telegram_id} for group {target_group}")

    for event_loop_task in event_loop_tasks:
        await event_loop_task

    global bot

    if bot != None:
        session = await bot.get_session()
        await session.close()


asyncio.run(main())

# ,
#         "466262044" : ["ХХБО-04-19", "ХХБО-03-19"]
