import requests
from bs4 import BeautifulSoup as bs


class Parser:
    url = 'https://eparhia992.by/component/search/?searchword=%D0%BA%D1%83%D1%88%D0%BD%D0%B5%D1%80%D0%B5%D0%B2%D0%B8%' \
          'D1%87&searchphrase=all&limit=0'

    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    names = soup.find_all('a')
    pub_date = soup.find_all(class_='result-created')
    name_result = [x for x in names if 'item' in x.get('href')]
    string_result = min(len(pub_date), len(name_result))
