import logging
import os

from dotenv import load_dotenv
from fetch_hh import get_hh_statistics
from fetch_sj import get_sj_statistics
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from terminaltables import AsciiTable


def make_table(site, statistics):
    TABLE_DATA = (
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
        TABLE_DATA = (*TABLE_DATA, lang_info)
    title = f'{site} Moscow'
    table_instance = AsciiTable(TABLE_DATA, title)
    print(table_instance.table)


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
        statistics_from_hh = get_hh_statistics(languages)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from hh.ru.")

    try:
        statistics_from_sj = get_sj_statistics(languages, api_key)
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from superjob.ru.")

    site_to_statistics = {
        'HeadHunter': statistics_from_hh,
        'SuperJob': statistics_from_sj,
    }

    for site, statistics in site_to_statistics.items():
        make_table(site, statistics)


if __name__ == '__main__':
    main()
