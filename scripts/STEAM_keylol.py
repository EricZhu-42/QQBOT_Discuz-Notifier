from CORE_utils import *
from STEAM_spider import get_data, load_file, process_data, save_file, time_equal

if DEBUG:
    STEAM_GROUP_ID = HEARTBEAT_GROUP_ID

# Spider configs
base_url = r"https://keylol.com/"
forum_url = base_url + r"forum.php?mod=forumdisplay&fid={}&filter=author&orderby=dateline"

free_section_url = forum_url.format(319)
discount_sction_url = forum_url.format(234)
chat_section_url = forum_url.format(148)

section2icon_dict = {
    "福利放送": 'taiyang',
    "购物心得": 'xigua',
}


last_update_time = time.time()

# Spider subroutine
@app.subroutine
async def __event_spider_update(app: Mirai):
    global_counter = 0
    while True:
        current_date = time.strftime(r"%Y-%m-%d")
        js = load_file(current_date)

        data = list()
        data.extend(process_data(get_data(url=discount_sction_url, section="购物心得"), js))
        data.extend(process_data(get_data(url=free_section_url, section="福利放送"), js))

        send_counter = 0
        for item in data:
            if time_equal(item['msg_date'], current_date):

                icon = section2icon_dict.get(item['section'])
                if not icon:
                    icon = 'nanguo'

                await app.sendGroupMessage(
                    STEAM_GROUP_ID,
                    [
                        Plain(text='---'),
                        Face(faceId=QQFaces[icon]),
                        Plain(text="{}".format(item['section'])),
                        Face(faceId=QQFaces[icon]),
                        Plain(text='---\n'),
                        Plain(text="分类：{}\n".format(item['msg_type'])),
                        Plain(text="主题：{}\n".format(item['msg_content'])),
                        Plain(text="链接：{}t{}-1-1".format(base_url, item['msg_link_id']))
                    ]
                )

                send_counter += 1
                if send_counter >= 10:
                    await app.sendGroupMessage(
                        HEARTBEAT_GROUP_ID,
                        [
                            Plain(text="警告！当前轮次存在未发送完毕的信息。")
                        ]
                    )
                    break

        global_counter += 1
        save_file(current_date, js)

        global last_update_time
        last_update_time = time.time()
        print("Update at", time.strftime(r"%b %d %Y %H:%M:%S"))
        await asyncio.sleep(120)

# Heartbeat subroutine to keep alive
@app.subroutine
async def __event_keep_alive(app: Mirai):
    while True:
        wait_time = random.uniform(240, 300)
        await app.sendGroupMessage(
            HEARTBEAT_GROUP_ID,
            [
                Plain(text="{}".format(wait_time))
            ]
        )
        if time.time() - last_update_time > 600:
            await app.sendTempMessage(
                HEARTBEAT_GROUP_ID,
                MASTER_QQ_ID,
                [
                    Plain(text="掉线啦！！！")
                ]
            )
        await asyncio.sleep(wait_time)