import sqlite3
import urllib.request, urllib.parse, urllib.error
import bs4
import ssl

def extract_address(content_tag):
    address_set = set()
    for item in content_tag:
        element = str(item.text.strip())
        if len(element) > 0:
            address_set.add(element)

    return list(address_set)

def street_name(address):
    maxString = None
    for i, item in enumerate(address):

        if maxString is None:
            maxString = item

        elif len(item) > len(maxString):
            maxString = item

    return maxString

URL = "https://www.remax.ca/on/ottawa-real-estate?page=1"
count = 0;

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

html = urllib.request.urlopen(URL, context=ctx).read().decode()

soup = bs4.BeautifulSoup(html, 'html.parser')
tags_div = soup.find_all('div', 'left-content flex-one')

for tag in tags_div:
    count += 1
    h3Tags = tag.findChildren('h3')
    locationTags = tag.findChildren('span', 'ng-star-inserted')

    for h3Tag in h3Tags:
        print('Price :', h3Tag.text.strip())

    location = extract_address(locationTags)
    print('Location :', street_name(location))

    if count % 10 == 0:
        break
