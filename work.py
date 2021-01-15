import requests
import codecs
from bs4 import BeautifulSoup as BS


gheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

hh_url = 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&st=resumeSearch&areaId=113&st=employersList&text=python'
upwork_url = 'https://www.upwork.com/freelance-jobs/python/'
# url = 'https://hh.ru'
# url = 'https://google.com'

response = requests.get(hh_url, headers=gheaders)
hh_jobs_lst = []
errors_lst = []
if response.status_code == 200:
    soup = BS(response.content, 'html.parser')
    main_div = soup.find('div', attrs={'class': 'vacancy-serp'})
    if main_div:
        pass
        div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
        for div in div_lst:
            # vac_title = div.find('span', attrs={'class': 'g-user-content'})
            vac = div.find('a')
            vac_title = vac.text
            vac_href = vac['href']
            vac_content = div.find('div', attrs={'class': 'g-user-content'}).text
            vac_company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
            hh_jobs_lst.append({'title': vac_title, 'url': vac_href, 'description': vac_content, 'company': vac_company})
    else:
        errors_lst.append({'url': hh_url, 'title': 'The div does not exists'})
else:
    errors_lst.append({'url': hh_url, 'title': 'The page does not respond'})

with codecs.open('hh_parse.txt', 'w', 'utf-8') as file:
    file.write(str(hh_jobs_lst))

# Saving the whole webpage:
# with codecs.open('resp_cont.html', 'w', 'utf-8') as file:
#     file.write(str(response.text))




