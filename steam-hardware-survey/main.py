from scrapper import Scrapper

if __name__ == "__main__":
    scrapper = Scrapper()
    html_content = scrapper.fetch()
    data = scrapper.parse(html_content)
    scrapper.write_csv(data)
