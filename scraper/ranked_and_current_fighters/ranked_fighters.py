'''
scrape the names of the fighters on the rankings
'''

import requests 
import bs4
import csv
import os

url = 'https://www.ufc.com/rankings'
file_path = os.path.join(os.getcwd(), 'ranked_and_current_fighters')  
os.makedirs(file_path, exist_ok=True)

response = requests.get(url)

soup = bs4.BeautifulSoup(response.text, 'lxml')

name_elements = soup.find_all('td', class_='views-field views-field-title')


with open('ufc_rankings.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['Rank', 'Name'])

    for index, element in enumerate(name_elements, start=1):
        name = element.a.text.strip()  # get the text inside the <a> tag
        writer.writerow([index, name])  # write rank and name to the CSV

print("Names have been saved to 'ufc_rankings.csv'.")
