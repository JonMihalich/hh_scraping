import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json

def get_headers():
    return Headers(browser='firefox', os='win').generate()

# Начало парсинга
head_hunter_html = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=0', headers=get_headers()).text
head_hunter_soup = BeautifulSoup(head_hunter_html, 'lxml')
head_hunter_all_vacancy = head_hunter_soup.find_all('div', class_='serp-item')

pars = []

# извлечение определенных данных
for vacan in head_hunter_all_vacancy:
    h3_tag = vacan.find('h3')
    a_tag = h3_tag.find('a')
    a_tag_text = a_tag.text

    # Извлечение ссылки и названия компании
    if 'Django' in a_tag_text or 'Flack' in  a_tag_text:
        name_company = a_tag_text
        link = a_tag['href']

        # извелечение вилки заработной платы
        fork = vacan('span')[2]
        fork1 = fork.text.replace('\u202f', ' ')

        # извлечение названия компании
        company = vacan('a')[1]
        company1 = company.text

        # извлечение города
        linking = BeautifulSoup(requests.get(link, headers=get_headers()).text, 'lxml')
        city_text = linking.find('div', class_='vacancy-company-redesigned')
        for city1 in city_text:
            city = city1.text

        # добавление всей информации в список
        pars.append(
            {
            'title': name_company,
            'link': link,
            'wage_fork': fork1,
            'company': company1,
            'city': city
            }
        )
# Записись в json формат!
with open('parsing_file_hh_ru.json', 'w') as file:
    json.dump(pars, file, indent=1)