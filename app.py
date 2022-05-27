import asyncio
import os
from aiogram import Bot


from back.config_manager import get_config
from back.telegram_manager import send_table_to_user
from back.token_manager import get_token
from back.table.table_manager import make_timetable_image_buff


SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])


async def start_app():

    global SCRIPT_PATH
    CURRENT_CONFIG = get_config(SCRIPT_PATH)
    bot = Bot(token=get_token(SCRIPT_PATH))

    for target_group, telegram_ids in CURRENT_CONFIG["TELEGRAM_GROUPS"].items():

        timetable_image_buff = make_timetable_image_buff(
            SCRIPT_PATH=SCRIPT_PATH,
            CURRENT_CONFIG=CURRENT_CONFIG,
            target_group=target_group,
        )

        for telegram_id in telegram_ids:
            await send_table_to_user(timetable_image_buff, telegram_id, bot=bot)

    if bot != None:
        session = await bot.get_session()
        await session.close()


asyncio.run(start_app())


# "466262044" : ["ХХБО-04-19", "ХХБО-03-19"]
