from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup, Tag

class Chapter:
    def __init__(
            self,
            chapter_number: int,
            chapter_link: str
            ):
        self.chapter_number = chapter_number
        self.chapter_link = chapter_link

def _get_rendered_html(url: str) -> str:
    with sync_playwright() as play:
        browser = play.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, wait_until="load")

        html = page.content()
        browser.close()
        return html
    
def _parse_ul_element(html_string: str):
    soup = BeautifulSoup(html_string, features="html.parser")
    target = soup.find(class_="main version-chap no-volumn")
    return target

def _get_chapters(target: Tag, chapters: list[Chapter]):
    list_items = target.find_all("li")
    for index, li in enumerate(list_items):
        a_tag = li.find("a")
        if a_tag and a_tag.has_attr("href"):
            chapters.append(
                Chapter(
                    chapter_number = len(list_items) - index,
                    chapter_link = a_tag["href"]
                )
            )
    chapters.reverse()

def get_chapters(url: str) -> list[Chapter]:
    chapters: list[Chapter] = []
    _get_chapters(
        _parse_ul_element(
            _get_rendered_html(url)
        ),
        chapters
    )
    return chapters
