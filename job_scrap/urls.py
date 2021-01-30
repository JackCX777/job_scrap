"""job_scrap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from scrap.views import vacancy_view, home_view, vacancy_details, VacancyDetail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('vacancy/', vacancy_view, name='vacancy'),
    path('accounts/', include(('accounts.urls', 'accounts'))),
    # <int:pk> - после адреса должно быть число, которое парсит Django и присваивает значение переменной pk,
    # имя которой должно совпадать с именем во views.py, чтобы потом это значение могло пеередаваться во views.py.
    # path('detail/<int:pk>/', vacancy_details, name='vacancy_details'),
    # vacancy_details с помощью класса
    path('detail/<int:pk>/', VacancyDetail.as_view(), name='vacancy_details'),
]
