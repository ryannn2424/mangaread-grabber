from playwright.sync_api import sync_playwright
import requests
import os
from bs4 import BeautifulSoup
import zipfile
import io

def save_as_image_dir(path: str, image_datas: list):
    os.makedirs(path, exist_ok=True)
    for index, image_data in enumerate(image_datas):
        with open(f"{path}/{index}.jpeg", "wb") as file:
            file.write(image_data)

def save_as_cbz(path: str, image_datas: list):
    if not path.endswith('.cbz'):
        path += '.cbz'
    
    with zipfile.ZipFile(path, 'w') as zip_file:
        for index, image_data in enumerate(image_datas):
            img_name = f"{index:03d}.jpeg"
            zip_file.writestr(img_name, image_data)
    

def download_single_chapter(page, url: str, chapter_path: str, save_type: str = "image_dir"):
    page.goto(url, wait_until="load")
    html = page.content()

    soup = BeautifulSoup(html, features="html.parser")
    target = soup.find(class_="reading-content")

    images = target.find_all("img")
    images_data = []
    for image in images:
        images_data.append(requests.get(image["src"][7:]).content)

    if save_type == "image_dir":
        save_as_image_dir(chapter_path, images_data)
    elif save_type == "cbz":
        save_as_cbz(chapter_path, images_data)

def download_chapters(chapters_list: list, chapters_path: str, save_type: str = "image_dir"):
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=True)
        page = browser.new_page()

        for chapter in chapters_list:
            download_single_chapter(
                page = page,
                url = chapter.chapter_link,
                chapter_path = f'{chapters_path}/Chapter {chapter.chapter_number}',
                save_type = save_type
                )
