import datetime

import requests
from predict_salary import predict_salary


def get_hh_vacancies(lang, page):
    hh_url = 'https://api.hh.ru/vacancies'
    date_interval = datetime.datetime.now() - datetime.timedelta(days=30)
    params = {
        'area': 1,
        'date_from': date_interval.strftime('%Y-%m-%d'),
        'page': page,
        'per_page': 100,
        'specialization': 1.221,
        'text': f'Программист {lang}',
    }
    response = requests.get(hh_url, params=params)
    response.raise_for_status()

    return response.json()


def predict_rub_salary_hh(vacancy):
    salary = vacancy['salary']
    if salary and salary['currency'] == 'RUR':
        return predict_salary(salary['from'], salary['to'])
    return None


def get_hh_statistics(languages):
    statistics = {}
    for lang in languages:
        page = 0
        pages_number = 1
        average_salary = 0
        vacancies_processed = 0
        while page < pages_number:
            lang_vacancies = get_hh_vacancies(lang, page)

            pages_number = lang_vacancies['pages']
            vacancies_quantity = lang_vacancies['found']
            vacancies = lang_vacancies['items']
            for vacancy in vacancies:
                salary = predict_rub_salary_hh(vacancy)
                if salary:
                    average_salary += salary
                    vacancies_processed += 1
            page += 1

        statistics[lang] = {
            "vacancies_found": vacancies_quantity,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary // vacancies_processed,
        }
    return statistics
