import requests 
import csv
from bs4 import BeautifulSoup

url = 'https://www.pointspreads.com/ufc/fighters/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

first_names = soup.find_all('div', class_='fighter_first_name')
last_names = soup.find_all('div', class_='fighter_last_name')

with open('active_fighters.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['First Name', 'Last Name'])

    # Extract and write the first and last names
    for first_name, last_name in zip(first_names, last_names):
        first_name_text = first_name.text.strip()
        last_name_text = last_name.text.strip()
        writer.writerow([first_name_text, last_name_text])

print("Names have been saved to 'fighter_names.csv'.")
