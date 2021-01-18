from django.contrib import admin
from .models import City, Vacancy, ProgrammingLanguage, Error


admin.site.register(City)
admin.site.register(ProgrammingLanguage)
admin.site.register(Vacancy)
admin.site.register(Error)
