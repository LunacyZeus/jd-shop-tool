import asyncio
import json
import os
import time

import httpx
import jmespath
from DrissionPage._pages.chromium_page import ChromiumPage
from loguru import logger

from pkg.utils.dp import get_page, test_cdp_connection


class MainProcess(object):
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.page: ChromiumPage = None
        self.debugger_port = 12345

    async def start_dp(self):
        if not test_cdp_connection(count=3, local_address=f"127.0.0.1:{self.debugger_port}", is_show=False):
            logger.success("浏览器未启动 开始唤起浏览器")
            self.page = get_page(debugger_port=self.debugger_port)
        else:
            logger.success("浏览器已经启动 开始执行后续流程")
            self.page = get_page(debugger_port=self.debugger_port)

    async def login_jd_ht(self):
        # 跳转到京东后台
        if "/sub_item/item/" not in self.page.url:
            logger.debug(f"当前页面不在京东后台,尝试跳转")
            url = "https://vcgoods.jd.com/sub_item/item/initItemListPage?_source=pop"
            self.page.get(url=url)
            while 1:
                cookies = self.page.cookies(as_dict=True)
                print(cookies)
                if "b_belong" not in cookies and "flash" not in cookies:
                    logger.error(f"未找到登录ck,请手动扫码登录")
                    await asyncio.sleep(15)
                    continue
                break

            logger.success(f"登录后台成功")
        else:
            logger.success(f"当前页面已在京东后台,等待后续操作")

    async def run(self):
        await self.start_dp()

        await self.login_jd_ht()


async def main():
    process = MainProcess()
    await process.run()


def start_run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
