import asyncio

from make_table import send_message_to_user, CURRENT_CONFIG
from make_table import  MakeTable

async def fucking_async(telegram_id, target_group):
    table = MakeTable(target_group)
    await table._init()
    await send_message_to_user(
        user_id=telegram_id,
        image_value= await table.make_timetable_image_buff()
        )
    # print(f"sended to {telegram_id} for group {table.target_group}")

for telegram_id, target_group_arr in CURRENT_CONFIG['TELEGRAM_GROUPS'].items():
    for target_group in target_group_arr:

        asyncio.run(fucking_async(telegram_id, target_group))

# ,
#         "466262044" : ["ХХБО-04-19", "ХХБО-03-19"]