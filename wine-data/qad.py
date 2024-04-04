"""
Quick & dirty script to scrape data from the bordeauxindex wine site.
This just gets the table the market landing pages and processes it's rows.

Requirements:
    - The script should extract the following columns: Vintage, Wine Name, Wine Details,
      Case Description, Last Trade per Case, Sell Qty, Bid per Case, Spread, Offer per Case, Buy Qty
    - Save the data in a CSV format
    - You don't have to run the script all the way and collect the data. I can do that.
"""

import csv
import requests
from bs4 import BeautifulSoup

URL = "https://bordeauxindex.com/livetrade/marketplace"

page = requests.get(URL, timeout=10)
table = BeautifulSoup(page.content, "html.parser").find("table", id="tblMarketPlace")
col_headers = [
    "Vintage",
    "Wine Name",
    "Wine Details",
    "Case Description",
    "Last Trade per Case",
    "Sell Qty",
    "Bid per Case",
    "Spread",
    "Offer per Case",
    "Buy Qty",
]


def button_packsize(col):
    """The buy & sell cols have a single button with data-packsize attribute"""
    button = col.find("button", class_="open-trade")
    if button is None:
        return ""
    return button.attrs["data-packsize"].strip()


def data_from_row(cols):
    """
    The classic brittle part, mapping specific columns (and potentially deeper dom element)
    to the required fields
    """
    vintage = cols[1].text.strip()
    name = cols[2].find("span", class_="product-name").text.strip()
    case_description = cols[4].text.strip()
    spread = cols[10].text.strip()
    bid = cols[9].text.strip()
    offer = cols[11].text.strip()

    details = cols[2].find("span", class_="subscript")
    for span in details.find_all("span", class_="hide-tablet-landscape"):
        span.decompose()
    details = details.text.strip()

    last_trade = cols[5]
    for span in last_trade.find_all("span"):
        span.decompose()
    for span in last_trade.find_all("br"):
        span.decompose()
    last_trade = last_trade.text.strip()

    sell_qty = button_packsize(cols[6])
    buy_qty = button_packsize(cols[6])

    return [
        vintage,
        name,
        details,
        case_description,
        last_trade,
        sell_qty,
        bid,
        spread,
        offer,
        buy_qty,
    ]


with open("wines.csv", mode="w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(col_headers)

    for row in table.tbody.find_all("tr"):
        columns = row.find_all("td")
        if columns != []:
            writer.writerow(data_from_row(columns))
