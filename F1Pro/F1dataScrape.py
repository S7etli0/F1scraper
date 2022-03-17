import requests
from bs4 import BeautifulSoup as soup


def WebScrape(calendar, sector):
    website = "https://www.formula1.com/en/results.html/{}/{}.html".format(calendar, sector)
    rec = requests.get(website)
    site_html = rec.text
    scrape = soup(site_html, 'lxml')
    table = soup.select(scrape, "tbody>tr")

    return table