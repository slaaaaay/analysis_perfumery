import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import csv

with open('perfume_test.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Name", "Brand", "Type", "Price", "Rating", "Review", "Year", "Sex", "Group", "Notes", "High notes", "Middle notes", "Base notes", "Perfumer", "Country", "Event"])

URL = "https://randewoo.ru/category/parfyumeriya"
headers = {"User-Agent": "",  # User-Agent вставьте из браузера
           "Cookie": "".encode("utf-8")}  # Cookie вставьте из браузера
headers_catalog = {"User-Agent": "",  # User-Agent вставьте из браузера
           "Cookie": "".encode("utf-8")}  # Cookie вставьте из браузера

session = requests.Session()


def url_f(catalog_url, year, sex, group, note, high_note, middle_note, base_note, perfumer, country,
          event):  # функция для нахождения инфы на страничке самого аромата

    try:
        resp = session.get(catalog_url, headers=headers_catalog)

        soup = BeautifulSoup(resp.text, "lxml")

        info_perfume = soup.find("div", class_="small-tabs__box")
        if info_perfume is not None:
            items_info = info_perfume.select('dl.dl > div')
            data = {}
            for item in items_info:
                # Извлекаем текст из span внутри dt
                theme_text = item.find('span').text

                # Извлекаем текст из dd (игнорируем лишние символы)
                info_text = item.find('dd').text

                # Записываем в словарь
                data[theme_text] = info_text

            year = data.get('Год создания', '')
            sex = data.get('Пол', '')
            group = data.get('Группы', '')
            note = data.get('Ноты', '')
            high_note = data.get('Верхние ноты', '')
            middle_note = data.get('Средние ноты', '')
            base_note = data.get('Базовые ноты', '')
            perfumer = data.get('Парфюмер', '')
            country = data.get('Страна', '')
            event = data.get('Для какого события', '')

        # brand = data.get('Бренд', 'Не указано')

        return catalog_url, year, sex, group, note, high_note, middle_note, base_note, perfumer, country, event
    except Exception as e:
        print(f"Ошибка при обработке {catalog_url}: {e}")
        return catalog_url, year, sex, group, note, high_note, middle_note, base_note, perfumer, country, event


for i in tqdm(range(1, 298), mininterval=10):
    items_found = []
    try:
        params = {"page": f"{i + 1}"}

        resp = session.get(URL, params=params, headers=headers)

        soup = BeautifulSoup(resp.text, "lxml")

        all_items = soup.find_all("div", class_="products__innerLink")
        #    if i == 0:
        # all_items = all_items[11:]  # 11: , чтобы избавиться от первых 11 промо-айтемов

        for sample_item in all_items:
            try:
                price_container = sample_item.find("div", class_="products__price")

                if price_container is not None:
                    product_price = price_container.find("b").text
                else:
                    product_price = ''

                # span_container = sample_item.find("div", class_="_3iCDs aP0JE").find("span", class_="ds-valueLine DPiFo") #ds-valueLine ds-valueLine_gap_2

                info_container = sample_item.find("a",
                                                  class_="b-catalogItem__descriptionLink s-link s-link--unbordered")
                if info_container is not None:

                    brand_name = info_container.find("div", class_="b-catalogItem__brand")
                    if brand_name is not None:
                        brand_name = brand_name.text
                    else:
                        brand_name = ''
                    # print(brand_name)

                    product_name = info_container.find("div",
                                                       class_="b-catalogItem__name s-link s-link--unbordered js-product-follow")
                    if product_name is not None:
                        product_name = product_name.text
                    else:
                        product_name = ''
                    # print(product_name)

                    product_type = info_container.find("small", class_="products__hint")
                    if product_type is not None:
                        product_type = product_type.text
                    else:
                        product_type = ''
                    # print(product_type)
                else:
                    brand_name = ''
                    product_name = ''
                    product_type = ''

                rating_container = sample_item.find("div", class_="b-catalogProductRating")

                if rating_container is not None:
                    rating = rating_container.find("div", class_="s-rating s-rating--static")
                    if rating is not None:
                        rating = rating.get("data-rating-value")
                    else:
                        rating = ''
                    # print(rating)

                    n_rates = rating_container.find("span", "b-catalogProductRating__reviewsCount")
                    if n_rates is not None:
                        n_rates = n_rates.text[1:-1]
                    else:
                        n_rates = ''
                # print(n_rates)
                else:
                    rating = ''
                    n_rates = ''

                catalog_container = sample_item.find("a", class_="b-catalogItem__photoWrap js-product-follow")
                if catalog_container is not None:
                    catalog_url = 'https://randewoo.ru/' + catalog_container.get('href')
                    year = ''
                    sex = ''
                    group = ''
                    note = ''
                    high_note = ''
                    middle_note = ''
                    base_note = ''
                    perfumer = ''
                    country = ''
                    event = ''
                    catalog_url, year, sex, group, note, high_note, middle_note, base_note, perfumer, country, event = url_f(
                        catalog_url, year, sex, group, note, high_note, middle_note, base_note, perfumer, country,
                        event)

                items_found.append((product_name, brand_name, product_type, product_price, rating, n_rates, year, sex,
                                    group, note, high_note, middle_note, base_note, perfumer, country, event))
            except Exception as e:
                print(f"Ошибка при обработке элемента {i + 1}: {e}")
                continue

        with open('perfume_data.csv', 'a', encoding='utf-8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(items_found)

        time.sleep(random.uniform(27, 51))

    except Exception as e:
        print(f"Ошибка при загрузке страницы {i + 1}: {e}")
        continue
