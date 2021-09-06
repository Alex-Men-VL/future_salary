import datetime

import requests
from predict_salary import predict_salary


def get_sj_vacancies(lang, page, api_key):
    sj_url = 'https://api.superjob.ru/2.33/vacancies'
    date_interval = datetime.datetime.now() - datetime.timedelta(days=30)
    town_id = 4
    specialization_id = 48

    headers = {
        'X-Api-App-Id': api_key,
    }
    params = {
        'catalogues': specialization_id,
        'count': 100,
        'date_published_from': date_interval.strftime('%Y-%m-%d'),
        'keywords': f'Программист {lang}',
        'page': page,
        'town': town_id,
    }
    response = requests.get(sj_url, headers=headers, params=params)
    response.raise_for_status()

    return response.json()


def predict_rub_salary_sj(vacancy):
    salary = (vacancy['payment_from'], vacancy['payment_to'])
    if any(salary) and vacancy['currency'] == 'rub':
        salary_from, salary_to = salary[0], salary[1]
        return predict_salary(salary_from, salary_to)
    return None


def get_lang_statistic(lang, api_key):
    page = 0
    other_pages = True
    average_salaries_amount = 0
    vacancies_processed = 0
    while other_pages:
        lang_vacancies = get_sj_vacancies(lang, page, api_key)

        other_pages = lang_vacancies['more']
        vacancies_found = lang_vacancies['total']
        vacancies = lang_vacancies['objects']
        for vacancy in vacancies:
            salary = predict_rub_salary_sj(vacancy)
            if salary:
                average_salaries_amount += salary
                vacancies_processed += 1
        page += 1

    try:
        average_salary = average_salaries_amount // vacancies_processed
    except ZeroDivisionError:
        average_salary = 0

    return vacancies_found, vacancies_processed, average_salary


def get_sj_statistics(languages, api_key):
    statistics = {}
    for lang in languages:
        vacancies_found, vacancies_processed, average_salary = \
            get_lang_statistic(lang, api_key)

        statistics[lang] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }
    return statistics
