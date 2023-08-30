from dataclasses import asdict
from pprint import pprint
from urllib.parse import urljoin, urlparse

import settings
from src import api, pages

api = api.UnotechnoApi()

main_page_html = api.get_main_page()


main_page = pages.MainPage(main_page_html)

categories = main_page.get_categories()


for category in categories:
    data = []
    print(category)
    category_page_html = api.get_category_page(category.rel_url, items_per_page=90)
    category_page = pages.CategoryPage(category_page_html)
    pages_count = category_page.get_pages_count()

    products_urls = []
    for page in range(1, 2):  # , pages_count + 1):
        print(f"Page {page}")
        category_page_html = api.get_category_page(
            category.rel_url, page=page, items_per_page=30
        )
        category_page = pages.CategoryPage(category_page_html)

        curr_page_products_urls = category_page.get_products_urls()
        products_urls.extend(curr_page_products_urls)
        print(f"page {page}, products {len(curr_page_products_urls)}")
        break

    for product_url in products_urls:
        print(product_url)
        product_page_html = api.get_product_page(product_url)
        product_page = pages.ProductPage(product_page_html)

        # with open("t_html.txt", "w") as f:
        #     f.write(product_page_html)

        slug = urlparse(product_url).path.split("/")[-2]
        name = product_page.get_product_name()
        article = product_page.get_article()
        images = list(product_page.get_images_urls())
        in_stock = product_page.get_in_stock_status()
        price = product_page.get_price()
        short_desc = product_page.get_short_desc()
        characs = product_page.get_characteristics()
        mods = product_page.get_product_modifications()
        delivery = product_page.get_delivery_info()
        full_desc = product_page.get_full_desc()
        full_desc_html = product_page.get_full_desc(
            type=pages.ProductFullDescViewType.html
        )

        data_row = {}
        data_row["url"] = urljoin(settings.UNOTECHNO_MAIN_LINK, product_url)
        data_row["slug"] = slug
        data_row["article"] = article
        data_row["images"] = list(map(asdict, images))
        data_row["in_stock"] = in_stock
        data_row["price"] = price
        data_row["short_desc"] = short_desc
        for charac in characs:
            data_row[charac.name] = charac.value
        data_row["mods"] = list(map(asdict, mods))
        data_row["delivery"] = list(map(asdict, delivery))
        data_row["full_desc"] = "\n".join(full_desc)
        data_row["full_desc_html"] = full_desc_html

        data.append(data_row)
        pprint(data_row)

    # break
