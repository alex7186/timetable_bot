from PIL import Image, ImageDraw, ImageFont


class TextImage:
    def __init__(
        self, SCRIPT_PATH, timetable_text, rel_font_path, background_image_path
    ):
        self.SCRIPT_PATH = SCRIPT_PATH
        self.timetable_text = timetable_text
        self.font_path = f"{SCRIPT_PATH}/{rel_font_path}"

        self.background_image = Image.open(background_image_path)

    async def crop_image(self, img, new_w, new_h):
        w, h = img.size

        return img.crop(
            ((w - new_w) / 2, (h - new_h) / 2, (w + new_w) / 2, (h + new_h) / 2)
        )

    async def make_timetable_image(
        self,
        color=(255, 255, 255),
        text_hight=15,
    ):

        lines_count = len(self.timetable_text.split("\n"))
        image_size = (400, 30 + 18 * lines_count)

        self.background_image = (
            await self.crop_image(self.background_image, *image_size)
        ).point(lambda pixel: pixel * 0.5)

        drawer = ImageDraw.Draw(self.background_image)
        drawer.multiline_text(
            (15, 15),
            self.timetable_text,
            fill=color,
            font=ImageFont.truetype(self.font_path, text_hight),
        )

        return self.background_image
