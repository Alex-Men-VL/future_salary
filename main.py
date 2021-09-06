import logging
import os

from dotenv import load_dotenv
from fetch_hh import get_hh_statistics
from fetch_sj import get_sj_statistics
from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from terminaltables import AsciiTable


def make_table(site, lang_statistics):
    site_statistics_table = [
        (
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ),
    ]
    for lang, statistics in lang_statistics.items():
        table_raw = (
            lang,
            statistics['vacancies_found'],
            statistics['vacancies_processed'],
            statistics['average_salary'],
        )
        site_statistics_table.append(table_raw)
    title = f'{site} Moscow'
    table_instance = AsciiTable(site_statistics_table, title)
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

    site_statistics = {}
    try:
        hh_statistics = get_hh_statistics(languages)
        site_statistics['HeadHunter'] = hh_statistics
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from hh.ru.")

    try:
        sj_statistics = get_sj_statistics(languages, api_key)
        site_statistics['SuperJob'] = sj_statistics
    except (ConnectionError, InvalidURL, HTTPError) as error:
        logging.error(f"{error}\nCan't get data from superjob.ru.")

    for site, statistics in site_statistics.items():
        langs_statistics_table = make_table(site, statistics)
        print(langs_statistics_table)


if __name__ == '__main__':
    main()
