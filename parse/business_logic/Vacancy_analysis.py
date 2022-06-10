import json
import os

def json_treatment():

    skills_name = []  # Список названий навыков
    vacancies = []
    # В выводе будем отображать прогресс
    # Для этого узнаем общее количество файлов, которые надо обработать
    # Счетчик обработанных файлов установим в ноль
    cnt_docs = len(os.listdir('parse/business_logic/json_vacancy/'))
    i = 0

    # Проходимся по всем файлам в папке vacancies
    for fl in os.listdir('parse/business_logic/json_vacancy/'):

        # Открываем, читаем и закрываем файл
        f = open('parse/business_logic/json_vacancy/{}'.format(fl), encoding='utf8')
        jsonText = f.read()
        f.close()

        # Текст файла переводим в справочник
        jsonObj = json.loads(jsonText)

        # Заполняем списки для таблиц
        current = []
        salary = []
        current.append(jsonObj['name'])
        current.append(jsonObj['description'])

        if isinstance(jsonObj['salary'] , dict):
            salary.append(str(jsonObj['salary'].get('from',0 )))
            salary.append(str(jsonObj['salary'].get('to',0 )))

        else:
            salary.append('0')
            salary.append('0')

        current.append('-'.join(salary))
        # Т.к. навыки хранятся в виде массива, то проходимся по нему циклом
        for skl in jsonObj['key_skills']:
            skills_name.append(skl['name'])

        current.append(' '.join(skills_name))
        # Увеличиваем счетчик обработанных файлов на 1, очищаем вывод ячейки и выводим прогресс
        i += 1
        vacancies.append(current)

    return vacancies



if __name__ == '__main__':
    json_treatment()
