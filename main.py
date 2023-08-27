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

        p_m = product_page.get_product_modifications()
        print(list(p_m))
        break
