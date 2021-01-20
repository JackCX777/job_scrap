from django.core.paginator import Paginator
from django.shortcuts import render
from .Forms import FindForm
from .models import Vacancy


def home_view(request):
    form = FindForm()
    return render(request, 'scrap/home.html', {'form': form})


def vacancy_view(request):
    form = FindForm()
    city = request.GET.get('city')
    programming_language = request.GET.get('programming_language')
    context = {'city': city, 'programming_language': programming_language, 'form': form}
    if city or programming_language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if programming_language:
            _filter['programming_language__slug'] = programming_language
        query_set = Vacancy.objects.filter(**_filter)  # Request to database returns query_set object.
        paginator = Paginator(query_set, 10)  # Show 25 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
    return render(request, 'scrap/vacancy.html', context)
