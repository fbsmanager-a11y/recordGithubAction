import requests
from bs4 import BeautifulSoup

url = 'https://ridibooks.com/category/new-releases/2200'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'html.parser')
#class="fig-w1hthz e7z8ge71"
bookservices = soup.select('.fig-w1hthz')
for no, book in enumerate(bookservices, 1):
    print(no, book.text.strip()) 
