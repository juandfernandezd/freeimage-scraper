import os
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from connection import (init_db, insert_images)

BASE_URL = f'https://www.freeimages.com'
load_dotenv()


def prepare_site(*, headless: bool = True):
    search_page = BASE_URL + '/signin'
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument('--headless')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    driver.get(search_page)
    time.sleep(3)
    return driver


def do_login():
    username = os.getenv("USERNAME", 'example@example.com')
    password = os.getenv("PASSWORD", 'example')
    driver = prepare_site()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signin-form"))
    )
    if element:
        username_field = driver.find_element(By.ID, 'username-input')
        username_field.send_keys(username)
        password_field = driver.find_element(By.ID, 'password-input')
        password_field.send_keys(password)
        login_button = driver.find_element(By.ID, 'btn-signin-submit')
        login_button.click()
        time.sleep(3)


def get_page_content(page: int):
    search_page = BASE_URL + f'/search/dogs/{page}'
    response = requests.get(search_page)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_urls_from_page(page: int):
    page_content = get_page_content(page=page)
    main_div = page_content.find('div', class_='grid-container')
    urls = []
    if main_div:
        all_images = main_div.find_all('img', class_='grid-thumb')
        urls = [(img['src'],) for img in all_images]
    return urls


def get_and_save_urls():
    page = 1
    count_urls = 0
    max_urls = 1000
    conn, cursor = init_db()

    while count_urls < max_urls:
        new_urls = get_urls_from_page(page=page)
        insert_images(conn, cursor, new_urls)
        count_urls += len(new_urls)
        page += 1

    images_count = next(cursor.execute('SELECT COUNT(*) FROM images'))
    print(f'images_count: {images_count}')
    conn.close()


if __name__ == '__main__':
    do_login()
    get_and_save_urls()
