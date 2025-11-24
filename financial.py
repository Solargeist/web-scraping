import sys
import os
from bs4 import BeautifulSoup
import requests
import time

def extract_html(url):
    print('Сплю 5 секуд')
    time.sleep(5)
    headers = {'User-Agent': 'Mozilla/5.0', 'Accept':'text/html'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Url doesn't exist: {url}. No such ticker")
    
    html = response.text
    return html

def parse(html, field):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('div', class_='row lv-0 yf-t22klz')
    res = None
    for row in rows:
        elem = row.find('div', class_='rowTitle')
        if elem.get('title') == field:
            res = row
    if not res:
        raise Exception("No such field")
    
    values = []
    cols = list(res.find_all('div'))[3::]
    for col in cols:
        values.append(col.text.strip())
    values = tuple(values)
    return values

    
if __name__ == "__main__":
    try:
        args = sys.argv
        if len(args) != 3:
            raise Exception('Введите: ./financial.py <ticker> <field>')
        ticker = args[1].upper()
        field = args[2].lower().title()
        url = f"https://finance.yahoo.com/quote/{ticker}/financials"
        html = extract_html(url)
        values = parse(html, field)
        print(values)
    except Exception as e:
        print(e)