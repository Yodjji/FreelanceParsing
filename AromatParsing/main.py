import requests
import time
import csv
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class Katalog:
    def __init__(self, url, headers) -> None:
        self.url = url
        self.headers = headers

    def write_page_in_file(self) -> None:
        req = requests.get(self.url, headers=self.headers)
        src = req.text
        with open("index.html", "w") as file:
            file.write(src)

    def get_soup(self) -> object:
        with open("index.html") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        return soup


class Page:
    def __init__(self, soup) -> None:
        self.soup = soup
    
    def get_hrefs(self) -> None:
        os.mkdir("./Products")
        all_hrefs = []
        all_cards = self.soup.find("div", class_="catalog_block")
        all_products = all_cards.find_all(class_="item_block")
        for item in all_products:
            item_name = item.find("a", class_="js-notice-block__title").find("span").text
            item_href = item.find("a", class_="js-notice-block__title")["href"]
            item_href = f"https://aromat.market{item_href}"
            with open(f"./Products/index.html", "w") as file:
                src_1 = requests.get(item_href)
                file.write(src_1.text)

            with open(f"./Products/index.html", "r") as file:
                src_2 = file.read()
            soup_2 = BeautifulSoup(src_2, "lxml")
            item_photo_a_tag = soup_2.find("a", class_="product-detail-gallery__link")['href']
            item_photo_url = f"https://aromat.market{item_photo_a_tag}"

            all_hrefs.append(
                {
                    "Name": item_name,
                    "Photo_URL": item_photo_url
                }
            )

        print(all_hrefs)
          


def main() -> None:
    start_time = time.time()
    ua = UserAgent()
    headers = {
        "Accept": "*/*",
        "User-Agent": f"{ua.random}"
    }
    url = "https://aromat.market/catalog/smesi_efirnykh_masel/?SHOWALL_1=1"
    
    katalog = Katalog(url, headers)
    print(f"Обрабатываю страничку {url}...")
    katalog.write_page_in_file()
    soup = katalog.get_soup()

    product_page = Page(soup)
    product_page.get_hrefs()
    finish_time = float((time.time() - start_time))
    print(f"Время, затраченное на парсинг: {finish_time}")


if __name__ == "__main__":
    main()
