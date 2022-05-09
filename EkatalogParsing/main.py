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
       
    def get_page_category(self) -> str:
        active_category = self.soup.find("a", class_="selected").text
        return active_category

    def get_sup_category(self) -> str:
        sup_category = self.soup.find("h1", class_="t2").text
        return sup_category

    def get_characters(self) -> list:
        os.mkdir("./Products")
        all_products = self.soup.find_all(class_="list-item--goods-group")
        all_list_products = []
        products = []
        for item in all_products:
            item_name = item.find("a", class_="no-u")['href']
            with open(f"./Products/{item_name}", "w") as file:
                item_name = f"https://kz.e-katalog.com{item_name}"
                src_1 = requests.get(item_name)
                file.write(src_1.text)
            
            item_name = item.find("a", class_="no-u")['href']
            with open(f"./Products/{item_name}", "r") as file:
                src_2 = file.read()
            soup_2 = BeautifulSoup(src_2, "lxml")
            all_info = soup_2.find_all("div", class_="m-s-f3")                
            all_list_products.append([el['title'].replace("\xa0", "") for el in all_info])
        
            product_info = ""
            for el in all_list_products:
                product_info = el

            all_products = self.soup.find_all(class_="list-item--goods-group")
            item_name = item.find("a", class_="no-u")
            item_photo_src = item.find("img")["src"]
            photo_src = f"https://kz.e-katalog.com{item_photo_src}"
            products.append(
                {
                    "Name": item_name.text,
                    "Photo_URL": photo_src,
                    "All_product_info": product_info
                }
            )
        return products

    def write_in_csv(self, products, first_cat, second_cat, page) -> str:
        os.mkdir("./CSV")
        CSV_name = f"./CSV/{first_cat}-{second_cat}-{page}.csv"
        with open(CSV_name, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    "Name",
                    "Photo_URL",
                    "All_product_info"
                )
            )
            writer.writerows(
                (
                    [el.values() for el in products]
                )
            )
        return CSV_name
          


def main() -> None:
    start_time = time.time()
    ua = UserAgent()
    headers = {
        "Accept": "*/*",
        "User-Agent": f"{ua.random}"
    }
    url = "https://kz.e-katalog.com/list/298/"
    
    katalog = Katalog(url, headers)
    print(f"Обрабатываю страничку {url}...")
    katalog.write_page_in_file()
    soup = katalog.get_soup()

    pages_count = int(soup.find("div", class_="page-num").find_all("a")[-1].text)
    for page in range(0, pages_count - 1):
        url = f"https://kz.e-katalog.com/list/298/{page}"
        katalog = Katalog(url, headers)
        print(f"Обрабатываю страничку {url}...")
        katalog.write_page_in_file()
        soup = katalog.get_soup()

        product_page = Page(soup)
        first_category = product_page.get_page_category()
        second_category = product_page.get_sup_category()
        print(f"Обрабатываю много страничек c URL:{url}... Подождите, пожалуйста!")
        characters = product_page.get_characters()
        print(f"Файл {product_page.write_in_csv(characters, first_category, second_category, page)} записан!")
        finish_time = (time.time() - start_time) / 60.0
        print(f"Время, затраченное на парсинг - {finish_time}")


if __name__ == "__main__":
    main()
