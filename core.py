#!/usr/bin/env python
# coding=utf-8

import os
import asyncio
import hashlib
import logging

import aiofiles
from aiohttp import ClientSession


class Config:
    URLS_DATA = "data.txt"
    PICS_FILENAME_LENGTH = 16
    PICS_EXT = ".jpg"
    PICS_DIR = "pics"

    # 每次请求超时时间（秒）
    REQUEST_TIMEOUT = 60
    # 每次请求延迟（秒）
    DELAY_TIME = 0.25
    # 最大并发数，尽量不要设置得过大
    MAX_CONNECT_COUNT = 64
    # 单任务爬取数
    MAX_NUMBER = 10000
    # 日志等级
    LOG_LEVEL = logging.INFO

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    )


CONFIG = Config()


def get_logger():
    """
    获取 logger 实例
    """
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    logger = logging.getLogger("monitor")
    logger.setLevel(CONFIG.LOG_LEVEL)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


LOGGER = get_logger()


def get_headers(url):
    """
    根据对应 url 返回 headers
    """
    if url.startswith("http://i.meizitu.net/"):
        return {"User-Agent": CONFIG.USER_AGENT, "Referer": "http://www.mzitu.com"}
    if url.startswith("http://img.mmjpg.com/"):
        return {"User-Agent": CONFIG.USER_AGENT, "Referer": "http://www.mmjpg.com"}


def get_urls():
    """
    获取所有 url
    """
    with open(CONFIG.URLS_DATA, "r", encoding="utf8") as f:
        for u in f.readlines():
            yield u.strip()


def create_dir():
    """
    如果文件夹不存在，则创建文件夹
    """
    if not os.path.exists(CONFIG.PICS_DIR):
        os.mkdir(CONFIG.PICS_DIR)


async def download(sem, url, session):
    """
    异步获取请求数据

    :param sem: Semaphore 实例
    :param url: 请求链接
    :param session: Session 实例
    """
    try:
        file_name = hashlib.sha224(url.encode("utf8")).hexdigest()[
            :CONFIG.PICS_FILENAME_LENGTH
        ] + CONFIG.PICS_EXT
        file_path = os.path.join(CONFIG.PICS_DIR, file_name)
        if os.path.exists(file_path):
            LOGGER.info("Ignore: {} has existed".format(file_path))
            return
        await asyncio.sleep(CONFIG.DELAY_TIME)
        async with sem:
            async with session.get(
                url, headers=get_headers(url), timeout=CONFIG.REQUEST_TIMEOUT
            ) as response:
                data = await response.read()
            async with aiofiles.open(file_path, mode="ab") as f:
                await f.write(data)
                LOGGER.info("Save: {}".format(file_path))
    except Exception:
        LOGGER.error("Url: {} download failed".format(url))


async def run(urls):
    """
    运行主函数
    """
    # 创建 Semaphore 实例
    sem = asyncio.Semaphore(CONFIG.MAX_CONNECT_COUNT)

    # 创建可复用的 Session，减少开销
    async with ClientSession() as session:
        tasks = [asyncio.ensure_future(download(sem, url, session)) for url in urls]
        await asyncio.wait(tasks)


if __name__ == "__main__":
    create_dir()
    pic_urls = list(get_urls())
    loop = asyncio.get_event_loop()
    for i in range(int(len(pic_urls) / CONFIG.MAX_NUMBER) + 1):
        loop.run_until_complete(
            asyncio.wait(
                [run(pic_urls[i * CONFIG.MAX_NUMBER:(i + 1) * CONFIG.MAX_NUMBER])]
            )
        )
