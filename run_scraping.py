import codecs
import os, sys


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'job_scrap.settings'


import django
django.setup()
from django.db import DatabaseError
from django.contrib.auth import get_user_model


from scrap.parsers import *
from scrap.models import Vacancy, City, ProgrammingLanguage, Error, Url


parsers = (
    (hh_parser, 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&st=resumeSearch&areaId=113&st=employersList&text=python'),
    (upwork_parser, 'https://www.upwork.com/freelance-jobs/python/')
           )

User = get_user_model()

def get_settings():
    query_set = User.objects.filter(send_email=True).values()
    settings_set = set((q['city_id'], q['programming_language_id']) for q in query_set) # default unique set
    return settings_set


def get_urls(_settings):
    query_set = Url.objects.all().values()  # values() returns ids instead instances.
    urls_dict = {(q['city_id'], q['programming_language_id']): q['url_data'] for q in query_set}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['programming_language'] = pair[1]
        tmp['url_data'] = urls_dict[pair]
        urls.append(tmp)
    return urls

q = get_settings()
u = get_urls(q)


city = City.objects.filter(slug='moscow').first()
program_language = ProgrammingLanguage.objects.filter(slug='python').first()

jobs_lst, errors_lst = [], []

if __name__ == '__main__':
    for func, url in parsers:
        jobs, errors = func(url)
        jobs_lst += jobs
        errors_lst += errors

    for job in jobs_lst:
        # так как имена ключей словаря из файла parsers.py совпадают с моделью Vacancy,
        # (url, title...) можно раскрыть словарь:
        vacancy = Vacancy(**job, city=city, programming_language=program_language)
        try:
            vacancy.save()
        except DatabaseError:
            pass
        if errors_lst:
            error = Error(data=errors_lst).save()

    # with codecs.open('parse_result.txt', 'w', 'utf-8') as file:
    #     file.write(str(jobs_lst))
