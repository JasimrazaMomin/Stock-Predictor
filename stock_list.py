import requests
from bs4 import BeautifulSoup

URL = "https://stockanalysis.com/list/sp-500-stocks/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.findAll(class_="sym svelte-eurwtr")

stock_list = []

for result in results:
    children = result.findChildren("a", recursive=False)
    for child in children:
        stock_list.append(child.get_text())

print(stock_list)