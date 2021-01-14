import requests
from bs4 import BeautifulSoup as BS


def xsrf(text):
    bs = BS(text, 'html5lib')
    xsrf = bs.find('input', {'name': "_xsrf", 'type': "hidden"})
    return xsrf


my_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Cookie': '__ddg1=UMeggUGizTKjVPRgOK8v; _xsrf=e4cb9df0c9e0bf4fd4e6edec2b6e2b44; _xsrf=e4cb9df0c9e0bf4fd4e6edec2b6e2b44; hhrole=anonymous; regions=1; region_clarified=NOT_SET; display=desktop; hhtoken=K6VAYMKXmQK6V9WPM4Ulw1DNrKL9; hhuid=b_AE3TTTVegAqV!ohx4xRQ--; GMT=3; _ga_44H5WGZ123=GS1.1.1609074493.1.1.1609075266.0; _ga=GA1.1.1442314115.1609074495; iap.uid=063b7988e6014d8d8beebe6ed1cb0f22; total_searches=2',
    'DNT': '1',
    'Host': 'hh.ru',
    'TE': 'Trailers',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:84.0) Gecko/20100101 Firefox/84.0'
             }
linux_headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0'}

more_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8'
           }

myip_headers = {
    'Accept-Encoding': 'gzip',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.3 Safari/605.1.15',
    'accept-language': 'ru'
}

gheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

# url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&st=resumeSearch&areaId=113&st=employersList&text=python'
url = 'https://hh.ru'
# url = 'https://google.com'

response = requests.get(url, headers=my_headers)
status_code = response.status_code
print(status_code)




