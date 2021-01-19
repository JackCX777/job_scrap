import codecs
import asyncio
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
    (hh_parser, 'hh'),
    (upwork_parser, 'upwork')
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


async def main(value_tuple):
    func, url, city, programming_language = value_tuple
    jobs, errors = await loop.run_in_executor(None, func, url, city, programming_language)
    jobs_lst.extend(jobs)
    errors_lst.extend(errors)


settings = get_settings()
url_list = get_urls(settings)

# city = City.objects.filter(slug='moscow').first()
# program_language = ProgrammingLanguage.objects.filter(slug='python').first()

jobs_lst, errors_lst = [], []


if __name__ == '__main__':
    # Sync scraping:
    for data in url_list:
        for func, key in parsers:
            url = data['url_data'][key]
            jobs, errors = func(url, city=data['city'], programming_language=data['programming_language'])
            jobs_lst += jobs
            errors_lst += errors

    # Async scraping:
    # loop = asyncio.get_event_loop()
    # tmp_tasks = [
    #     (func, data['url_data'][key], data['city'], data['programming_language'])
    #     for data in url_list
    #     for func, key in parsers
    # ]
    # tasks = asyncio.wait([loop.create_task(main(task_set)) for task_set in tmp_tasks])
    # loop.run_until_complete(tasks)
    # loop.close()

    for job in jobs_lst:
        # так как имена ключей словаря из файла parsers.py совпадают с моделью Vacancy,
        # (url, title...) можно раскрыть словарь:
        vacancy = Vacancy(**job)
        try:
            vacancy.save()
        except DatabaseError:
            pass
        if errors_lst:
            error = Error(data=errors_lst).save()

    # with codecs.open('parse_result.txt', 'w', 'utf-8') as file:
    #     file.write(str(jobs_lst))
