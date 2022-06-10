from django.shortcuts import render, redirect
from .models import Vacancies
from .business_logic.Weather import day_recomendation
from .business_logic.Course import course_transfer
from .business_logic.HH_parse import vacancy ,collect_pages
from .business_logic.Vacancy_analysis import *


def vacancy_list(request):
    best_day, other_days = day_recomendation()
    # currency, usd, euro = course_transfer(1)

    return render(request, 'parse/vacancy_list.html', {'best_day': best_day, 'other_days': other_days,
                                                       'euro': 1, 'usd': 1})


def search(request):
    name = 0

    if 'vacancy_name' in request.GET:
        name = request.GET.get('vacancy_name')

    print(name)
    collect_pages(1, name)  # найти вакансии
    vacancy()  # пересоберем в отдельные файлы
    vacancies = json_treatment()  # анализ

    list_of_models_vacancies = []

    for current_vacancy in vacancies:
        template = Vacancies()

        template.name = current_vacancy[0]
        template.description = current_vacancy[1]
        template.salary = current_vacancy[2]
        template.skills_name = current_vacancy[3]

        list_of_models_vacancies.append(template)

    return render(request, 'parse/search.html', {'vacancies': list_of_models_vacancies})
