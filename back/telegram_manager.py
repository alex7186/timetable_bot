async def send_message_to_user(user_id, message=None, image_value=None, bot=None):

    if message != None and image_value == None:
        await bot.send_message(user_id, message)
    elif message == None and image_value != None:
        await bot.send_photo(user_id, photo=image_value)
    else:
        raise ValueError


async def send_table_to_user(timetable_image_buff, telegram_id, bot=None):
    await send_message_to_user(
        user_id=telegram_id,
        image_value=timetable_image_buff,
        bot=bot,
    )
