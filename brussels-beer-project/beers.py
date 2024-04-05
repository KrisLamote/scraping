import csv
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://beerproject.be"
INDEX_PATH = "/collections/all"

# add your proxy here, if needed
proxies = {}

page = requests.get(BASE_URL + INDEX_PATH, proxies=proxies, timeout=10)
beer_els = BeautifulSoup(page.content, "html.parser").find_all(class_='boost-pfs-filter-product-item')

with open("beers.csv", mode="w", encoding="utf8", newline="") as file:
    cnt = 0
    col_headers = [
        "Name",
        "Price",
        "Description",
        "Color",
        "Bitterness",
        "Image",
    ]
    writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL)
    writer.writerow(col_headers)

    for beer_el in beer_els:
        name = beer_el.find('a', class_='boost-pfs-filter-product-item-title').text
        print(f'🍺 {name}')
        
        price = beer_el.find('span', class_='boost-pfs-filter-product-item-regular-price').text.strip()
        
        link_element = beer_el.find('a', class_='boost-pfs-filter-product-item-image-link')
        link = link_element.attrs['href']

        image = link_element.find('img').attrs['data-src']
        image = image.split('?')[0].replace('//', 'https://') if image is not None else None

        detail = requests.get(BASE_URL + link, proxies=proxies, timeout=10)
        
        description_el = BeautifulSoup(detail.content, "html.parser").find('div', class_='sp-tab-content')
        description = description_el.get_text(strip=True) if description_el else None
        
        ebc = BeautifulSoup(detail.content, "html.parser").select_one('div.custom-field__colour > p > span')
        
        ibu = BeautifulSoup(detail.content, "html.parser").select_one('div.custom-field__bitterness > p > span')

        writer.writerow([
            name,
            price,
            description,
            ebc.text.strip().split(': ')[-1] if ebc else None,
            ibu.text.strip().split(': ')[-1] if ibu else None,
            image,
        ])
        cnt += 1
    
print(f'Collected {cnt} 🍺.')
    
