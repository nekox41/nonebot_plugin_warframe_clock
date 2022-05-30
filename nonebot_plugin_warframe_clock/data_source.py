from io import BytesIO
from typing import Union
from pathlib import Path
import arrow
import httpx
from PIL import Image, ImageDraw, ImageFont


class wfClock():
    """获取各个开放地图的时间状态。"""
    __file_path__ = Path(__file__).parent / 'data'

    def __init__(self) -> None:
        pass

    @classmethod
    async def eidolon(cls) -> Union[BytesIO, None]:
        """获取夜灵平野的状态。"""

        async with httpx.AsyncClient() as client:
            try:
                worldState = await client.get("http://content.warframe.com/dynamic/worldState.php")
                if worldState.status_code != 200:
                    raise Exception(f"错误代码：{worldState.status_code}")
            except:
                return None
            else:
                worldState = worldState.json()

        for item in worldState["SyndicateMissions"]:
            if item["Tag"] == "CetusSyndicate":
                jobStart = arrow.get(
                    (int(item["Activation"]["$date"]["$numberLong"])) / 1000, tzinfo="Asia/Shanghai")
                jobEnd = arrow.get(
                    (int(item["Expiry"]["$date"]["$numberLong"])) / 1000, tzinfo="Asia/Shanghai")
                break

        toNight = jobStart.shift(minutes=100)
        isDay = arrow.now() < toNight
        mShift = 0 if isDay else 150
        toNext = toNight if isDay else jobEnd
        nightList = []
        for _ in range(5):
            nightList.append(
                toNight.shift(minutes=mShift).format("HH:mm | hh:mm A")
            )
            mShift += 150

        stateStr = f"当前状态：{'白天' if isDay else '夜晚'}\n\n距离切换：{toNext.humanize(locale='zh-cn', only_distance=True, granularity=['hour', 'minute', 'second'])}"
        nightStr = "\n\n".join(nightList)
        timeImage = BytesIO()
        img = Image.open(cls.__file_path__ / '夜灵背景.png')
        draw = ImageDraw.ImageDraw(img)
        tfont = ImageFont.truetype(f'{cls.__file_path__}/font1.ttf', 55)
        textW, textH = draw.textsize(stateStr, tfont)
        draw.text(((800-textW)/2, (368-textH)/2),
                  stateStr, font=tfont, align="center")
        textW, textH = draw.textsize(nightStr, tfont)
        draw.text(((800-textW)/2, (788-textH)/2 + 368), nightStr, font=tfont)
        img.save(timeImage, "png")
        return timeImage

    @classmethod
    def earth(cls) -> BytesIO:
        now = arrow.now().int_timestamp % 28800
        isDay = now < 14400
        leftSeconds = 14400 - (now % 14400)
        toNext = arrow.now().shift(seconds=leftSeconds)
        earthState = "当前状态：{}\n\n距离结束：{}".format("白天" if isDay else '夜晚', toNext.humanize(
            locale='zh-cn', only_distance=True, granularity=['hour', 'minute', 'second']))
        earthImage = BytesIO()
        img = Image.open(cls.__file_path__ / '时间背景.png')
        draw = ImageDraw.ImageDraw(img)
        tfont = ImageFont.truetype(f'{cls.__file_path__}/font1.ttf', 28)
        textW, textH = draw.textsize(earthState, tfont)
        draw.text(((400-textW)/2, (400-textH)/2),
                  earthState, font=tfont, align="center")
        img.save(earthImage, "png")
        return earthImage

    @classmethod
    def vallis(cls) -> BytesIO:
        start = arrow.get("2018-11-10 08:13:48")
        loop = 1600
        cold = 1200
        sinceLast = (arrow.now().int_timestamp - start.int_timestamp) % loop
        toNextFull = loop - sinceLast
        state = "寒冷"
        if (toNextFull > cold):
            state = "温暖"
            toNextMinor = toNextFull - cold
        else:
            toNextMinor = toNextFull

        stateStr = "当前状态：{}\n\n距离结束：{}".format(state, arrow.now().shift(seconds=toNextMinor).humanize(
            locale='zh-cn', only_distance=True, granularity=['hour', 'minute', 'second']))
        vallisImage = BytesIO()
        img = Image.open(cls.__file_path__ / '时间背景.png')
        draw = ImageDraw.ImageDraw(img)
        tfont = ImageFont.truetype(f'{cls.__file_path__}/font1.ttf', 28)
        textW, textH = draw.textsize(stateStr, tfont)
        draw.text(((400-textW)/2, (400-textH)/2),
                  stateStr, font=tfont, align="center")
        img.save(vallisImage, "png")
        return vallisImage

    @classmethod
    async def cambion(cls) -> Union[BytesIO, None]:
        async with httpx.AsyncClient() as client:
            try:
                worldState = await client.get("http://content.warframe.com/dynamic/worldState.php")
                if worldState.status_code != 200:
                    raise Exception(f"错误代码：{worldState.status_code}")
            except:
                return None
            else:
                worldState = worldState.json()

        for item in worldState["SyndicateMissions"]:
            if item["Tag"] == "CetusSyndicate":
                jobStart = arrow.get(
                    (int(item["Activation"]["$date"]["$numberLong"])) / 1000, tzinfo="Asia/Shanghai")
                jobEnd = arrow.get(
                    (int(item["Expiry"]["$date"]["$numberLong"])) / 1000, tzinfo="Asia/Shanghai")
                break

        toNight = jobStart.shift(minutes=100)
        isDay = arrow.now() < toNight
        toNext = toNight if isDay else jobEnd
        stateStr = f"当前状态：{'Fass' if isDay else 'Vome'}\n\n距离结束：{toNext.humanize(locale='zh-cn', only_distance=True, granularity=['hour', 'minute', 'second'])}"
        timeImage = BytesIO()
        img = Image.open(cls.__file_path__ / '时间背景.png')
        draw = ImageDraw.ImageDraw(img)
        tfont = ImageFont.truetype(f'{cls.__file_path__}/font1.ttf', 28)
        textW, textH = draw.textsize(stateStr, tfont)
        draw.text(((400-textW)/2, (400-textH)/2),
                  stateStr, font=tfont, align="center")
        img.save(timeImage, "png")
        return timeImage
