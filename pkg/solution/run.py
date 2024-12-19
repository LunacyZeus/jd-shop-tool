import asyncio
import json
import os
import time

import httpx
import jmespath
from DrissionPage._pages.chromium_page import ChromiumPage
from loguru import logger

from pkg.utils.dp import get_page, test_cdp_connection, record_data


class MainProcess(object):
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.page: ChromiumPage = None
        self.debugger_port = 12345

    async def start_dp(self):
        if not test_cdp_connection(count=2, local_address=f"127.0.0.1:{self.debugger_port}", is_show=False):
            logger.success("浏览器未启动 开始唤起浏览器")
            self.page = get_page(debugger_port=self.debugger_port)
        else:
            logger.success("浏览器已经启动 开始执行后续流程")
            self.page = get_page(debugger_port=self.debugger_port)

    async def login_jd_ht(self):
        # 跳转到京东后台

        cookies = self.page.cookies(as_dict=True)
        print(cookies)
        if "b_belong" not in cookies and "flash" not in cookies:
            url = "https://shop.jd.com"
            logger.error(f"未找到登录ck,开始跳转到登录页->{url}")
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

        if "/sub_item/item/" not in self.page.url:
            logger.debug(f"当前页面不在京东后台,尝试跳转")
            url = "https://vcgoods.jd.com/sub_item/item/initItemListPage?_source=pop"
            self.page.get(url=url)
        else:
            logger.success(f"当前页面已在京东后台,等待后续操作")

        ck = self.page.cookies()
        logger.debug(f"登录会话ck->{ck}")
        record_data("data/ck.json", ck)
        # [{'name': '_base_', 'value': 'YKH2KDFHMOZBLCUV7NSRBWQUJPBI7JIMU5R3EFJ5UDHJ5LCU7R2NILKK5UJ6GLA2RGYT464UKXAI5TPYU4VBBBWDQX6FGO2MU2LUEVZ7M5LEFBINUAUC6ML35K2O6SW2JSPVORIFTBUVPCJUAGQKI352LNKFPOR42WQALLUAOV5DRD6AHODT4JN7KE5J2UD5T3SGLS6K5KW2RKKT6PEDIJOL37SFS6BM5IL564G6RUXQCVML2QXQKCTKHUNMMP6NYBRKHS6ICOXUE3IKDLTLHFGIH4MXQKZLNZ5JRNKW3Z6KPYGEG4MJ77GSNQL52J36M2ODNAT34XEMTJM5F5XBBF73AWOPRE3I62N3O4I4VDWYXVL3FE7UISMMYMZWBO5537EULLGAOCUYHU2UPMD32BSTOFZD7O6YEPHY73PR7RNFOAEYFZTPIGOJWJ27A2LTXY7OOFB5KRNXUSUREOYP23SDSKFJ5WSCGJIBALLJM4GSWYT6UQOSFJTOH6OX3RAP', 'domain': '.jd.com'}, {'name': '__jdc', 'value': '147742768', 'domain': '.jd.com'}, {'name': '__jda', 'value': '147742768.17345889899991180314800.1734588990.1734588990.1734588990.1', 'domain': '.jd.com'}, {'name': '__jdb', 'value': '147742768.9.17345889899991180314800|1.1734588990', 'domain': '.jd.com'}, {'name': 'style_flag', 'value': 'popStyle', 'domain': '.jd.com'}, {'name': '__USE_NEW_PAGEFRAME_VERSION__', 'value': 'v9', 'domain': '.jd.com'}, {'name': 'b-sec', 'value': 'JKOL5T3IHEKACLWGSYJFXVTDNM3IV36JFFFGVXZH44SC3H42DHMQ', 'domain': '.jd.com'}, {'name': 'light_key', 'value': 'AASBKE7rOxgWQziEhC_QY6yaRU4YJHEjBHNWCAEko-vB1GEje7PUKG-6IU3hgkNoREKX9ooC', 'domain': '.jd.com'}, {'name': 'ceshi3.com', 'value': '000', 'domain': '.jd.com'}, {'name': 'flash', 'value': '3_YebykyKLV_41-S-me0xTyMpKGH7sn2ZNM0FECDL9XgRJcH4CJu8L8wCHTBKwvtWyB8btEKgNJFDBb57iqOPxlvJ3CKC6SUHGPRsHonD4_aa9_39w8j4J0vJc1Og5KAe0WsKMoSvQIkV*', 'domain': '.jd.com'}, {'name': 'pin', 'value': 'cdjfjzmj', 'domain': '.jd.com'}, {'name': '_pst', 'value': 'cdjfjzmj', 'domain': '.jd.com'}, {'name': 'thor', 'value': '8C2446B711B9C6F42BEACF3C9B1A6441782D65A2053FE19B1FDCCAD3DB7404022F5C96973CA8C905DF3CECF94152E17BEFA34852CD0B2F39558126270220039D01F329B1FC52223935B900D2090BE1C57B4721630617CF8794B52C97EFB93D99B3B8900F2056CF014240BCFB94A2DC191E0B213133EDB495DC02571F90671D8F21BE90F1E7F884370B3E3C3A8FDCD556', 'domain': '.jd.com'}, {'name': '__USE_NEW_PAGEFRAME__', 'value': 'false', 'domain': '.jd.com'}, {'name': '_tp', 'value': 't%2BM4mfmYDB5BehitgfKXWg%3D%3D', 'domain': '.jd.com'}, {'name': '3AB9D23F7A4B3CSS', 'value': 'jdd03V5UP7YHQNF63BSWXZ6M4OLYBUFPA3OSSZVNLZ7UCUQPAGAPI3MAAD5ESAV5RKUHRZ7W32DMZGO3XZEWG6MAPEGZJLIAAAAMT3WPRHEIAAAAAC7ZHTBJYEV2R4AX', 'domain': '.jd.com'}, {'name': 'language', 'value': 'zh_CN', 'domain': '.jd.com'}, {'name': '3AB9D23F7A4B3C9B', 'value': 'V5UP7YHQNF63BSWXZ6M4OLYBUFPA3OSSZVNLZ7UCUQPAGAPI3MAAD5ESAV5RKUHRZ7W32DMZGO3XZEWG6MAPEGZJLI', 'domain': '.jd.com'}, {'name': 'unick', 'value': 'pr19g30c3cl198', 'domain': '.jd.com'}, {'name': '__jdv', 'value': '95931165|direct|-|none|-|1734588990001', 'domain': '.jd.com'}, {'name': 'VC_INTEGRATION_JSESSIONID', 'value': '6aabf46b-3aa1-4410-9768-d5eaa9d49d89', 'domain': '.jd.com'}, {'name': 'TrackID', 'value': '1jzHorrQ_LZJsSTbZ8PfoG4jl3mJJYpc-FUjNgmuVmPx_xCHSMZwAdf8IkA2oEXpm', 'domain': '.jd.com'}, {'name': 'pinId', 'value': 'yxfIdvvkpu-1ffsfn98I-w', 'domain': '.jd.com'}, {'name': 'wlfstk_smdl', 'value': '0fpsu0x3dloh1e50lzb8cxcsibco7rf7', 'domain': '.jd.com'}, {'name': '__jdu', 'value': '17345889899991180314800', 'domain': '.jd.com'}]

    async def run(self):
        await self.start_dp()
        await self.login_jd_ht()


async def main():
    process = MainProcess()
    await process.run()


def start_run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
