import typing as tp
from dataclasses import dataclass
from urllib.parse import urlparse

from lxml import html as _html


class BasePage:
    """
    Базовый класс для парсинга страниц.
    Принимает html в виде строки либо уже
    подготовленного объекта lxml.html.HtmlElement
    """

    def __init__(self, html: tp.Union[str, _html.HtmlElement]) -> None:
        self.dom = (
            html if isinstance(html, _html.HtmlElement) else _html.fromstring(html)
        )
        self.xpath_begin = "." if isinstance(html, _html.HtmlElement) else ""

    def find_element(self, xpath) -> tp.Optional[tp.Union[_html.HtmlElement, str]]:
        """
        Поиск одного элемента под заданному выражению xpath.
        Если элементов несколько - возвращает первый из них.
        Если ничего не найдено - возвращает пустую строку
        """
        elems = self.find_elements(xpath)
        elem = elems[0] if len(elems) > 0 else None
        # return elem if elem else None
        return elem

    def find_elements(self, xpath) -> tp.List[tp.Union[_html.HtmlElement, str]]:
        """
        Поиск нескольких элементов по заданному выражению xpath.
        Если ничего не найдено - возвращает пустой список.
        """
        return self.dom.xpath(self.xpath_begin + xpath)


@dataclass
class Category:
    name: str
    rel_url: str

    def __str__(self) -> str:
        return f"{self.name} {self.rel_url}"


class CategoryElem(BasePage):
    def get_rel_url(self):
        xpath = "/@href"
        elem = self.find_element(xpath)
        return elem

    def get_name(self):
        xpath = '/span[contains(@class, "categories-v__title")]/text()'
        elem = self.find_element(xpath)
        return elem


class MainPage(BasePage):
    def get_categories(self) -> tp.List[Category]:
        xpath = '(//div[contains(@class, "categories-v__menu ")])[1]/div[contains(@class, "categories-v__item")]/span[@class="categories-v__item-inner"]/a[contains(@class, "categories-v__link--with-subs")]//span[@class="categories-v__title" and not(text() = "Горячее" or text() = "Бренды")]/..'
        cats_elems = self.find_elements(xpath)
        cats_pages = map(CategoryElem, cats_elems)
        cats = [
            Category(name=cat_page.get_name(), rel_url=cat_page.get_rel_url())
            for cat_page in cats_pages
        ]
        return cats


class CategoryPage(BasePage):
    def get_pages_count(self) -> int:
        xpath = '(//div[contains(@class, "js-paging-nav")]/ul[contains(@class, "js-pagination")]/li/a[not (@class = "inline-link")])[last()]/text()'
        elem = self.find_element(xpath)
        return int(elem) if elem is not None else 1

    def get_products_urls(self) -> tp.List[str]:
        xpath = '//div[contains(@class, "product-list")]/div[@class = "product-tile__outer"]//div[@class = "product-tile__name"]/a/@href'
        elems = self.find_elements(xpath)
        return elems


@dataclass
class ProductModificationValue:
    name: str
    rel_url: str

    def __str__(self) -> str:
        return f"{self.name} ({self.rel_url})"


@dataclass
class ProductModification:
    name: str
    values: tp.List[ProductModificationValue]

    def __str__(self) -> str:
        return f"{self.name} {self.values}"


class ProductModificationValueElem(BasePage):
    def get_name(self):
        xpath = '/div[contains(@class,"product-modifications__value")]/span[@class="product-modifications__name"]/text()'
        elem = self.find_element(xpath)
        return elem

    def get_rel_url(self):
        xpath = "/@href"
        elem = self.find_element(xpath)
        rel_url = urlparse(elem).path
        return rel_url


class ProductModificationElem(BasePage):
    def get_name(self):
        xpath = '/div[@class="product-modifications__name"]/text()'
        elem = self.find_element(xpath)
        return elem.strip(":")

    def get_values(self):
        xpath = '/div[@class="product-modifications__values"]/a'
        for elem in self.find_elements(xpath):
            product_modifications_value_elem = ProductModificationValueElem(elem)
            yield ProductModificationValue(
                name=product_modifications_value_elem.get_name(),
                rel_url=product_modifications_value_elem.get_rel_url(),
            )


class ProductPage(BasePage):
    def get_images_urls(self):
        xpath = ""
        elems = self.find_elements(xpath)
        return elems

    def get_article(self):
        xpath = ""
        elem = self.find_element(xpath)
        return elem

    def get_in_stock_status(self):
        xpath = ""
        elem = self.find_element(xpath)
        return elem

    def get_price(self):
        xpath = ""
        elem = self.find_element(xpath)
        return elem

    def get_short_desc(self):
        xpath = ""
        elem = self.find_element(xpath)
        return elem

    def get_characteristics(self):
        xpath = ""
        elem = self.find_element(xpath)
        return elem

    def get_delivery_info(self):
        xpath = ""
        elem = self.find_element(xpath)
        return elem

    def get_product_modifications(self):
        xpath = '//div[@class="product-modifications"]/div[@class="product-modifications__item"]'

        for elem in self.find_elements(xpath):
            product_modification_elem = ProductModificationElem(elem)
            yield ProductModification(
                name=product_modification_elem.get_name(),
                values=list(product_modification_elem.get_values()),
            )
