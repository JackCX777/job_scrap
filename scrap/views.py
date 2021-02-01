from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

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


# class VacancyList(ListView):
#     model = Vacancy
#     template_name = 'scrap/vacancy.html'
#     form = FindForm()
#     # чтобы работала пагинация, нужно в vacancy.html заменить все object_list на page_obj
#     paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)
#         context['city'] = self.request.GET.get('city')
#         context['programming_language'] = self.request.GET.get('programming_language')
#         context['form'] = self.form
#         return context
#
#     def get_queryset(self):
#         city = self.request.GET.get('city')
#         programming_language = self.request.GET.get('programming_language')
#         query_set = []
#         if city or programming_language:
#             _filter = {}
#             if city:
#                 _filter['city__slug'] = city
#             if programming_language:
#                 _filter['programming_language__slug'] = programming_language
#             query_set = Vacancy.objects.filter(**_filter)  # Request to database returns query_set object.
#         return query_set



# def vacancy_details(request, pk):
#     # object_ = Vacancy.objects.get(pk=pk)
#     # чтобы обработать ошибку, если такого pk не существует
#     object_ = get_object_or_404(Vacancy, pk=pk)
#     return render(request, 'scrap/detail.html', {'object': object_})


# vacancy_details с помощью класса
class VacancyDetail(DetailView):
    queryset = Vacancy.objects.all()
    template_name = 'scrap/detail.html'
    # context_object_name = 'object'
    # если нужна еще логика, переопределяем метод get()
    def get(self, request, *args, **kwargs):
        pass
