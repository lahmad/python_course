import urllib.request
from bs4 import BeautifulSoup

SAMPLE_URL = "http://py4e-data.dr-chuck.net/comments_42.html"
ACTUAL_URL = "http://py4e-data.dr-chuck.net/comments_175113.html"

def get_sum(url):
    if not url:
        print('URL cannot be empty or null')
        return

    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')

    tags = soup('span')
    sum = 0
    for tag in tags:
        sum += int(tag.contents[0])

    print(sum)


if __name__ == '__main__':
    get_sum(ACTUAL_URL)
