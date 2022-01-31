import requests
from pprint import pprint
from bs4 import BeautifulSoup
from pymongo import MongoClient, errors


def main(profession, database):
    url = 'https://hh.ru/search/vacancy'
    params = {'quick_filters': 'serials',
              'text': profession,
              'page': 0,
              'search_field': 'name',
              'items_on_page': 20
              }
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}
    print('Идет поиск вакансий')
    while True:
        response = requests.get(url, params=params, headers=headers)

        dom = BeautifulSoup(response.text, 'html.parser')
        blocks = dom.find_all('div', {'class': 'vacancy-serp-item'})
        for item in blocks:
            vacancy = {'_id': None, 'name': None, 'link': None, 'salary_min': None, 'salary_max': None,
                       'salary_currency': None}
            title = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            vacancy['name'] = title.getText()
            vacancy['link'] = title.get('href').split('?')[0]
            vacancy['_id'] = vacancy['link']

            try:
                salary = item.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"}).getText()
                salary = salary.replace('\u202f', '').replace('\xa0', '').split()
                if 'от' in salary:
                    vacancy['salary_min'] = int(salary[1])
                elif 'до' in salary:
                    vacancy['salary_max'] = int(salary[1])
                else:
                    vacancy['salary_min'] = int(salary[0])
                    vacancy['salary_max'] = int(salary[2])
                vacancy['salary_currency'] = salary[-1]
            except:
                pass

            try:
                database.insert_one(vacancy)
            except errors.DuplicateKeyError:
                database.update_one({'link': vacancy['link']}, {'$set': vacancy})

        print(f'Обработано страниц: {params["page"] + 1}')

        if dom.find('a', {'data-qa': 'pager-next'}):
            params['page'] += 1
        else:
            break


def search_by_salary(salary, database):
    vacancy_lst = []

    for item in database.find({'$and':
                               [{'salary_currency': 'руб.'},
                                {'$or': [{'salary_min': {'$gt': salary}}, {'salary_max': {'$gt': salary}}]}
                                ]}):
        vacancy_lst.append(item)
    pprint(vacancy_lst)


if __name__ == '__main__':
    client = MongoClient('127.0.0.1', 27017)
    search_string = 'python'

    db = client[search_string]
    vacancy_db = db.vacancy

    main(search_string, vacancy_db)

    search_salary = int(input('Ведите сумму желаемой зарплаты: '))
    search_by_salary(search_salary, vacancy_db)
