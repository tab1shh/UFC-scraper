'''
fighter1, fighter2, gender, weight class, winner, method of winning (METHOD), round won (ROUND), time in said round (TIME), fight url
'''

import requests
import bs4
import csv
import os
import re

file_path = os.path.join(os.getcwd(), 'scraped_files')  
url_path = os.path.join(os.getcwd(), 'url_data')

def create_scraped_csv_file():
    if 'fight_data.csv' not in os.listdir(file_path):
        with open(file_path + '/' + 'fight_data.csv', 'w', newline='') as fight_data:
            writer = csv.writer(fight_data)
            writer.writerow(['event',
                            'fighter1',
                            'fighter2',
                            'gender',
                            'weight_class',
                            'title_fight',
                            'winner',
                            'method_of_winning',
                            'number_of_rounds',
                            'round_won',
                            'time_won',
                            'fight_url'
                            ])
        print('fight_data.csv has been created.')
    else:
        print('Scraping to existing fight_data.csv file...')

        
def filter_duplicates(fight_url):
    # first check if the file is even in the specified path
    if 'fight_data.csv' in os.listdir(file_path):
        with open(file_path + '/' + 'fight_data.csv', 'r') as fight_csv_file:
            reader = csv.DictReader(fight_csv_file)


            # want to iterate throught each row in the csv file, and append the url to the list
            # then want to iterate through the list and remove duplicates
            scraped_urls = []
            for row in reader:
                scraped_urls.append(row['fight_url'])

            for url in scraped_urls:
                if url in fight_url:
                    fight_url.remove(url)

# scrape both fighters
def get_fighters(fight_names, fight_soup):

    try:
        return fight_names[0].text, fight_names[1].text
    except:
        return fight_soup.select('a.b-fight-details__person-link')[0].text, fight_soup.select('a.b-fight-details__person-link')[1].text

# scrape gender of fight
def get_gender(fight_wc_or_gender):
    if 'Women' in fight_wc_or_gender[0].text:
        return 'F'
    else:
        return 'M'
    
def get_title_fight(fight_wc_or_gender):
    if 'Title' in fight_wc_or_gender[0].text:
        return 'Title Fight'
    else:
        return 'NULL'

# scrape weight class
def get_weight_class(fight_wc_or_gender):
    if 'Women' in fight_wc_or_gender[0].text.strip():
        return "Women's " + re.findall(r'\w*weight',fight_wc_or_gender[0].text.strip())[0]
    else:
        try:
            return re.findall(r'\w*weight',fight_wc_or_gender[0].text.strip())[0]
        except:
            return 'NULL'

# scrape the way the match was won (KO, NC etc)
def get_method_of_winning(select_result, select_result_details):
    if 'Decision' in select_result[0].text.split(':')[1]:
        return select_result[0].text.split(':')[1].split()[0], select_result_details[0].text.split(':')[1].split()[-1]
    else:
        return select_result[0].text.split(':')[1], select_result_details[0].text.split(':')[1].split()[-1]


def scrape_all_fights():
    fight_url = []
    if 'fight_urls.csv' in os.listdir(url_path):
        with open(url_path + '/' + 'fight_urls.csv', 'r') as fight_csv_file:
            reader = csv.reader(fight_csv_file)
            for row in reader:
                fight_url.append(row[0])

    else:
        print("fight_urls.csv is missing, run get_urls.get_fight_urls again...")

    filter_duplicates(fight_url)

    urls_to_scrape = len(fight_url)

    if urls_to_scrape == 0:
        print('Fights have already been scraped.')

    else:
        create_scraped_csv_file()

        print(f'Scraping {urls_to_scrape} fights...')
        urls_scraped = 0

        with open(file_path + '/' + 'fight_data.csv', 'a+', newline='') as csv_f:
            writer = csv.writer(csv_f)

            for url in fight_url:
                fight_url = requests.get(url)
                fight_url_soup = bs4.BeautifulSoup(fight_url.text, 'lxml')


                # select statements
                overview = fight_url_soup.select('i.b-fight-details__text-item') # overview of method, round, refree, etc
                fight_wc_or_gender = fight_url_soup.select('i.b-fight-details__fight-title') # gives weight class and gender
                fight_names = fight_url_soup.select('p.b-fight-details__table-text') # gets both names form the table
                win_lose = fight_url_soup.select('i.b-fight-details__person-status')
                select_result = fight_url_soup.select('i.b-fight-details__text-item_first') # gives method of winning
                select_result_details = fight_url_soup.select('p.b-fight-details__text') # additional details on the win, like cut above eye, etc


                # scraping fight details
                event = fight_url_soup.h2.text
                fighter1, fighter2 = get_fighters(fight_names, fight_url_soup)
                weight_class = get_weight_class(fight_wc_or_gender)
                gender = get_gender(fight_wc_or_gender)
                title_fight = get_title_fight(fight_wc_or_gender)
                result, result_details = get_method_of_winning(select_result, select_result_details)
                num_of_rounds = overview[2].text.split(':')[1].strip()[0]
                finish_round = overview[0].text.split(':')[1]
                finish_time = re.findall(r'\d:\d\d',overview[1].text)[0]

                if (win_lose[0].text.strip()=='W') | (win_lose[1].text.strip()=='W'):
                    if (win_lose[0].text.strip()=='W'):
                        winner = fighter1
                    else:
                        winner = fighter2
                else:
                    winner = 'NULL'


                writer.writerow([event.strip(),
                                 fighter1.strip(),
                                 fighter2.strip(),
                                 gender,
                                 weight_class.strip(),
                                 title_fight,
                                 winner.strip(),
                                 result.strip(),
                                 num_of_rounds.strip(),
                                 finish_round.strip(),
                                 finish_time.strip(),
                                 url
                                 ])


                
                urls_scraped += 1

        print(f'{urls_scraped}/{urls_to_scrape} links scraped successfully')

