#%%
import asyncio
import sys
import json

from make_table import send_message_to_user
from make_table import MakeTable

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

#%%
async def fucking_async(telegram_id, target_group):
    table = MakeTable(
        target_group,
        SCRIPT_PATH=SCRIPT_PATH,
        DOWNLOAD_LINK=DOWNLOAD_LINK,
        FONT_PATH=FONT_PATH,
    )
    await table._init()
    await send_message_to_user(
        user_id=telegram_id,
        image_value=await table.make_timetable_image_buff(),
        TELEGRAM_KEY=CURRENT_CONFIG["TELEGRAM_KEY"],
    )
    # print(f"sended to {telegram_id} for group {table.target_group}")


for telegram_id, target_group_arr in CURRENT_CONFIG["TELEGRAM_GROUPS"].items():
    for target_group in target_group_arr:

        asyncio.run(fucking_async(telegram_id, target_group))

# ,
#         "466262044" : ["ХХБО-04-19", "ХХБО-03-19"]
