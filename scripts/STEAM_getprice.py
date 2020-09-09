from CORE_utils import *
from STEAM_spider import get_price

@app.subroutine
async def __event_print_price(app: Mirai):
    current_hr, current_min = time.strftime(r"%H %M").split(sep=' ')
    current_hr = int(current_hr)
    current_min = int(current_min)
    left_time = ((current_hr % 8) * 60 + current_min) * 60
    left_time = int(8 * 3600 - left_time)
    await app.sendGroupMessage(
        HEARTBEAT_GROUP_ID,
        [
            Plain(text="下次价格播报时间：{:d}小时{:d}分后".format(int(left_time // 3600), int((left_time % 3600) // 60)))
        ]
    )
    await asyncio.sleep(left_time)
    while True:
        msg_list = [
            Face(faceId=QQFaces['shandian']),
            Plain(text="Steam充值价格播报"),
            Face(faceId=QQFaces['shandian']),
        ]
        data, rate = get_price()
        for item in data:
            msg_list.extend([
                Plain(text="\n====================\n"),
                Plain(text="商家名：{}\n价格：{} RMB = 50 USD\n比率：{:.2f}%".format(item['seller'], item['price'], float(item['price'])/(rate*50)*100))
                ])
        await app.sendGroupMessage(
            MAIN_GROUP_ID,
            msg_list
        )
        await asyncio.sleep(8 * 3600)