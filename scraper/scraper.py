import requests
from bs4 import BeautifulSoup
from datetime import date
import csv

url = "https://www.coinlore.com/"
response = requests.get(url)

today = date.today()
today = today.isoformat()



if response.status_code == 200:
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    filename = 'records.csv'
    currencies = []
    for i in range(1, 5):
        row = soup.find('tr', id=str(i))
        if row:

            name = row.find('td', class_="currency-name txtl")
            symbol = row.find('p', class_="m-0 crypto-coin-t d-block text-muted coin-name small")
            price = row.find('td', class_="txtr price_td_p")

            crypto_data = {
                'name':name.text.strip() if name else 'N/A',
                'symbol':symbol.text.strip() if symbol else 'N/A',
                'price': price.text.strip() if price else 'N/A',
                'date': today if today else 'N/A'
            }

            currencies.append(crypto_data)

    if not currencies:
        print("No data found.")
        exit()

    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=currencies[0].keys())
        if csvfile.tell() == 0:
                csvwriter.writeheader()

        csvwriter.writerows(currencies)


    
    

else:
    print("Failed to retrieve webpage.")
    exit()