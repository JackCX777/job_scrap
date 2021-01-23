import os
import sys
import django
import datetime


project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ['DJANGO_SETTINGS_MODULE'] = 'job_scrap.settings'
django.setup()


from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from scrap.models import Vacancy, Error, Url
from job_scrap.settings import EMAIL_HOST_USER


User = get_user_model()
today = datetime.date.today()
empty = '<h4>К сожалению, таких вакансий сегодня не найдено.</h4>'
subject = f'Рассылка вакансий за { today }'
text_content = f'Рассылка вакансий за { today }'
from_email = EMAIL_HOST_USER
ADMIN_USER = EMAIL_HOST_USER

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
            html += f'<h3><a href="{ row["url"] }">{ row["title"] }</a></h3>'
            html += f'<p>{ row["company"] }</p>'
            html += f'<p>{ row["conditions"] }</p>'
            html += f'<p>{row["description"]}</p>'
        _html = html if html else empty
        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

query_set_err = Error.objects.filter(timestamp=today)
subject = ''
text_content = ''
_html = ''
to = ADMIN_USER

if query_set_err.exists():
    # my query set is the list of errors, and when I take first, only one error will be send.
    error = query_set_err.first()
    data = error.data
    for _ in data:
        _html += f'<p><a href="{ _["url"] }">Error: { _["title"] }</a></p><br>'
    subject = f'Ошибки сбора вакасий за { today }'
    text_content = f'Ошибки сбора вакасий за { today }'

query_set_url = Url.objects.all().values('city', 'programming_language')
urls_dict = {(_['city'], _['programming_language']): True for _ in query_set_url}
urls_pair_keys_error = ''
for keys in users_dict.keys():
    if keys not in urls_dict:
        urls_pair_keys_error += f'<p>Для города { keys[0] } и специальности { keys[1] } нет url.</p><br>'
if urls_pair_keys_error:
    subject += ' Отсутствуют url'
    _html += urls_pair_keys_error

if subject:
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


# If mails doesnt sands from django use smtplib

# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
#
# msg = MIMEMultipart('alternative')
# msg['Subject'] = 'Список вакансий за  {}'.format(today)
# msg['From'] = EMAIL_HOST_USER
# mail = smtplib.SMTP()
# mail.connect(EMAIL_HOST, 25)
# mail.ehlo()
# mail.starttls()
# mail.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#
# html_m = "<h1>Hello world</h1>"
# part = MIMEText(html_m, 'html')
# msg.attach(part)
# mail.sendmail(EMAIL_HOST_USER, [to], msg.as_string())
# mail.quit()
