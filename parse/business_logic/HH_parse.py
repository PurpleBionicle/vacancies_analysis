import requests
import json
import os
import time
import shutil


def get_page(page=0, name_vacancy=0):
    '''
    :param page: с какой по счету страницы собираем информацию (по 20 постов на одной странице)
    Отмечу, что на общих страницах только часть информации о вакансии, а для полной надо проваливаться в ссылку
    :param name_vacancy: по какому имени собираем вакансии
    :return: результат get запроса с использованием Api hh.ru в формате json
    '''
    params = {
        'text': f'NAME:{name_vacancy}',  # name of vacancies
        'area': 1,  # Moscow
        'page': page,  # index page
        'per_page': 20  # vacancies per page
    }

    request_ = requests.get('https://api.hh.ru/vacancies', params)
    data = request_.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
    request_.close()
    return data


def collect_pages(pages, name_vacancy):
    """
    :param pages: число страниц, с которых будут анализироваться вакансии
    :param name_vacancy: имя запрашиваемой вакансии
    :return: ничего, ф-ция создает файлы с полученной информацией
    """
    for i in range(pages):
        "по одной страницы получаем информацию"
        json_vacancy = json.loads(get_page(i, name_vacancy))

        "для каждой странички записываем свой файл"
        count_of_files = str(len(os.listdir("parse/business_logic/json_files/")))
        next_file_name = f'parse/business_logic/json_files/{count_of_files}.json'
        file = open(next_file_name, mode='w', encoding='utf8')
        file.write(json.dumps(json_vacancy, ensure_ascii=False))
        file.close()

        "Проверка на последнюю страницу, если вакансий меньше"
        if (json_vacancy['pages'] - i) <= 1:
            break

        " Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать"
        time.sleep(0.25)


def vacancy():
    """
    Функция пересобирает информацию из файла вакансий по страницам на отдельные вакансии
    """
    for file in os.listdir('parse/business_logic/json_files/'):
        "Поочередно читаем все файлы"
        f = open('parse/business_logic/json_files/1.json'.format(file), encoding='utf8')
        json_file = f.read()
        f.close()

        "весь файл сохранили в переменную и удаляем файл"
        json_vacancy = json.loads(json_file)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'json_vacancy')
        shutil.rmtree(path)
        os.mkdir(path)
        "перебираем вакансии из удаленного файла"
        for vacancy in json_vacancy['items']:
            "для каждой вакансии получаем ссылку и проваливаемся по ней для полной информации о ней"
            request_ = requests.get(vacancy['url'])
            data = request_.content.decode()
            request_.close()
            "Собранную информацию сохраняем"
            filename = 'parse/business_logic/json_vacancy/{}.json'.format(vacancy['id'])
            f = open(filename, mode='w', encoding='utf8')
            f.write(data)
            f.close()

        time.sleep(0.25)
        print('Вакансии собраны')


if __name__ == '__main__':
    collect_pages(1, 'python')
    vacancy()
