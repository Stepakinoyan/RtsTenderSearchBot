import datetime
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from pydantic import BaseModel
from datetime import datetime
from pytz import timezone

class Zakupki(BaseModel):
    price: str
    description: str
    url: str
    date: datetime


headers = {'user-agent': UserAgent().random}

response = requests.get("https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=setting_order_lrjaimav&sortBy=UPDATE_DATE&ppRf615=on&af=on&ca=on&currencyIdGeneral=-1&delKladrIds=5277401%2C5277403%2C5277407&delKladrIdsCodes=25000000000%2C28000000000%2C79000000000&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0", headers=headers)

soup = BeautifulSoup(response.text, 'lxml')

def get_data():
    json_data = []
    
    urls = list(filter(lambda x: type(x) is str and "common-info" in x, [f"https://zakupki.gov.ru{url.get('href')}" for url in soup.find_all('a')]))
    prices = [price.text.replace('\n', '').replace(' ', '') for price in soup.find_all('div', class_="price-block__value")]
    descriptions = [description.text for description in soup.find_all("div", class_='registry-entry__body-value')][::2]
    dates = [datetime.strptime(date.text, '%d.%m.%Y') for date in soup.find_all("div", class_='data-block__value')][::3]

    for url, (description, price, date) in list((zip(urls, zip(descriptions, prices, dates)))):
        zakupki = Zakupki(url=url, description=description, price=price, date=date)
        json_data.append(zakupki)

    return json_data

<<<<<<< HEAD


=======
>>>>>>> origin/master
def get_new_data():
    get_date_now = datetime.now()
    zone = timezone("Asia/Vladivostok")
    dt = zone.localize(get_date_now)
    json_data = []
    for item in get_data():
        if item.date.date() == dt.date():
<<<<<<< HEAD
            json_data.append(item)
=======
            json_data.append(item.model_dump())
>>>>>>> origin/master
    return json_data