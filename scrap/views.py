from django.shortcuts import render
from .models import Vacancy


def vacancy_view(request):
    city = request.GET.get('city')
    programming_language = request.GET.get('programming_language')
    query_set = []
    if city or programming_language:
        _filter = {}
        if city:
            _filter['city__name'] = city
        if programming_language:
            _filter['programming_language__name'] = programming_language
        query_set = Vacancy.objects.filter(**_filter)  # Request to database returns query_set object.
    return render(request, 'scrap/vacancy.html', {'object_list': query_set})
