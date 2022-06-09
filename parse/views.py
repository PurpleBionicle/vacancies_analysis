from django.shortcuts import render
from django.utils import timezone
from .models import Vacancies
from .business_logic.Weather import day_recomendation


def vacancy_list(request):
    best_day , other_days = day_recomendation()

    # current_vacancy = Vacancies()
    # current_vacancy.salary = 100
    # current_vacancy.skills = 'Python'
    # message = request.POST['name_field']
    # print(message)
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'

    return render(request, 'parse/vacancy_list.html', {'best_day': best_day, 'other_days': other_days })
