from django.shortcuts import render
from django.utils import timezone
from .models import Vacancies
from .business_logic.Weather import day_recomendation
from .business_logic.Course import course_transfer


def vacancy_list(request):

    best_day, other_days = day_recomendation()
    # currency, usd, euro = course_transfer(1)

    def sim():
        pass

    # current_vacancy = Vacancies()
    # current_vacancy.salary = 100
    # current_vacancy.skills = 'Python'
    # message = request.POST['name_field']
    # print(message)

    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'

    return render(request, 'parse/vacancy_list.html', {'best_day': best_day, 'other_days': other_days,
                                                       'euro': 1, 'usd': 1})
