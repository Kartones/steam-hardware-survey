import csv
from os import path
import config.base
from typing import List

from bs4 import BeautifulSoup
import requests


class Scrapper:

    @staticmethod
    def fetch() -> str:
        try:
            response = requests.get(config.base.STEAM_SURVEY_URL, timeout=15)
            return response.text
        except (Exception) as e:
            raise ValueError(str(e))

    @classmethod
    def is_header_column(cls, element) -> bool:
        if element.name != "div":
            return False

        elementClasses = element.get("class", [])
        return "col_header" in elementClasses or \
               "substats_col_month_last_pct col_header" in elementClasses or \
               "substats_col_month_last_chg" in elementClasses

    @classmethod
    def is_row(cls, element) -> bool:
        if element.name != "div":
            return False

        elementClasses = element.get("class", [])
        return "substats_row" in elementClasses

    @classmethod
    def process_row(cls, row) -> List[str]:
        row_data = []
        row_divs = row.find_all("div")
        for div in row_divs:
            if div.get("class") == ["substats_col_left"]:
                continue
            row_data.append(div.text.lower())

        # last row has different format so the first column won't be automatically added
        if len(row_data) == 6:
            row_data.insert(0, "other")
        return row_data

    @classmethod
    def write_csv(cls, data) -> None:
        file_path = path.join(
            path.dirname(path.dirname(path.abspath(__file__))),
            "data",
            config.base.STEAM_SURVEY_CSV_FILE
        )

        with open(file_path, "w", newline="") as csv_file_handle:
            csv_writer = csv.writer(
                csv_file_handle,
                delimiter=config.base.CSV_SEPARATOR,
                quotechar=config.base.CSV_QUOTE_CHAR,
                quoting=csv.QUOTE_ALL
            )
            for row in data:
                csv_writer.writerow(row)

    @classmethod
    def parse(cls, html: str) -> List[List[str]]:
        soup = BeautifulSoup(html, "html.parser")
        # main container
        fragment = soup.find(id="sub_stats")

        # header of the "all video cards" table
        # table_headers = fragment.find_all("div", class_="substats_col_left col_header")
        # content are divs of class `substats_row`, but not all, only after the header block
        # ends when the next item is a `<br clear="all">`

        rows: List[List[str]] = []
        currentRow: List[str] = []

        readingHeader = False
        readingRows = False
        for child in fragment.children:
            # skip empty tags
            if child.name is None:
                continue

            if readingHeader:
                if cls.is_header_column(child):
                    name = child.text.lower()
                    if name.startswith("\xa0"):
                        name = "delta"
                    currentRow.append(name)
                else:
                    readingHeader = False
                    rows.append(currentRow)
                    currentRow = []
                    # note that order matters, if we were reading the header and is not a header "column", need to
                    # mark state as reading rows and try to read as a row
                    readingRows = True

            if readingRows:
                if cls.is_row(child):
                    currentRow = cls.process_row(child)
                    rows.append(currentRow)
                    currentRow = []
                else:
                    readingRows = False
                    # always end after the first table
                    break

            if child.name == "div" and \
               child.get("class") == ["substats_col_left", "col_header"] and \
               child.text.lower() == "all video cards":
                readingHeader = True
                currentRow.append("video_card")

        return rows
