import urllib.request
from bs4 import BeautifulSoup

def get_link(url, loc):
    if loc <= 0:
        return

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup('a')
    return tags[loc - 1].get('href', None)


def main():
    count = int(input("Enter count: "))
    position = int(input("Enter the position: "))
    url = "http://py4e-data.dr-chuck.net/known_by_Reigan.html"
    while count > 0:
        url = get_link(url, position)
        print('Retrieving: ' + url)
        count = count - 1

    print(url)


if __name__ == "__main__":
    main()
