import json
import requests
from bs4 import BeautifulSoup


def main():
    vacancy_list = []

    while True:
        response = requests.get(url, params=params, headers=headers)

        dom = BeautifulSoup(response.text, 'html.parser')

        blocks = dom.find_all('div', {'class': 'vacancy-serp-item'})

        for item in blocks:
            vacancy = {'name': None, 'link': None, 'salary_min': None, 'salary_max': None, 'salary_currency': None}
            title = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
            vacancy['name'] = title.getText()
            vacancy['link'] = title.get('href')
            vacancy['page'] = params['page'] + 1
            try:
                salary = item.find('span', {"data-qa": "vacancy-serp__vacancy-compensation"}).getText().split()
                if 'от' in salary:
                    vacancy['salary_min'] = salary[1] + salary[2]
                elif 'до' in salary:
                    vacancy['salary_max'] = salary[1] + salary[2]
                else:
                    vacancy['salary_min'] = salary[0] + salary[1]
                    vacancy['salary_max'] = salary[3] + salary[4]
                vacancy['salary_currency'] = salary[-1]
            except:
                pass

            vacancy_list.append(vacancy)

        if dom.find('a', {'data-qa': 'pager-next'}):
            params['page'] += 1
        else:
            break

    with open('hh.json', 'w', encoding='utf-8') as f:
        json.dump(vacancy_list, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    profession = 'продавец'
    url = 'https://hh.ru/search/vacancy'
    params = {'quick_filters': 'serials',
              'text': profession,
              'page': 0,
              'search_field': 'name',
              }
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'}

    main()
