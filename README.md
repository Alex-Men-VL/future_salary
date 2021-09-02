#Статистика вакансий для программистов

Скрипт позволяет получить информацию по количеству вакансий и средней 
заработной платы для 10 популярных языков программирования.

Статистика выводится с сайтов [hh.ru](https://spb.hh.ru/) и
[superjob.ru](https://www.superjob.ru/) для вакансий из Москвы, выложенных
не более месяца назад.

Статистика выводится в виде двух таблиц для каждого сайта.

## Запуск

- Скачайте код;
- Установите зависимости командой:
```bash
pip install -r requirements.txt
```
- Запустите скрипт командой:
```bash
python3 main.py 
```

## Переменные окружения

Часть данных берется из переменных окружения. 
Чтобы их определить, создайте файл `.env` 
рядом с `main.py` и запишите туда данные в таком формате: 
`ПЕРЕМЕННАЯ=значение`.

Доступна одна переменные:
- `SJ_TOKEN` - токен с сайта [API SuperJob](https://api.superjob.ru/).
