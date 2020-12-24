from django.shortcuts import render
from .models import Vacancy


def vacancy_view(request):
    print(request.POST)
    query_set = Vacancy.objects.all()  # Request to database returns query_set object.
    return render(request, 'scrap/vacancy.html', {'object_list': query_set})
