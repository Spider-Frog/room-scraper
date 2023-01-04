import requests
from lxml import html


def collect_residences(city_code):
    page = requests.get(f"https://holland2stay.com/residences.html?available_to_book=179,336&city={city_code}&product_list_limit=30")

    tree = html.fromstring(page.text)

    return tree.xpath("/html/body/div[3]/main/div[2]/div/section/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div")


city_codes = [
    28,
    29,
    6217,
    6209
]

residences = []

for city_code in city_codes:
    for collected_residences in collect_residences(city_code):
        residences.append(collected_residences)

residence_total = len(residences)
book_directly_total = 0
lottery_total = 0

for residence in residences:
    name = residence.xpath("div[2]/div/h4")[0].text
    label = residence.xpath("div[2]/div/h4/span")[0].text.strip()

    match label:
        case "BOOK DIRECTLY":
            book_directly_total += 1
        case "LOTTERY":
            lottery_total += 1

    url = residence.xpath("div[3]/a")[0].get('href')

    rent = residence.xpath("div[3]/div/div")[0].text
    building = residence.xpath("div[2]/ul[1]/li[3]/span")[0].text
    city = residence.xpath("div[2]/ul[1]/li[2]/span")[0].text

    print(f"{building}, {name} {city}, {rent}")

print(f"Total: {residence_total}")
print(f"Book directly: {book_directly_total}")
print(f"Lottery: {lottery_total}")
