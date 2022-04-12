import asyncio
import sys
import json

from make_table import send_message_to_user
from make_table import MakeTable

bot = None

# operating with config.json file
def _get_current_config(SCRIPT_PATH):
    with open(f"{SCRIPT_PATH}/config.json", "r") as f:
        return json.load(f)


def _set_current_config(SCRIPT_PATH, current_config: dict):
    with open(f"{SCRIPT_PATH}/config.json", "w") as f:
        f.write(json.dump(current_config))


SCRIPT_PATH = list(sys.argv)[1]
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
        TELEGRAM_KEY=CURRENT_CONFIG["TELEGRAM_KEY"],
        bot=bot,
    )
    # print(f"sended to {telegram_id} for group {timetable_image_buff[:20]}")


async def main():

    event_loop_tasks = []
    for target_group, telegram_ids in CURRENT_CONFIG["TELEGRAM_GROUPS"].items():
        timetable_image_buff = await generate_targetgroup_timetable(target_group)
        for telegram_id in telegram_ids:

            event_loop_tasks.append(
                asyncio.ensure_future(
                    send_table_to_user(timetable_image_buff, telegram_id)
                )
            )
            print(f"content {target_group} to {telegram_id}")

    for event_loop_task in event_loop_tasks:
        await event_loop_task

    global bot

    if bot != None:
        session = await bot.get_session()
        await session.close()


asyncio.run(main())

# ,
#         "466262044" : ["ХХБО-04-19", "ХХБО-03-19"]
