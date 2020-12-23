from django.contrib import admin
from .models import City, Vacancy
from .models import ProgrammingLanguage


admin.site.register(City)
admin.site.register(ProgrammingLanguage)
admin.site.register(Vacancy)
