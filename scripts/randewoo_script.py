import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import csv

URL = "https://randewoo.ru/category/parfyumeriya"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0",
    # User-Agent вставьте из браузера (используя инструменты разработчика)
    "Cookie": "utm_params=%5B%7B%22ysclid%22%3A%22macwgjduy0380860872%22%2C%22created_at%22%3A%222025-05-06T19%3A25%3A47.489%2B00%3A00%22%2C%22referer%22%3A%22https%3A%2F%2Fyandex.ru%2F%22%7D%5D; jwtToken=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImV4cCI6MTc3ODA5NTU0NywiaWF0IjoxNzQ2NTU5NTQ3LCJqdGkiOiJmZTM4M2IwOS0wZjIzLTQ1MTItYWQ2YS01MjgyNjgzMmRiNTgiLCJzY3AiOiJhcGlfdjFfY2xpZW50X2d1ZXN0X3VzZXIiLCJzdWIiOiJiY2FhMzFmMi0zYjM1LTQwODMtODE0NC1mNWQ4Yjc1NGJhOTUifQ.puoEIx_oNG6dR2RRLo0-o3IzTa09hn-RV9HRXJj7s_c; subscriber_status=new; deduplication_cookie=direct; _randewoo_session=8c569158d1620e0ba2d8bf1671a25c73; analytics_document_referrer=https://yandex.ru/; firstVisitTime=1746559550249; _userGUID=0:macwgm96:98Po_vrPYNHbKJ_Msdz6Um2aG9DN3ZCd; _userGUID=0:macwgm96:98Po_vrPYNHbKJ_Msdz6Um2aG9DN3ZCd; _ym_uid=1746559551648087234; _ym_d=1746559551; gnezdo_uid=uZQlT2f2FF+76S5gFrY0Ag==; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ga=GA1.1.1367718011.1746559557; tmr_lvid=7521efc3436abbed551e51cc56a6c830; tmr_lvidTS=1746559557117; _pin_unauth=dWlkPU56WXdOMk14TldVdFptSTVaUzAwT0RjMUxXRXhPRFF0WVdObU1UZzFNelUzTmpVNQ; cartHash=50a8228d245944c4735134cfa7164c13; dSesn=47ef5e18-773a-8127-f885-59a76d75d4a4; _dvs=0:mafm7o84:AbhzBRSZRvFrOW1E7wdFli997GZPzZk_; _ym_isad=2; pageCount=5; mindboxDeviceUUID=25dee3c5-a7d0-4fd8-938f-38a58b64c813; directCrm-session=%7B%22deviceGuid%22%3A%2225dee3c5-a7d0-4fd8-938f-38a58b64c813%22%7D; domain_sid=F-ij6c9_Jt4VbCOol-CE9%3A1746723742201; tmr_detect=0%7C1746723744202; last_request=7e9eb426d2874e973b33b8e470b5be17; header_info_message_counter=5; _ga_RN3S387LJ5=GS2.1.s1746723734$o2$g1$t1746723757$j37$l0$h0; _ga_LBDKL5SKRS=GS2.1.s1746723734$o2$g1$t1746723757$j37$l0$h0; digi_uc=|v:174655:450480!174672:60607".encode(
        "utf-8")}  # Cookie вставьте из браузера (используя инструменты разработчика)
headers_catalog = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0",
    # User-Agent вставьте из браузера (используя инструменты разработчика)
    "Cookie": "jwtToken=eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImV4cCI6MTc3ODA5NTU0NywiaWF0IjoxNzQ2NTU5NTQ3LCJqdGkiOiJmZTM4M2IwOS0wZjIzLTQ1MTItYWQ2YS01MjgyNjgzMmRiNTgiLCJzY3AiOiJhcGlfdjFfY2xpZW50X2d1ZXN0X3VzZXIiLCJzdWIiOiJiY2FhMzFmMi0zYjM1LTQwODMtODE0NC1mNWQ4Yjc1NGJhOTUifQ.puoEIx_oNG6dR2RRLo0-o3IzTa09hn-RV9HRXJj7s_c; subscriber_status=new; deduplication_cookie=direct; _randewoo_session=8c569158d1620e0ba2d8bf1671a25c73; analytics_document_referrer=https://yandex.ru/; firstVisitTime=1746559550249; _userGUID=0:macwgm96:98Po_vrPYNHbKJ_Msdz6Um2aG9DN3ZCd; _userGUID=0:macwgm96:98Po_vrPYNHbKJ_Msdz6Um2aG9DN3ZCd; _ym_uid=1746559551648087234; _ym_d=1746559551; gnezdo_uid=uZQlT2f2FF+76S5gFrY0Ag==; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; _ga=GA1.1.1367718011.1746559557; tmr_lvid=7521efc3436abbed551e51cc56a6c830; tmr_lvidTS=1746559557117; _pin_unauth=dWlkPU56WXdOMk14TldVdFptSTVaUzAwT0RjMUxXRXhPRFF0WVdObU1UZzFNelUzTmpVNQ; domain_sid=F-ij6c9_Jt4VbCOol-CE9%3A1746723742201; utm_params=%5B%7B%22ysclid%22%3A%22macwgjduy0380860872%22%2C%22created_at%22%3A%222025-05-06T19%3A25%3A47.489%2B00%3A00%22%2C%22referer%22%3A%22https%3A%2F%2Fyandex.ru%2F%22%7D%2C%7B%22source_category%22%3A%226%22%2C%22preferred%22%3A%2249070%22%2C%22created_at%22%3A%222025-05-09T12%3A43%3A08.637%2B00%3A00%22%7D%5D; _dvs=0:magvlz2i:frSdvlBjIJUnb~Z9FzZNSH8m3Nts8jvN; cartHash=50a8228d245944c4735134cfa7164c13; _ym_isad=2; hide_stickers=true; last_request=e92900ce0c11d793ff1d695ddc9a7821; header_info_message_counter=26; digi_uc=|v:174655:450480!174679:455263:60607:513503!174680:465192:444081:449778:50298; mindboxDeviceUUID=25dee3c5-a7d0-4fd8-938f-38a58b64c813; directCrm-session=%7B%22deviceGuid%22%3A%2225dee3c5-a7d0-4fd8-938f-38a58b64c813%22%7D; pageCount=26; _ga_RN3S387LJ5=GS2.1.s1746799990$o6$g1$t1746800224$j19$l0$h0; _ga_LBDKL5SKRS=GS2.1.s1746799991$o6$g1$t1746800224$j19$l0$h0; tmr_detect=0%7C1746800226967".encode(
        "utf-8")}  # Cookie вставьте из браузера (используя инструменты разработчика)

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


for i in tqdm(range(244, 298), mininterval=10):
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
