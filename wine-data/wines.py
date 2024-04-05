"""
This version is a more complete version that gets all the available wine data from the
bordeauxindex.com site. The 'infinite scroll' feature uses the livetrade/next-page end-point
to further extend the table as you scroll down

So here we are using the endpoint to incrementally get all pages and append them to our csv file
"""

import csv
import requests
from bs4 import BeautifulSoup


URL = "https://bordeauxindex.com/livetrade/next-page"


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


headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "cookie": "see-readme",
    "x-xsrf-token": "see-readme",
}

# there are usually more than 50 pages, for testing purposes make this >= 50
next_page = "1"

with open("wines.csv", mode="w", encoding="utf8") as file:
    writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(
        [
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
    )

    while next_page is not None:
        print(f"getting page: {next_page}")
        response = requests.post(
            URL,
            headers=headers,
            json={"page": next_page},
        )
        data = response.json()

        if "marketRows" in data:
            soup = BeautifulSoup(data["marketRows"], "html.parser")
            next_page = data["nextPage"]

            for row in soup.find_all("tr"):
                columns = row.find_all("td")
                if columns != []:
                    writer.writerow(data_from_row(columns))
        else:
            print(f"failed with status: {response.status_code}")
            print(response.text)
            break
