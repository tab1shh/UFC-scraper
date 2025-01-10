'''
name, height (cm), weight (lbs), reach, stance, date of birth, record (W-L-D), fighter url
'''

import requests
import bs4
import csv
import os
import re
from datetime import datetime

file_path = os.path.join(os.getcwd(), 'scraped_files')  
url_path = os.path.join(os.getcwd(), 'url_data')

def create_scraped_csv_file():
    if 'fighter_data.csv' not in os.listdir(file_path):
        with open(file_path + '/' + 'fighter_data.csv', 'w', newline='') as fighter_data:
            writer = csv.writer(fighter_data)
            writer.writerow(['first_name',
                             'last_name',
                             'height_cm',
                             'weight_pounds',
                             'reach_cm',
                             'stance',
                             'date_of_birth',
                             'f_wins',
                             'f_losses',
                             'f_draws',
                             'f_dc_nc',
                             'fighter_url'])
        print('fighter_data.csv has been created.')
    else:
        print('Scraping to existing fighter_data.csv file...')

def filter_duplicates(fighter_url):
    # first check if the file is even in the specified path
    if 'fighter_data.csv' in os.listdir(file_path):
        with open(file_path + '/' + 'fighter_data.csv', 'r') as fight_csv_file:
            reader = csv.DictReader(fight_csv_file)
            # want to iterate throught each row in the csv file, and append the url to the list
            # then want to iterate through the list and remove duplicates
            scraped_urls = []
            for row in reader:
                scraped_urls.append(row['fighter_url'])

            for url in scraped_urls:
                if url in fighter_url:
                    fighter_url.remove(url)

def get_last_name(name):
    if len(name) > 1:
        return name[-1]
    else:
        return 'NULL'

def get_height(height):
    height_text = height.text.split(':')[1].strip()
    if '--' in height_text.split("'"):
        return 'NULL'
    else:
        height_ft = height_text[0]
        height_in = height_text.split("'")[1].strip().strip('"')
        height_cm = ((int(height_ft) * 12.0) * 2.54) + (int(height_in) * 2.54)
        return height_cm


def get_reach(reach):
    reach_text = reach.text.split(':')[1]
    if '--' in reach_text:
        return 'NULL'
    else:
        return round(int(reach_text.strip().strip('"')) * 2.54, 2)

def get_weight(weight):
    weight_text = weight.text.split(':')[1]
    if '--' in weight_text:
        return 'NULL'
    else:
        return weight_text.split()[0].strip()

def get_stance(stance):
    try:
        stance_text = stance.text.split(':')[1].strip()
        if stance_text == '':
            return 'NULL'
        else:
            return stance_text
    except IndexError:
        return 'NULL'

def get_dob(dob):
    dob_text = dob.text.split(':')[1].strip()
    if dob_text == '--':  # Handle missing DOB
        return 'NULL'
    else:
        try:
            # Parse and format DOB
            dob_datetime = datetime.strptime(dob_text, '%b %d, %Y')
            return dob_datetime.strftime('%Y-%m-%d')  # Return in 'YYYY-MM-DD' format
        except ValueError:
            return 'INVALID_DATE'  # Handle unexpected date formats

def scrape_all_fighters():
    fighter_url = []
    if 'fighter_urls.csv' in os.listdir(url_path):
        with open(url_path + '/' + 'fighter_urls.csv', 'r') as fighter_csv_file:
            reader = csv.reader(fighter_csv_file)
            for row in reader:
                fighter_url.append(row[0])

    else:
        print("fighter_urls.csv is missing, run get_urls.get_fighter_urls again...")

    filter_duplicates(fighter_url)

    urls_to_scrape = len(fighter_url)

    if urls_to_scrape == 0:
        print('Fighters have already been scraped.')

    else:
        create_scraped_csv_file()

        print(f'Scraping {urls_to_scrape} fighters...')
        urls_scraped = 0

        with open(file_path + '/' + 'fighter_data.csv', 'a+', newline='') as csv_f:
            writer = csv.writer(csv_f)

            for url in fighter_url:
                fighter_url = requests.get(url)
                fighter_url_soup = bs4.BeautifulSoup(fighter_url.text, 'lxml')


                # select statements
                name = fighter_url_soup.select('span')[0].text.split() # gets the first span element which is the full name, then split into a list of first and last name
                details = fighter_url_soup.select('li.b-list__box-list-item') # details like height, weight, reach, etc
                # goes to first span with specific text, extracts the record portion, removes leading space and split '-' into a list so like ['16', '0', '0']
                record = fighter_url_soup.select('span.b-content__title-record')[0].text.split(':')[1].strip().split('-') 


                # scraping fight details
                fighter_first_name = name[0]
                fighter_last_name = get_last_name(name)
                fighter_height = get_height(details[0])
                fighter_weight_pounds = get_weight(details[1])
                fighter_reach = get_reach(details[2])
                fighter_stance = get_stance(details[3])
                fighter_dob = get_dob(details[4])
                fighter_wins = record[0]
                fighter_losses = record[1]
                # get draws
                if (len(record[-1]) > 1): # if last element has more than 1 character
                    fighter_draws = record[-1][0] # take the first character (e.g "1" from "(1 NC)")
                else: 
                    fighter_draws = record[-1] # use entire last element

                # get nc/dq
                if (len(record[-1]) > 1):
                    fighter_nc_dq = record[-1].split('(')[-1][0] # split by ( and take the part after it, then extract the first character
                else:
                    fighter_nc_dq = 'NULL'

                writer.writerow([fighter_first_name.strip(),
                                 fighter_last_name.strip(),
                                 fighter_height,
                                 fighter_weight_pounds,
                                 fighter_reach,
                                 fighter_stance,
                                 fighter_dob[0:10],
                                 fighter_wins,
                                 fighter_losses,
                                 fighter_draws,
                                 fighter_nc_dq,
                                 url])


                
                urls_scraped += 1

        print(f'{urls_scraped}/{urls_to_scrape} links scraped successfully')


