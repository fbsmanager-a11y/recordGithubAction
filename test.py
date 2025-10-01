import requests
from bs4 import BeautifulSoup
# url = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bjky&pkid=1&os=28410101&qvt=0&query=%EA%B0%95%ED%98%95%EC%B2%A0' 
url = 'https://ridibooks.com/category/new-releases/2200'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

soup = BeautifulSoup(html, 'html.parser')
#class="fig-w1hthz e7z8ge71"
bookservices = soup.select('.fig-w1hthz')
for no, book in enumerate(bookservices, 1):
    print(no, book.text.strip()) 
