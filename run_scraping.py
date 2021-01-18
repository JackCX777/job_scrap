import codecs
import os, sys


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'job_scrap.settings'


import django
django.setup()
from django.db import DatabaseError


from scrap.parsers import *
from scrap.models import Vacancy, City, ProgrammingLanguage, Error


parsers = (
    (hh_parser, 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&st=resumeSearch&areaId=113&st=employersList&text=python'),
    (upwork_parser, 'https://www.upwork.com/freelance-jobs/python/')
           )

city = City.objects.filter(slug='amsterdam').first()
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
