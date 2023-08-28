from dataclasses import asdict
from pprint import pprint

from src import api, pages

api = api.UnotechnoApi()

main_page_html = api.get_main_page()


main_page = pages.MainPage(main_page_html)

categories = main_page.get_categories()


for category in categories:
    print(category)
    category_page_html = api.get_category_page(category.rel_url, items_per_page=90)
    category_page = pages.CategoryPage(category_page_html)
    pages_count = category_page.get_pages_count()

    products_urls = []
    for page in range(1, pages_count + 1):
        category_page_html = api.get_category_page(
            category.rel_url, page=page, items_per_page=90
        )
        category_page = pages.CategoryPage(category_page_html)

        curr_page_products_urls = category_page.get_products_urls()
        products_urls.extend(curr_page_products_urls)
        print(f"page {page}, products {len(curr_page_products_urls)}")
        break

    for product_url in products_urls:
        product_page_html = api.get_product_page(product_url)
        product_page = pages.ProductPage(product_page_html)

        # with open("t_html.txt", "w") as f:
        #     f.write(product_page_html)

        name = product_page.get_product_name()
        article = product_page.get_article()
        images = list(product_page.get_images_urls())
        in_stock = product_page.get_in_stock_status()
        price = product_page.get_price()
        short_desc = product_page.get_short_desc()
        characs = product_page.get_characteristics()
        mods = product_page.get_product_modifications()

        pprint(f"Article: {article}")
        pprint(f"In stock: {in_stock}")
        pprint(f"Price: {price}")
        pprint(f"Short desc: {short_desc}")
        print("Images:")
        pprint(list(map(asdict, images)))
        print("Characs:")
        pprint(list(map(asdict, characs)))
        print("Mods:")
        pprint(list(map(asdict, mods)))

        break
    break
