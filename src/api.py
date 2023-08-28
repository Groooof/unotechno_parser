from urllib.parse import urljoin

import requests as r


class UnotechnoApi:
    main_url = "https://unotechno.ru/"
    base_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Host": "unotechno.ru",
        "Referer": "https://unotechno.ru/category/smartfony/",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
    }
    base_cookies = {
        "landing": "/",
        "_ga": "GA1.2.748131281.1693217040",
        "_ga_9YCTVH42F3": "GS1.1.1693220391.2.0.1693220463.0.0.0",
        "_ga_SVDHTZGFBW": "GS1.1.1693220391.2.0.1693220391.0.0.0",
        "_gid": "GA1.2.887488653.1693217046",
        "adtech_uid": "7712a3fb-7f05-4f0a-a759-ca06e9a6b661:unotechno.ru",
        "cityselect__city": "Ð\u009cÐ¾Ñ\u0081ÐºÐ²Ð°",
        "cityselect__region": "77",
        "cityselect__zip": "101000",
        "last_visit": "1693209591118::1693220391118",
        "PHPSESSID": "67a2068a5450200bb85240bd009b82c3",
        "popup_advert_tabu": "1",
        "referer": "https://www.google.com/",
        "t3_sid_7211523": "s1.830318900.1693220391117.1693220635310.2.3",
        "top100_id": "t1.7211523.465721768.1693217039915",
        "viewed_list": "12991",
        "widget_popup_advert_close_2": "1",
    }

    def __init__(self) -> None:
        pass

    def get_main_page(self) -> str:
        url = self.main_url
        resp = r.get(url, headers=self.base_headers, cookies=self.base_cookies)

        return resp.text

    def get_category_page(
        self, rel_url: str, items_per_page: int = 90, page: int = 1
    ) -> str:
        cookies = {"products_per_page": str(items_per_page)}
        cookies.update(self.base_cookies)
        params = {"page": str(page)}
        url = urljoin(self.main_url, rel_url)
        resp = r.get(
            url,
            cookies=cookies,
            params=params,
            headers=self.base_headers,
        )

        return resp.text

    def get_product_page(self, rel_url: str):
        url = urljoin(self.main_url, rel_url)
        resp = r.get(url, headers=self.base_headers, cookies=self.base_cookies)

        return resp.text
