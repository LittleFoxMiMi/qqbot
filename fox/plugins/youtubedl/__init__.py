import subprocess
import os

from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.typing import T_State
from fox.check import qq_check

youtubedl = on_command("youtubedl", priority=1, block=True)
super_user = "./fox/data/config/superuser.txt"
download_path = "/home/qqbot/fox/data/youtubedl/"


@youtubedl.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip().split(" ")
    if not await qq_check(event.get_user_id(), super_user):
        await youtubedl.finish("你没有权限捏")
    len_args = len(args)
    download_args = f"cd {download_path} && youtube-dl -f best "
    ffmpeg_args = ""
    if args==[""]:
        await youtubedl.finish("至少需要一个url参数")
    elif len_args>2:
        await youtubedl.finish("传入了过多的参数！\nyoutubedl url [mp3/mp4]")
    download_args += args[0]
    try:
        await clear_dir()
    except:
        await youtubedl.finish("清空download目录错误！")
    await youtubedl.send("正在下载。。。")
    await download(download_args)
    filename=os.listdir(download_path)
    name=filename[0]
    if len_args ==2:
        await youtubedl.send("下载完成，正在转码。。。")
        if args[1] == "mp3":
            if name[-4:]==".mp3":
                await youtubedl.send("文件无需转码")
            else:
                ffmpeg_args = f"cd {download_path} && ffmpeg -i '{name}' -c:v libx264 -b:a 256k '{name}.mp3'"
                name+=".mp3"
                await ffmpeg_format(ffmpeg_args)
        elif args[1] == "mp4":
            if name[-4:]==".mp4":
                await youtubedl.send("文件无需转码")
            else:
                ffmpeg_args = f"cd {download_path} && ffmpeg -i '{name}' -c:v libx264 -c:a copy '{name}.mp4'"
                name+=".mp4"
                await ffmpeg_format(ffmpeg_args)
        else:
            await youtubedl.send("不支持的格式，将会发送原文件")
    await bot.call_api(api="upload_group_file",group_id=event.group_id,file=download_path+name,name=name)
    


async def download(args):
    try:
        subprocess.check_call(args,shell=True)
    except Exception as e:
        await youtubedl.finish("download错误！\n错误代码是:"+str(e))

async def clear_dir():
    filename=os.listdir(download_path)
    for name in filename:
        os.remove(download_path+name)

async def ffmpeg_format(args):
    try:
        subprocess.check_output(args,shell=True)
    except Exception as e:
        await youtubedl.finish("ffmpeg错误！\n错误代码是:"+str(e))
