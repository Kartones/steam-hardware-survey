from scrapper import Scrapper

if __name__ == "__main__":
    scrapper = Scrapper()
    html_content = scrapper.fetch()
    scrapper.parse(html_content)
