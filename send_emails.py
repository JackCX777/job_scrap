import os
import sys
import django
import datetime
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from scrap.models import Vacancy
from job_scrap.settings import EMAIL_HOST_USER


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'job_scrap.settings'
django.setup()


User = get_user_model()
today = datetime.date.today()
empty = '<h4>К сожалению, таких вакансий сегодня не найдено.</h4>'
subject = f'Рассылка вакансий за { today }'
text_content = f'Рассылка вакансий за { today }'
from_email = EMAIL_HOST_USER
query_set_usr = User.objects.filter(send_email=True).values('city', 'programming_language', 'email')
users_dict = {}
for _ in query_set_usr:
    # set default tuple for key and list for value
    users_dict.setdefault((_['city'], _['programming_language']), [])
    users_dict[(_['city'], _['programming_language'])].append(_['email'])
if users_dict:
    # __in = all values with this pair
    params = {'city_id__in': [], 'programming_language_id__in': []}
    for pair in users_dict.keys():
        params['city_id__in'].append(pair[0])
        params['programming_language_id__in'].append(pair[1])
        # **params = unpack params dict, [:10] = temporary limit
    query_set_vac = Vacancy.objects.filter(**params, timestamp=today).values()
    # if .values() without any key, then keys + _id
    vacancies_dict = {}
    for _ in query_set_vac:
        vacancies_dict.setdefault((_['city_id'], _['programming_language_id']), [])
        vacancies_dict[(_['city_id'], _['programming_language_id'])].append(_)
    for keys, emails in users_dict.items():
        rows = vacancies_dict.get(keys, [])
        html = ''
        for row in rows:
            html += f'<h><a href="{ row["url"] }">{ row["title"] }</a></h5>'
            html += f'<h4>{ row["company"] }</h4>'
            html += f'<p>{ row["conditions"] }</p>'
            html += f'<p>{row["description"]}</p>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()


# It's from manuals:

# subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
# text_content = 'This is an important message.'
# html_content = '<p>This is an <strong>important</strong> message.</p>'
# msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
# msg.attach_alternative(html_content, "text/html")
# msg.send()
