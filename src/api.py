from urllib.parse import urljoin

import requests as r


class UnotechnoApi:
    main_url = "https://unotechno.ru/"

    def __init__(self) -> None:
        pass

    def get_main_page(self) -> str:
        url = self.main_url
        resp = r.get(url)

        return resp.text

    def get_category_page(
        self, rel_url: str, items_per_page: int = 90, page: int = 1
    ) -> str:
        cookies = {"products_per_page": str(items_per_page)}
        params = {"page": str(page)}
        url = urljoin(self.main_url, rel_url)
        resp = r.get(url, cookies=cookies, params=params)

        return resp.text

    def get_product_page(self, rel_url: str):
        url = urljoin(self.main_url, rel_url)
        resp = r.get(url)

        return resp.text
