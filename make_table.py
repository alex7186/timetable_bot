from datetime import datetime
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import random
from aiogram import Bot

# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor


# setup global consts
days_of_the_week = {
    "1": "Пн",
    "2": "Вт",
    "3": "Ср",
    "4": "Чт",
    "5": "Пт",
    "6": "Сб",
    "7": "Вс",
}

pair_time = {
    "1": [" 9.00", "10.30"],
    "2": ["10.40", "12.10"],
    "3": ["12.40", "14.10"],
    "4": ["14.20", "15.50"],
    "5": ["16.20", "17.50"],
    "6": ["18.00", "19.30"],
}


# setup telegram part
async def send_message_to_user(
    user_id, message=None, image_value=None, TELEGRAM_KEY=None
):

    bot = Bot(token=TELEGRAM_KEY)
    # dp = Dispatcher(bot)

    if message != None and image_value == None:
        await bot.send_message(user_id, message)
    elif message == None and image_value != None:
        await bot.send_photo(user_id, photo=image_value)
    else:
        raise ValueError
    await bot.session.close()


class MakeTable:
    def __init__(
        self,
        target_group,
        SCRIPT_PATH=None,
        DOWNLOAD_LINK=None,
        FONT_PATH=None,
        CACHED_TABLE_NAME="cached_table.xlsx",
    ):
        "setup variables"
        self.SCRIPT_PATH = SCRIPT_PATH
        self.DOWNLOAD_LINK = DOWNLOAD_LINK
        self.FONT_PATH = FONT_PATH
        self.target_group = target_group
        self.CACHED_TABLE_NAME = CACHED_TABLE_NAME

        self.week_type = ""  # odd/even week number
        self.week_delta = 0  # number of weeks since starting

    async def _init(self):

        current_week = datetime.now().isocalendar()[1]  # .dow
        start_week = datetime.strptime("07.02.2022", "%d.%m.%Y").isocalendar()[1]

        self.week_delta = current_week - start_week + 1

        (
            self.table_data,
            self.table_data_downloaded,
            self.table_modified_date,
        ) = await self.return_processed_table_data()

        if days_of_the_week[str(datetime.today().weekday() + 1)] == "Вс":
            self.table_text = await self.make_week_table()
        else:
            self.table_text = await self.make_today_table()

        # self.make_timetable_image_buff()

    async def generate_pair_time_table(self, input_table):
        "generating table with week, pair_number, pair_start, pair_end"

        pair_time_table = input_table.iloc[
            2:14:2, self.pair_time_table_bias[0] : self.pair_time_table_bias[1]
        ]
        pair_time_table = pair_time_table.reset_index(drop=True)

        pair_time_table = (
            pd.concat((pair_time_table, pair_time_table), axis=0)
            .sort_index()
            .reset_index(drop=True)
        )

        pair_time_table = pd.concat(
            (pd.Series(("Нечетная", "Четная") * 6), pair_time_table), axis=1
        )
        pair_time_table.columns = ("Неделя", "Номер пары", "Начало пары", "Конец пары")

        return pair_time_table

    async def generate_full_table(self, input_table, target_group):
        "parsing input table & generating table with dow, pairs, odd/even week flag, teacher, room_number"

        cols = list(input_table.columns)
        partial_input_table = input_table.iloc[
            0:, cols.index(target_group) : cols.index(target_group) + 4
        ]

        partial_input_table = partial_input_table.reset_index(drop=True)
        partial_input_table.columns = (
            "Предмет",
            "Вид занятий",
            "Преподаватель",
            "Аудитория",
        )

        days_of_the_week_table = pd.Series(
            np.array(
                ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота")
            ).repeat(12, axis=0),
            name="День недели",
        )

        pair_time_table = await self.generate_pair_time_table(input_table)
        full_table = pd.concat(
            (
                days_of_the_week_table,
                pd.concat(
                    [pair_time_table]
                    * (partial_input_table.shape[0] // pair_time_table.shape[0]),
                    axis=0,
                )
                .reset_index()
                .drop("index", axis=1),
                partial_input_table,
            ),
            axis=1,
        )

        full_table.fillna("", inplace=True)

        return full_table

    async def make_dict_from_odd_even_table(self, table):
        "make dict with separated odd/even pairs from full table"
        res_dict = {}

        commp = dict(
            zip(
                ("Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"),
                list(np.arange(1, 7)),
            )
        )
        for day_of_the_week, table_daily in table.groupby(("День недели")):

            if day_of_the_week not in res_dict:  # TODO not in res_dict
                res_dict[int(commp[day_of_the_week])] = {}

            for pair_number, table_pairly in table_daily.groupby(("Номер пары")):
                if pair_number not in res_dict[commp[day_of_the_week]]:

                    res_dict[commp[day_of_the_week]][int(pair_number)] = []

                if table_pairly.iloc[0]["Предмет"] != "":
                    for el in list(
                        table_pairly[
                            ["Предмет", "Вид занятий", "Преподаватель", "Аудитория"]
                        ]
                        .iloc[0]
                        .values
                    ):
                        res_dict[commp[day_of_the_week]][int(pair_number)].append(el)

        return res_dict  # TODO pd.DataFrame.pivot might make life easier (not sure :3 )

    async def download_table(self):
        "downloading the input table"
        r = requests.get(self.DOWNLOAD_LINK)

        with BytesIO(r.content) as fh:
            input_table = pd.io.excel.read_excel(fh)
            input_table.to_excel(f"{self.SCRIPT_PATH}/{self.CACHE_TABLE_NAME}")

        return input_table

    async def get_cached_table(self):
        return pd.read_excel(f"{self.SCRIPT_PATH}/{self.CACHED_TABLE_NAME}")

    async def update_table_downloading_link(self):
        pass

    async def get_table(self):
        "parsing the input table, making table cache"

        # file was modified farther then 12h -> download new file
        cache_file_modified_date = pd.to_datetime(
            os.path.getmtime(f"{self.SCRIPT_PATH}/{self.CACHED_TABLE_NAME}"), unit="s"
        )

        downloaded = False
        if (datetime.now() - cache_file_modified_date) / pd.Timedelta("1 hour") > 12:
            # print("trying to download the table")

            try:
                self.DOWNLOAD_LINK = await self.update_table_downloading_link()
                input_table = await self.download_table()
                downloaded = True
                # print("the table downloaded successfully")
            except Exception as e:
                pass
                # print("Using cached table")

        if not downloaded:
            input_table = await self.get_cached_table()
            downloaded = False

        input_table.columns = input_table.iloc[0]
        input_table = input_table.iloc[:74]

        try:
            self.pair_time_table_bias = (1, 4)
            full_table = await self.generate_full_table(input_table, self.target_group)

            res_dict = {
                "нечетная": await self.make_dict_from_odd_even_table(
                    full_table[full_table["Неделя"] == "Нечетная"]
                ),
                "четная": await self.make_dict_from_odd_even_table(
                    full_table[full_table["Неделя"] == "Четная"]
                ),
            }
        except Exception as e:
            self.pair_time_table_bias = (2, 5)
            full_table = await self.generate_full_table(input_table, self.target_group)

            res_dict = {
                "нечетная": await self.make_dict_from_odd_even_table(
                    full_table[full_table["Неделя"] == "Нечетная"]
                ),
                "четная": await self.make_dict_from_odd_even_table(
                    full_table[full_table["Неделя"] == "Четная"]
                ),
            }

        return {
            "data": res_dict,
            "downloaded": downloaded,
            "date_modified": cache_file_modified_date,
        }

    async def return_processed_table_data(self):

        if self.week_delta > 16:
            raise TimeoutError("LEARNING TIMEOUT")

        self.week_type = "нечетная" if self.week_delta % 2 == 1 else "четная"

        table_data, table_data_downloaded, table_modified_date = (
            await self.get_table()
        ).values()

        table_data = table_data[self.week_type]

        table_data = {
            days_of_the_week[str(key)]: value for key, value in table_data.items()
        }

        new_table_data = {}
        for key, values in table_data.items():

            if sum([len(el) for el in values.values()]):
                new_table_data.update({key: {}})

                for pair_number, value in values.items():
                    if value:
                        new_table_data[key].update(
                            {pair_number: value}
                        )  # new_table_data[key][pair_number] = value

        return new_table_data, table_data_downloaded, table_modified_date

    async def make_week_table(self):

        current_day = days_of_the_week[str(datetime.now().weekday() + 1)]

        table_str = (
            f"ПОЛУЧЕНО ИЗ КЭША ({str(self.table_modified_date)[:16]})\n\n"
            if not self.table_data_downloaded
            else ""
        )
        table_str += (
            self.target_group
            + "\nСегодня "
            + ".".join(
                (str(el) for el in list(datetime.now().date().timetuple())[:3][::-1])
            )
            + " ("
            + current_day
            + ")\n"
            + self.week_type[0].upper()
            + self.week_type[1:]
            + " неделя ("
            + str(self.week_delta)
            + ")\n\n"
        )

        # table_str += (
        #     self.week_type[0].upper()
        #     + self.week_type[1:]
        #     + " неделя ("
        #     + str(self.week_delta)
        #     + ")\n\n"
        # )

        count_of_pairs = 0
        for week_day in days_of_the_week.values():
            try:
                pairs = self.table_data[week_day]
            except Exception:
                continue

            week_day_printed = False
            for number, pair in pairs.items():
                prefix = (week_day + "\n  " if not week_day_printed else "  ") + " "
                week_day_printed = True

                content = str(number) + " : " + f"\t\t{pair[0]}"
                table_str += prefix + content + "\n"
                count_of_pairs += 1

            table_str += "\n"

        table_str += (
            f"Удивительное количество пар !!!\nЦелых {count_of_pairs} всего за неделю"
        )

        return table_str

    async def make_today_table(self):

        current_day = days_of_the_week[str(datetime.now().weekday() + 1)]

        current_day_table = self.table_data[current_day]

        table_str = (
            f"ПОЛУЧЕНО ИЗ КЭША ({str(self.table_modified_date)[:16]})\n\n"
            if not self.table_data_downloaded
            else ""
        )

        table_str += (
            self.target_group
            + "\nСегодня "
            + ".".join(
                (str(el) for el in list(datetime.now().date().timetuple())[:3][::-1])
            )
            + " ("
            + current_day
            + ")"
            + "\n"
            + self.week_type[0].upper()
            + self.week_type[1:]
            + " неделя ("
            + str(self.week_delta)
            + ")\n\n"
        )

        if current_day in list(self.table_data.keys()):
            content = ""

            for number, pair in current_day_table.items():

                content = (
                    content
                    + str(number)
                    + f" ({pair_time[str(number)][0]} - {pair_time[str(number)][1]})"
                    + f"\n\t\t{pair[0]}\n\t\t{pair[1]}"
                    + f"\t\t({pair[3]})\n\t\t{pair[2]}"
                    + "\n\n"
                )

        else:
            content = ""
        return (
            table_str
            + str(content)
            + f"С {pair_time[str(min(current_day_table))][0]} до "
            + f"{pair_time[str(max(current_day_table))][1]}"
        )

    async def crop_image(self, img, new_w, new_h):
        w, h = img.size

        return img.crop(
            ((w - new_w) / 2, (h - new_h) / 2, (w + new_w) / 2, (h + new_h) / 2)
        )

    async def pick_background_image(self):
        random_image_filename = random.choice(os.listdir(f"{self.SCRIPT_PATH}/images"))
        background_image = Image.open(
            f"{self.SCRIPT_PATH}/images/{random_image_filename}"
        )

        return background_image

    async def make_timetable_image(
        self,
        timetable_text,
        font_path,
        color=(255, 255, 255),
        text_hight=15,
    ):

        lines_count = len(timetable_text.split("\n"))
        image_size = (400, 30 + 18 * lines_count)
        background_image = await self.pick_background_image()
        background_image = (await self.crop_image(background_image, *image_size)).point(
            lambda pixel: pixel * 0.5
        )

        drawer = ImageDraw.Draw(background_image)
        drawer.multiline_text(
            (15, 15),
            timetable_text,
            fill=color,
            font=ImageFont.truetype(font_path, text_hight),
        )

        return background_image

    async def make_timetable_image_buff(self):
        img = await self.make_timetable_image(self.table_text, self.FONT_PATH)

        buff = BytesIO()
        img.save(buff, format="PNG")

        return buff.getvalue()
