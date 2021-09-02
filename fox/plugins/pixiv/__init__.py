from nonebot.adapters.cqhttp.permission import GROUP
from nonebot.adapters.cqhttp.utils import escape
from nonebot.rule import to_me
from .pixiv_p import download_pic, lolicon_api
from fox.check import files_writer, qq_check
from nonebot.adapters.cqhttp.event import Event, GroupMessageEvent
from nonebot.plugin import on_command
from nonebot.adapters import Bot
from nonebot.typing import T_State

pixiv = on_command('来点涩图', block=True, permission=GROUP, aliases={"来点色图"})


ban_group = ban_group = "./fox/data/pixiv/ban_group.txt"
r18_group = "./fox/data/pixiv/r18_group.txt"
super_user = "./fox/data/config/superuser.txt"


@pixiv.handle()
async def pi(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if await qq_check(event.group_id, ban_group):
        await pixiv.finish("不许ghs喵！")
    await pixiv.send("loading...")
    if args == "r18" or args == "R18":
        if await qq_check(event.group_id, r18_group):
            url = await lolicon_api(r18=1)
            if "https://" not in str(url):
                err = str(url)
                await pixiv.finish(f"工口发生！\n{err}")
            if await download_pic(url) == "err":
                await pixiv.finish("工口发生！")
                await bot.call_api(api="send_group_msg", group_id=event.group_id, message="[CQ:image,file=file:///home/qqbot/fox/data/pixiv/image/_tt.jpg]")
                return
        else:
            await pixiv.finish("不许R18喵！")
    elif args == "":
        url = await lolicon_api(r18=0)
        if "https://" not in str(url):
            err = str(url)
            await pixiv.finish(f"工口发生！\n{err}")
        if await download_pic(url) == "err":
            await pixiv.finish("工口发生！")
        await bot.call_api(api="send_group_msg", group_id=event.group_id, message="[CQ:image,file=file:///home/qqbot/fox/data/pixiv/image/_tt.jpg]")
    else:
        await pixiv.finish("参数错误捏")

pixiv_r18 = on_command("pixiv_admin", rule=to_me(), block=True)


@pixiv_r18.handle()
async def p_admin(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if not await qq_check(event.get_user_id(), super_user):
        await pixiv_r18.finish("你没有权限捏")
    if args == "ban":
        result = await files_writer(event.group_id, "off", ban_group)
    elif args == "allow":
        result = await files_writer(event.group_id, "on", ban_group)
    elif args == "allow_r18":
        result = await files_writer(event.group_id, "off", r18_group)
    elif args == "ban_r18":
        result = await files_writer(event.group_id, "on", r18_group)
    else:
        await pixiv_r18.finish("参数错误捏\nban,allow,ban_r18,allow_r18")
    await pixiv_r18.finish(result)
