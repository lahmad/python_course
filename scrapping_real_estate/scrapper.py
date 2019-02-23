import sqlite3
import urllib.request, urllib.parse, urllib.error
import bs4
import ssl
import time
from database import Database

URL = "https://www.remax.ca/on/ottawa-real-estate?page={}"
INSERT_PROPERTY = 'INSERT OR IGNORE INTO PROPERTY(address, price) VALUES(?,?);'
INSERT_PROPERTY_INFO = '''INSERT OR IGNORE INTO PROPERTY_INFO(property_id,
    bed, bath, sqft, type) VALUE(?,?,?,?,?);'''

SELECT_PROPERTY_INFO = 'SELECT id from PROPERTY WHERE address = ?'

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

def visit_pages(page, ctx, tag, clss):
    html = urllib.request.urlopen(page, context=ctx).read().decode()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tags_div = soup.find_all(tag, clss)

    return tags_div


def remove_pipe_tags(tags):
    result = []
    for tag in tags:
        print(tag)
        if tag.text == '|':
            continue
        result.append(tag)

def main():
    count = 0;
    pageIndex = 1
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    list_of_properties = []

    # Scrapping 10 pages
    for num in range(1, 2):

        url = URL.format(pageIndex)
        print(url)
        pageIndex  = pageIndex + 1
        # It will scrap 10 pages
        tags_address = visit_pages(url, ctx,'div', 'left-content flex-one')

        for tag in tags_address:
            property = dict()
            count += 1
            h3Tags = tag.findChildren('h3')
            locationTags = tag.findChildren('span', 'ng-star-inserted')
            price = None

            for h3Tag in h3Tags:
                price = h3Tag.text.strip()
                #print('Price :', price)

            location = extract_address(locationTags)
            location = street_name(location)
            #print('Location :', location)

            property['price'] = int(price[1:].replace(',',''))
            property['address'] = location

            list_of_properties.append(property)

        spans_property_info = visit_pages(url, ctx,'div', 'property-details')

        #spans_property_info = visit_pages(url, ctx,'span', 'detail ng-star-inserted')
        for tag in spans_property_info:
            children = tag.find_all('span', 'detail ng-star-inserted')
            if children is not None and len(children) > 0:
                print("----")
                remove_pipe_tags(children)
            # for child in children:
            #
            #     if len(child) >= 1 and child.find('span'):
            #         if (len(child) == 1) and child.find() == '|':
            #             continue
            #
            #         info =  child.find('span', 'classifier')
            #         info_text = info.text.strip()
            #         if info_text == 'bed':
            #             print(' Bed is ' + child.find('span', 'bold').text)
            #
            #         if info_text == 'bath':
            #             print(' Bath is ' + child.find('span', 'bold').text)
            #
            #         elif info_text == 'sqft':
            #                 print(' sqft is ' + child.find('span', 'bold').text)



        #     children = list(tag.contents)
        #     if len(children) > 1:
        #         print(children[0].text + " " + children[1].text)
        #
        #         text = children[1].text
        #         if text == 'bath':
        #             property['bath'] = children[0].text
        #         if text == 'bed':
        #             property['bed'] = children[0].text
        #         if text == 'sqft':
        #             property['sqft'] = children[0].text
        # print('=====================')



    # for element in list_of_properties:
    #     print(element)

        # if count % 2 == 0:
        #     print('Sleeping for 2 seconds...')
        #     time.sleep(2)
        # count = count + 1
    #
    # database = Database()
    #
    # for element in list_of_properties:
    #     # Put the property in property table
    #     database.insert(INSERT_PROPERTY, (element.get('address'), element.get(price)))
    #     row = database.query(SELECT_PROPERTY_INFO, (element.get('address'),))
    #
    #     if row is not None:
    #         database.insert(INSERT_PROPERTY_INFO, (row[-], bed, bath, sqft, type))


if __name__ == '__main__':
    main()
