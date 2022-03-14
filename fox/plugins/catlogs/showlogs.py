import asyncio
import os
import aiofiles


async def find_new_file(dir):
    '''查找目录下最新的文件'''
    file_lists = os.listdir(dir)
    file_lists.sort(key=lambda fn: os.path.getmtime(dir + "/" + fn)
                    if not os.path.isdir(dir + "/" + fn) else 0)
    file = os.path.join(dir, file_lists[-1])
    return file


async def read_last_line(path, line):
    path = await find_new_file(path)
    async with aiofiles.open(path, "r", encoding='utf-8') as f:
        data = await f.readlines()
        lines = len(data)
    if line > lines:
        line = lines
    text = ""
    for i in range(line):
        text += data[lines-line+i]
    return text