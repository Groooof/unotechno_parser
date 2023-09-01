import logging
import traceback
from dataclasses import asdict
from pprint import pprint
from urllib.parse import urljoin, urlparse

import pandas as pd

import settings
from src import api, pages

logging.basicConfig(
    level=logging.INFO,
    filename="log.log",
    filemode="w",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

api = api.UnotechnoApi()

main_page_html = api.get_main_page()


main_page = pages.MainPage(main_page_html)

categories = main_page.get_categories()


for category in categories:
    data = []
    logging.info(f"Parse category {category.name}")

    try:
        category_page_html = api.get_category_page(category.rel_url, items_per_page=30)
    except Exception as ex:
        print(".!.")
        logging.warn(f"Failed to get category page ({category.name})")
        continue

    try:
        category_page = pages.CategoryPage(category_page_html)
    except Exception as ex:
        print(".!.")
        logging.warn(f"Failed to parse category page ({category.name})")
        continue

    try:
        pages_count = category_page.get_pages_count()
    except Exception as ex:
        print(".!.")
        logging.warn(f"Failed to parse category pages count ({category.name})")
        continue

    logging.info(f"Category have {pages_count} pages with 30 items per page")
    logging.info(f"Total: {pages_count * 30} items")
    products_urls = []
    for page in range(1, pages_count + 1):
        logging.info(f"Parse {page} page")

        try:
            category_page_html = api.get_category_page(
                category.rel_url, page=page, items_per_page=30
            )
        except Exception as ex:
            print(".!.")
            logging.warn(f"Failed to get products page {page} ({category.name})")
            continue

        try:
            category_page = pages.CategoryPage(category_page_html)
            curr_page_products_urls = category_page.get_products_urls()
            products_urls.extend(curr_page_products_urls)
        except Exception as ex:
            print(".!.")
            logging.warn(1, traceback.format_exc())
            continue
        logging.info(f"Found {len(curr_page_products_urls)} items on this page")

    logging.info("Parse items")
    for product_url in products_urls:
        logging.info(
            f"Parse item\n{urljoin(settings.UNOTECHNO_MAIN_LINK, product_url)}"
        )

        try:
            product_page_html = api.get_product_page(product_url)
            product_page = pages.ProductPage(product_page_html)

            slug = urlparse(product_url).path.split("/")[-2]
            name = product_page.get_product_name()
            article = product_page.get_article()
            images = list(product_page.get_images_urls())
            in_stock = product_page.get_in_stock_status()
            price = product_page.get_price()
            price_with_sale = product_page.get_price_with_sale()
            short_desc = product_page.get_short_desc()
            characs = product_page.get_characteristics()
            mods = product_page.get_product_modifications()
            delivery = product_page.get_delivery_info()
            full_desc = product_page.get_full_desc()
            full_desc_html = product_page.get_full_desc(
                type=pages.ProductFullDescViewType.html
            )

            data_row = {}
            data_row["Ссылка"] = urljoin(settings.UNOTECHNO_MAIN_LINK, product_url)
            data_row["slug"] = slug
            data_row["Наименование"] = name
            data_row["Артикул"] = article
            for i, image in enumerate(images, start=1):
                data_row[f"Изобр. {i} (ориг)"] = image.orig_url
                data_row[f"Изобр. {i} (мин)"] = image.small_url

            data_row["В наличии"] = in_stock
            data_row["Цена"] = price
            data_row["Цена со скидкой"] = price_with_sale if price_with_sale else price
            data_row["Короткое описание"] = short_desc
            for charac in characs:
                data_row[f"Характеристика: {charac.name}"] = charac.value
            data_row["Модификации"] = list(map(asdict, mods))
            data_row["Доставка"] = list(map(asdict, delivery))
            data_row["Полное описание (текст)"] = "\n".join(full_desc)
            data_row["Полное описание (html)"] = full_desc_html

        except Exception as ex:
            print(".!.")
            logging.warn(2, traceback.format_exc())
            continue

        data.append(data_row)

    try:
        df = pd.DataFrame(data=data)
        df.to_excel(f"{category.name.strip().lower()}.xlsx", index=False)
    except Exception as ex:
        print(".!.")
        logging.warn(3, traceback.format_exc())
        continue

    logging.info(f"Category {category.name} parsed succesfull!")
