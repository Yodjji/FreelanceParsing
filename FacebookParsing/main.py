import time
import requests
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_page(url, language, useragent, login, password):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={useragent}")
    options.add_argument(f"accept-language={language}")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    s = Service(executable_path="./ChromeDriver/chromedriver")

    with webdriver.Chrome(service=s, options=options) as driver:
        driver.get(url=url)
        WebDriverWait(driver, 10)

        try:
            cookies_block = driver.find_element(By.XPATH, """//*[@id="facebook"]/body/div[3]/div[2]/div/div/div/div/div[3]""")
            cookies_block = cookies_block.find_element(By.XPATH, value="""/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]""").click()
            WebDriverWait(driver, 10)
        except Exception as ex:
            print(f"Ошибка - {ex}\nНе найден блок с куки!")

        try:
            login_form = driver.find_element(By.ID, "email")
            login_form.clear()
            login_form.send_keys(login)
            password_form = driver.find_element(By.ID, "pass")
            password_form.clear()
            password_form.send_keys(password)

            driver.find_element(By.ID, 'loginbutton').click()
            WebDriverWait(driver, 10)
        except Exception as ex:
            print(ex)

        try:
            time.sleep(0.5)
            global current_url
            current_url = driver.current_url
        except Exception as ex:
            print(ex)

        print("Сохраняю страницу...")
        with open("index.html", "w") as file:
            file.write(driver.page_source)

    with open("index.html", "r") as file:
        src = file.read()
    soup = BeautifulSoup(src, "lxml")

    return soup, current_url


def get_data(current_url, soup) -> None:
    os.mkdir("./Text")
    os.mkdir("./Foto")
    try:
        id = current_url.split("?")[1].split("=")[1]
        with open("./Text/id.txt", "w") as file:
            file.write(id)
        print("Файл id.txt записан!")
    except Exception as ex:
        print(f"Произошла ошибка {ex} ! Файл id.txt не записан!")
        
    try:
        user_photo_url = soup.find("image")['xlink:href']
        response = requests.get(url=str(user_photo_url))

        with open("./Foto/foto.jpg", "wb") as file:
            file.write(response.content)
        print("Фото foto.jpg сохранено!")

        with open("./Text/link.txt", "w") as file:
            file.write(user_photo_url)
        print("Файл link.txt записан!")

    except Exception as ex:
        print(f"Произошла ошибка {ex} ! Файл link.txt не записан! Фото foto.jpg не сохранено!")

    try:
        full_name = soup.find("h1", class_="""gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl""").text.split(" ")[0:2]
        short_name = soup.find("h1", class_="""gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl""").text.split(" ")[0:1]
        full_name = " ".join(full_name)
        short_name = "".join(short_name)

        with open("./Text/full_name.txt", "w") as file:
            file.write(full_name)
        print("Файл full_name.txt записан!")

        with open("./Text/short_name.txt", "w") as file:
            file.write(short_name)
        print("Файл short_name.txt записан!")
    except Exception as ex:
        print(f"Произошла ошибка {ex} ! Файлы full_name.txt и short_name.txt не записаны!")


def main():
    start_time = time.time()
    language = "en-US"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    login = "login"
    password = "password"
    post_request = f"https://facebook.com/profile.php?language={language}&useragent={useragent}&login={login}&password={password}"

    main_url = post_request.split("?")[0]
    post_request_list = post_request.split("?")[1].split("&")
    for item in post_request_list:
        if item.startswith("language"):
            language = item.split("=")[1]
        elif item.startswith("useragent"):
            useragent = item.split("=")[1]
        elif item.startswith("login"):
            login = item.split("=")[1]
        elif item.startswith("password"):
            password = item.split("=")[1]
        else:
            print(f"Не удалось получить параметры с url: {post_request}")

    print(f"Начинаю собирать информацию со страницы {post_request} ...")
    soup, current_url = get_page(main_url, language, useragent, login, password)
    get_data(current_url, soup)
    finish_time = time.time() - start_time
    print(finish_time)


if __name__ == "__main__":
    main()
