import requests
import json
import os
import time
import shutil


def get_page(page=0, name_vacancy=0):
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
    for i in range(pages):
        json_vacancy = json.loads(get_page(i, name_vacancy))

        next_file_name = 'parse/business_logic/json_files/1.json'\
            .format(len(os.listdir('parse/business_logic/json_files/')))

        file = open(next_file_name, mode='w', encoding='utf8')
        file.write(json.dumps(json_vacancy, ensure_ascii=False))
        file.close()

        # Проверка на последнюю страницу, если вакансий меньше
        if (json_vacancy['pages'] - i) <= 1:
            break

        # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
        time.sleep(0.25)


def vacancy():
    for file in os.listdir('parse/business_logic/json_files/'):
        f = open('parse/business_logic/json_files/1.json'.format(file), encoding='utf8')
        json_file = f.read()
        f.close()

        json_vacancy = json.loads(json_file)
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'json_vacancy')
        shutil.rmtree(path)
        os.mkdir(path)
        for vacancy in json_vacancy['items']:
            request_ = requests.get(vacancy['url'])
            data = request_.content.decode()
            request_.close()

            filename = 'parse/business_logic/json_vacancy/{}.json'.format(vacancy['id'])
            f = open(filename, mode='w', encoding='utf8')
            f.write(data)
            f.close()

        time.sleep(0.25)
        print('Вакансии собраны')


if __name__ == '__main__':
    collect_pages(1, 'python')
    vacancy()
