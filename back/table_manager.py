import numpy as np
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime

import os
import random
from back.image_manager import TextImage

dow = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
sf_pairs = ["900-1030", "1040-1210", "1240-1410", "1420-1550", "1620-1750", "1800-1930"]
start_date = "07.02.2022"

today_dow = dow[datetime.now().weekday() + 1]


def get_table(
    CACHED_TABLE_PATH: str = None,
    CACHED_TABLE_NAME: str = None,
    DOWNLOAD_LINK: str = None,
):
    def download_table(DOWNLOAD_LINK):
        responce = requests.get(DOWNLOAD_LINK)
        with BytesIO(responce.content) as bytes_table:
            # Unnamed:0 - index, we don`t need it
            return pd.io.excel.read_excel(bytes_table).drop("Unnamed: 0", axis=1)

    def get_cached_table(CACHED_TABLE_PATH, CACHED_TABLE_NAME):
        return pd.read_excel(f"{CACHED_TABLE_PATH}/{CACHED_TABLE_NAME}")

    def save_cache(table, CACHED_TABLE_PATH, CACHED_TABLE_NAME):
        table.to_excel(f"{CACHED_TABLE_PATH}/{CACHED_TABLE_NAME}", index=False)

    table = False

    if DOWNLOAD_LINK:
        table = download_table(DOWNLOAD_LINK)

    elif CACHED_TABLE_PATH and CACHED_TABLE_NAME:
        table = get_cached_table(CACHED_TABLE_PATH, CACHED_TABLE_NAME)

    else:
        table = False

    if table.shape[0] and CACHED_TABLE_PATH and CACHED_TABLE_NAME:
        save_cache(table, CACHED_TABLE_PATH, CACHED_TABLE_NAME)

    return table


def split_table(table, target_group):
    global dow
    global sf_pairs

    def get_start_group_point(table, target_group):

        column1 = list(table[table.columns.values[0]].values)
        row_index = column1.index("Группа")
        column_index = list(table.iloc[row_index, :].values).index(target_group)

        return column_index, row_index

    def clean_df_table(table):
        return table.dropna()

    column_index, row_index = get_start_group_point(table, target_group)

    # 12*6 - pairs per day * working days
    # +2 - useless rows
    # +4 - pair_name, type_of_pair, teacher, classroom
    target_table = table.iloc[
        row_index + 2 : row_index + 2 + 12 * 6, column_index : column_index + 4
    ].reset_index(drop=True)

    new_pair_types = target_table[target_table.columns.values[1]].apply(
        lambda x: x if x != "пр" else "сем"
    )

    target_table[target_table.columns.values[1]] = new_pair_types

    target_table_odd = pd.concat(
        (
            pd.Series(np.array(list(map(lambda x: [x] * 6, dow))).reshape(1, -1)[0]),
            pd.Series(sf_pairs * 6),
            target_table.iloc[::2].reset_index(drop=True),
        ),
        axis=1,
    )

    target_table_even = pd.concat(
        (
            pd.Series(np.array(list(map(lambda x: [x] * 6, dow))).reshape(1, -1)[0]),
            pd.Series(sf_pairs * 6),
            target_table.iloc[1::2].reset_index(drop=True),
        ),
        axis=1,
    )

    return (
        clean_df_table(target_table_odd),
        clean_df_table(target_table_even),
    )


def daily_table_text(table, target_group):
    global sf_pairs
    global dow
    global start_date
    global today_dow

    def make_dow_table_text(table):
        today_dow = dow[datetime.today().weekday()]

        today_table = table[table[table.columns.values[0]] == today_dow].reset_index(
            drop=True
        )

        s = ""
        times_arr = []
        for row in today_table[today_table.columns.values[1:]].to_records():
            times_arr.append(row[1])
            s += f"{sf_pairs.index(row[1]) + 1} ({row[1]})\n"
            s += f"  {(row[2])}\n"
            s += f"  {row[3]} {row[5]}\n"
            s += f"  {row[4]}\n\n"
        s = s[:-1]

        return s, times_arr

    current_week = datetime.now().isocalendar()[1]
    start_week = datetime.strptime(start_date, "%d.%m.%Y").isocalendar()[1]

    odd_week = (current_week - start_week) % 2 == 1
    today_list = list(datetime.now().date().timetuple())[:3][::-1]
    times_arr = []

    s = target_group + "\n"
    s += f'Сегодня {".".join(str(el) for el in today_list)} '
    s += f"({today_dow})\n"
    s += "Нечетная" if odd_week else "Четная"
    s += f" неделя ({current_week - start_week})\n\n"

    if odd_week:
        s_, times_arr = make_dow_table_text(split_table(table, target_group)[0])

        s += s_

    else:
        s_, times_arr = make_dow_table_text(split_table(table, target_group)[1])

        s += s_

    pair_start = times_arr[0].split("-")[0]
    pair_stop = times_arr[-1].split("-")[-1]

    s += f"\nС {pair_start} до {pair_stop}"

    return s


def weekly_table_text(table, target_group):
    global sf_pairs
    global dow
    global start_date
    global today_dow

    current_week = datetime.now().isocalendar()[1]
    start_week = datetime.strptime(start_date, "%d.%m.%Y").isocalendar()[1]

    odd_week = (current_week - start_week) % 2 == 1
    today_list = list(datetime.now().date().timetuple())[:3][::-1]

    s = target_group + "\n"
    s += f'Сегодня {".".join(str(el) for el in today_list)} '
    s += f"({today_dow})\n"
    s += "Нечетная" if odd_week else "Четная"
    s += f" неделя ({current_week - start_week})\n\n"

    tab = split_table(table, target_group)[0 if odd_week else 1]

    for i, day_of_week in enumerate(dow):
        dow_table = tab[tab[tab.columns.values[0]] == day_of_week]

        if dow_table.shape[0] == 0:
            continue

        pair_time = dow_table[tab.columns.values[1]].values
        pair_number = list(map(lambda x: sf_pairs.index(x) + 1, pair_time))
        pair_name = dow_table[tab.columns.values[2]].values

        s += day_of_week + "\n"

        for i, cur_pair_number in enumerate(pair_number):
            s += f"  {cur_pair_number} : {pair_name[i]}\n"

        s += "\n"

    s += "Удивительное количество пар !!!\n"
    s += f"Целых {tab.shape[0]} всего за неделю"

    return s


def genegate_timetable_text(
    target_group,
    CACHED_TABLE_PATH: str = None,
    CACHED_TABLE_NAME: str = None,
    DOWNLOAD_LINK: str = None,
):

    table = get_table(
        CACHED_TABLE_PATH=CACHED_TABLE_PATH,
        CACHED_TABLE_NAME=CACHED_TABLE_NAME,
        DOWNLOAD_LINK=DOWNLOAD_LINK,
    )

    global today_dow

    if today_dow == "Вс":
        return weekly_table_text(table, target_group)

    else:
        return daily_table_text(table, target_group)


def make_timetable_image_buff(SCRIPT_PATH: str, target_group, CURRENT_CONFIG):

    REL_FONT_PATH = CURRENT_CONFIG["FONT_PATH"]
    REL_IMAGE_PATH = CURRENT_CONFIG["REL_IMAGE_PATH"]
    CACHED_TABLE_PATH = CURRENT_CONFIG["CACHED_TABLE_PATH"]
    CACHED_TABLE_NAME = CURRENT_CONFIG["CACHED_TABLE_NAME"]

    DOWNLOAD_LINK = CURRENT_CONFIG["DOWNLOAD_LINK"]["FULL_LINK_PATH"]

    def pick_background_image_path(SCRIPT_PATH, REL_IMAGE_PATH):

        random_image_filename = random.choice(
            os.listdir(f"{SCRIPT_PATH}/{REL_IMAGE_PATH}")
        )

        background_image_path = f"{SCRIPT_PATH}/img/images/{random_image_filename}"

        return background_image_path

    table_text = genegate_timetable_text(
        CACHED_TABLE_PATH=CACHED_TABLE_PATH,
        CACHED_TABLE_NAME=CACHED_TABLE_NAME,
        target_group=target_group,
        DOWNLOAD_LINK=DOWNLOAD_LINK,
    )

    text_image = TextImage(
        timetable_text=table_text,
        rel_font_path=REL_FONT_PATH,
        SCRIPT_PATH=SCRIPT_PATH,
        background_image_path=pick_background_image_path(SCRIPT_PATH, REL_IMAGE_PATH),
    )

    img = text_image.make_timetable_image()

    buff = BytesIO()
    img.save(buff, format="PNG")

    return buff.getvalue()
