import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint


__all__ = ('hh_parser', 'upwork_parser')


headers_list = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
     },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
     },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8'
     },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
]


def hh_parser(site_url, city=None, programming_language=None):
    hh_jobs_lst = []
    hh_errors_lst = []
    if site_url:
        response = requests.get(site_url, headers=headers_list[randint(0, 4)])
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'vacancy-serp'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'vacancy-serp-item'})
                for div in div_lst:
                    # vac_title = div.find('span', attrs={'class': 'g-user-content'})
                    vac = div.find('a')
                    vac_title = vac.text
                    vac_href = vac['href']
                    vac_content = div.find('div', attrs={'class': 'g-user-content'}).text
                    vac_conditions = div.find('div', attrs={'class': 'vacancy-serp-item__sidebar'}).text
                    vac_company = div.find('div', attrs={'class': 'vacancy-serp-item__meta-info-company'}).text
                    hh_jobs_lst.append(
                        {
                            'title': vac_title,
                            'url': vac_href,
                            'description': vac_content,
                            'conditions': vac_conditions,
                            'company': vac_company,
                             'city_id': city,
                             'programming_language_id': programming_language
                         }
                                       )
            else:
                hh_errors_lst.append({'url': site_url, 'title': 'The div does not exists'})
        else:
            hh_errors_lst.append({'url': site_url, 'title': 'The page does not respond'})
        # Saving the whole webpage:
        # with codecs.open('resp_cont.html', 'w', 'utf-8') as file:
        #     file.write(str(response.text))
    return hh_jobs_lst, hh_errors_lst


def upwork_parser(site_url, city=None, programming_language=None):
    upwork_jobs_lst = []
    upwork_errors_lst = []
    domain = 'https://www.upwork.com'
    if site_url:
        response = requests.get(site_url, headers=headers_list[randint(0, 4)])
        if response.status_code == 200:
            soup = BS(response.content, 'html.parser')
            main_div = soup.find('div', attrs={'class': 'job-tiles-wrapper'})
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'job-tile-content'})
                for div in div_lst:
                    vac = div.find('a')
                    vac_title = vac.text
                    vac_href = vac['href']
                    vac_content = div.find('p', attrs={'data-qa': 'job-description'}).text
                    vac_conditions = div.find('div', attrs={'class': 'row'}).text
                    vac_company = 'No company (freelance)'
                    upwork_jobs_lst.append(
                        {
                            'title': vac_title,
                            'url': domain + vac_href,
                            'description': vac_content,
                            'conditions': vac_conditions,
                            'company': vac_company,
                            'city_id': city,
                            'programming_language_id': programming_language
                         }
                                           )
            else:
                upwork_errors_lst.append({'url': site_url, 'title': 'The div does not exists'})
        else:
            upwork_errors_lst.append({'url': site_url, 'title': 'The page does not respond'})
        # Saving the whole webpage:
        # with codecs.open('resp_cont.html', 'w', 'utf-8') as file:
        #     file.write(str(response.text))
    return upwork_jobs_lst, upwork_errors_lst
