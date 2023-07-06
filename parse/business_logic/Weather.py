import requests
from parse.business_logic import Keys
import numpy as np


class Day():
    """
    temp - температура в этот день
    desc - описание погоды в этот день
    """
    def __init__(self, day, timer, temp, desc):
        self.day = day
        self.timer = timer
        self.temp = temp
        self.desc = desc


def choose_day(data):
    """Собираем числа из json структур"""
    days = []
    count = 0
    for i in data['list']:
        if i['dt_txt'][:10] not in days:
            count += 1
            days.append(i['dt_txt'][:10])
    return days


def duration(data, temperature, description, k):
    "Вычленение среднедневной температуры без учета ночи"
    temp = {'день': 0}
    time = ['день']
    time_description = {'день': ''}
    night_count = 0

    for i in range(len(data)):
        if int(data[i]) < 6:
            night_count += 1

        else:
            temp['день'] += int(temperature[i])
            if description[i] not in time_description['день']:
                time_description['день'] += ' ' + description[i]

    # if temp['ночь'] != 0:
    #     temp['ночь'] //= night_count

    if temp['день'] != 0:
        temp['день'] //= len(data) - night_count

    return time[0], temp[time[0]], time_description[time[0]]


def weather():
    """
    :return: Получение погоды на N дня через API
    """
    API_key = Keys.weather
    city_id = 524894  # Moscow
    "Получение json структуры"
    parameters = {'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': API_key}

    response = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params=parameters)
    if response.status_code != 200:
        raise Exception("ERROR invalid request")

    data = response.json()
    "Соберем числа из json"
    days = choose_day(data)
    # print(choose_day(data))
    temperature, description, time = [], [], []
    days_info = []
    "Соберем остальную информацию из json"
    for day in days:
        for i in data['list']:
            if i['dt_txt'][:10] == day:
                temperature.append('{0:+3.0f}'.format(i['main']['temp']))
                description.append(i['weather'][0]['description'])
                time.append(i['dt_txt'][11:13])
            if len(time) == 8:
                break

        for i in range(2):

            if i != 0:
                timer, temp, desc = duration(time, temperature, description, i)
                days_info.append([day, timer, str(temp), desc])

    return days_info


def day_recomendation():
    "Основная ф-ция - По полученным дням выбирает лучший"
    days_info = np.array(weather())

    rating = [0 for _ in range(len(days_info))]
    "Определим хорошие характеристики дня и плохие"
    good_description_set = {'ясно', 'солнце'}
    bad_description_set = {'облачно', 'пасмурно', 'дождь', 'снегопад'}

    for i in range(len(days_info)):
        "Если случайно ночь осталась убираем ее"
        if days_info[i][1] == 'день':
            "1 балл получаем самый теплый день, который не теплее 25 градусов"
            if days_info[i, 2] == max(list(days_info[:, 2])) and int(days_info[i, 2]) <= 25:
                rating[i] += 1

            "1 балл за каждую хорошую характеристику дня и минус 1 за каждую плохую"
            for x in good_description_set:
                if x in days_info[i][3]:
                    rating[i] += 1

            for x in bad_description_set:
                if x in days_info[i][3]:
                    rating[i] -= 1

        else:
            rating[i] -= 10

    max_index = 0
    for i in range(len(rating)):
        if rating[i] == max(rating):
            max_index = i
            break

    best_day = days_info[max_index]
    days_info, best_day = days_info.tolist(), best_day.tolist()

    # convert to class
    days_info_in_class = []
    days_info.remove(best_day)
    best_day_class = Day(best_day[0], best_day[1], best_day[2], best_day[3])
    for day in days_info:
        day_class = Day(day[0], day[1], day[2], day[3])
        days_info_in_class.append(day_class)

    return best_day_class, days_info_in_class


if __name__ == '__main__':
    best_day, other_days = day_recomendation()
    for day in other_days:
        print(day.temp)
