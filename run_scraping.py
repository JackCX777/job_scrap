import codecs
import os, sys


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'job_scrap.settings'


import django
django.setup()


from scrap.parsers import *
from scrap.models import Vacancy, City, ProgrammingLanguage


parsers = (
    (hh_parser, 'https://hh.ru/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=true&st=resumeSearch&areaId=113&st=employersList&text=python'),
    (upwork_parser, 'https://www.upwork.com/freelance-jobs/python/')
           )

jobs_lst, errors_lst = [], []


if __name__ == '__main__':
    for func, url in parsers:
        jobs, errors = func(url)
        jobs_lst += jobs
        errors_lst += errors
    with codecs.open('parse_result.txt', 'w', 'utf-8') as file:
        file.write(str(jobs_lst))
