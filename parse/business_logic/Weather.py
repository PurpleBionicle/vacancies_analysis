import requests
import Keys
import numpy as np


def choose_day(data):
    days = []
    count = 0

    for i in data['list']:
        if i['dt_txt'][:10] not in days:
            count += 1
            days.append(i['dt_txt'][:10])

    return days


def duration(data, temperature, description, k):
    temp = {'ночь': 0, 'день': 0}
    time = ['ночь', 'день']
    time_description = {'ночь': '', 'день': ''}
    night_count = 0

    for i in range(len(data)):
        if int(data[i]) <= 6:
            night_count += 1
            temp['ночь'] += int(temperature[i])
            if description[i] not in time_description['ночь']:
                time_description['ночь'] += ' ' + description[i]
        else:
            temp['день'] += int(temperature[i])
            if description[i] not in time_description['день']:
                time_description['день'] += ' ' + description[i]

    if temp['ночь'] != 0:
        temp['ночь'] //= night_count
    if temp['день'] != 0:
        temp['день'] //= len(data) - night_count

    return time[k], temp[time[k]], time_description[time[k]]


def weather():
    API_key = Keys.weather
    city_id = 524894  # Moscow
    parameters = {'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': API_key}

    response = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                            params=parameters)

    if response.status_code != 200:
        raise Exception("ERROR invalid request")

    data = response.json()
    days = choose_day(data)
    # print(choose_day(data))
    temperature, description, time = [], [], []
    days_info = []
    for day in days:
        for i in data['list']:

            if i['dt_txt'][:10] == day:
                temperature.append('{0:+3.0f}'.format(i['main']['temp']))
                description.append(i['weather'][0]['description'])
                time.append(i['dt_txt'][11:13])
            if len(time) == 8:
                break
        for i in range(2):
            timer, temp, desc = duration(time, temperature, description, i)
            days_info.append([day, timer, temp, desc])

    return days_info


def day_recomendation():
    # days_info = weather()
    days_info = np.array([['2022-06-09', 'ночь', 15, ' небольшая облачность ясно переменная облачность'],
                          ['2022-06-09', 'день', 22, ' облачно с прояснениями небольшой дождь пасмурно'],
                          ['2022-06-10', 'ночь', 15, ' небольшая облачность ясно переменная облачность'],
                          ['2022-06-10', 'день', 22, ' облачно с прояснениями небольшой дождь пасмурно'],
                          ['2022-06-11', 'ночь', 15, ' небольшая облачность ясно переменная облачность'],
                          ['2022-06-11', 'день', 22, ' облачно с прояснениями небольшой дождь пасмурно'],
                          ['2022-06-12', 'ночь', 15, ' небольшая облачность ясно переменная облачность'],
                          ['2022-06-12', 'день', 22, ' облачно с прояснениями небольшой дождь пасмурно'],
                          ['2022-06-13', 'ночь', 15, ' небольшая облачность ясно переменная облачность'],
                          ['2022-06-13', 'день', 22, ' облачно с прояснениями небольшой дождь пасмурно']])

    rating = [0 for _ in range(len(days_info))]
    good_description_set = {'ясно', 'солнце'}
    bad_description_set = {'облачно', 'пасмурно', 'дождь', 'снегопад'}

    for i in range(len(days_info)):
        if days_info[i][1] == 'день':
            if days_info[i, 2] == max(list(days_info[:, 2])):
                rating[i] += 1

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
    days_info.remove(best_day)
    return best_day, days_info


if __name__ == '__main__':
    print(day_recomendation())
