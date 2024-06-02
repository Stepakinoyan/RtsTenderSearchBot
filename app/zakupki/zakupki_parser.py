import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from pytz import timezone
from httpx import AsyncClient
from zakupki.schemas import Zakupki


headers = {"user-agent": UserAgent().random}


async def get_data():
    async with AsyncClient() as client:
        response = await client.get(
            "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=setting_order_lrjaimav&sortBy=UPDATE_DATE&ppRf615=on&af=on&ca=on&currencyIdGeneral=-1&delKladrIds=5277401%2C5277403%2C5277407&delKladrIdsCodes=25000000000%2C28000000000%2C79000000000&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0",
            headers=headers,
        )

    soup = BeautifulSoup(response.text, "lxml")
    json_data = []
    for card in soup.find_all(
        "div", class_="search-registry-entry-block box-shadow-search-input"
    ):
        url = f'https://zakupki.gov.ru{card.find("a").get("href")}'
        price = card.find("div", class_="price-block__value").text
        description = " ".join(
            [i.text for i in card.find_all("div", class_="registry-entry__body-value")]
        )
        date = datetime.strptime(
            soup.find("div", class_="data-block__value").text, "%d.%m.%Y"
        ).date()

        json_data.append(
            Zakupki(url=url, price=price, description=description, post_date=date)
        )

    return json_data


async def get_new_data():
    get_date_now = datetime.now()
    zone = timezone("Asia/Yakutsk")
    dt = zone.localize(get_date_now)
    json_data = []
    for item in await get_data():
        if item.post_date == dt.date():
            json_data.append(item.model_dump())
    return json_data
