import requests
import config.base
from bs4 import BeautifulSoup


class Scrapper:

    @staticmethod
    def fetch() -> str:
        try:
            response = requests.get(config.base.STEAM_SURVEY_URL, timeout=15)
            return response.text
        except (Exception) as e:
            raise ValueError(str(e))

    @staticmethod
    def parse(html: str):
        soup = BeautifulSoup(html, "html.parser")
        fragment = soup.find(id="sub_stats")

        table_headers = fragment.find_all("div", class_="substats_col_left col_header")

        for child in fragment.children:
            print(child)

        flag = True
        # while flag:
        #    sibiling = fragment.next_sibling
        #    if sibiling is None:
        #        flag = False

        # print(fragment[1].prettify())
