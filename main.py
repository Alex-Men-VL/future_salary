import logging
import os

from dotenv import load_dotenv
from fetch_hh import get_hh_statistics
from fetch_sj import get_sj_statistics
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from terminaltables import AsciiTable


def make_table(site, statistics):
    table_data = [
        (
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ),
    ]
    for lang, info in statistics.items():
        lang_info = (
            lang,
            info['vacancies_found'],
            info['vacancies_processed'],
            info['average_salary'],
        )
        table_data.append(lang_info)
    title = f'{site} Moscow'
    table_instance = AsciiTable(table_data, title)
    return table_instance.table


def main():
    load_dotenv()
    api_key = os.getenv('SJ_TOKEN')

    languages = [
        'JavaScript',
        'Java',
        'Python',
        'Ruby',
        'PHP',
        'C++',
        'C#',
        'C',
        'GO',
        'Rust',
    ]

    try:
        hh_statistics = get_hh_statistics(languages)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from hh.ru.")

    try:
        sj_statistics = get_sj_statistics(languages, api_key)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from superjob.ru.")

    site_to_statistics = {
        'HeadHunter': hh_statistics,
        'SuperJob': sj_statistics,
    }

    for site, statistics in site_to_statistics.items():
        langs_statistics_table = make_table(site, statistics)
        print(langs_statistics_table)


if __name__ == '__main__':
    main()
