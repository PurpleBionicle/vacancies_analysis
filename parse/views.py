# from django.shortcuts import render
#
# # Create your views here.
#
# def vacancy_list(request):
#     return render(request, 'parse/vacancy_list.html', {})
from django.shortcuts import render
from django.utils import timezone
from .models import Vacancies


def vacancy_list(request):
    current_vacancy = Vacancies()
    current_vacancy.salary = 100
    current_vacancy.skills = 'Python'
    return render(request, 'parse/vacancy_list.html', {'current_vacancy': current_vacancy})
