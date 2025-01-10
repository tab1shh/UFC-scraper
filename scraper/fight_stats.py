'''
fighter name, knockdown (KD), sig strikes attempted and succeeded, total strikes attempted and succeeded, takedowns attempted and succeded, submissions attempted, reversals, control time, fight url
'''

import requests
import bs4
import csv
import os
import re
from datetime import datetime

file_path = os.path.join(os.getcwd(), 'scraped_files')  
url_path = os.path.join(os.getcwd(), 'url_data')

def filter_duplicates(fight_url):
    # first check if the file is even in the specified path
    if 'fight_stats.csv' in os.listdir(file_path):
        with open(file_path + '/' + 'fight_stats.csv', 'r') as stats_csv_file:
            reader = csv.DictReader(stats_csv_file)
            # want to iterate throught each row in the csv file, and append the url to the list
            # then want to iterate through the list and remove duplicates
            scraped_urls = []
            for row in reader:
                scraped_urls.append(row['fight_url'])

            for url in scraped_urls:
                if url in fight_url:
                    fight_url.remove(url)


def get_fighter_name(fight_url_soup, fight_stats, fighter):
    if fighter == 1:
        try:
            return fight_stats[0].text
        except:
            return fight_url_soup.select('a.b-fight-details__person-link')[0].text
    elif fighter == 2:
        try:
            return fight_stats[1].text
        except:
            return fight_url_soup.select('a.b-fight-details__person-link')[1].text

def get_striking_stats(fight_stats, fighter):
    if fighter == 1:
        try:
            return (
                fight_stats[2].text, # knockdowns
                fight_stats[4].text.split(' of ')[0], # significant strikes successful
                fight_stats[4].text.split(' of ')[1], # significant strikes attempted
                fight_stats[8].text.split(' of ')[0], # total strikes successful
                fight_stats[8].text.split(' of ')[1] # total strikes attempted
            )
        except:
            return (
                'NULL',
                'NULL',
                'NULL',
                'NULL',
                'NULL',
            )
        
    elif fighter == 2:
        try:
            return (
                fight_stats[3].text, # knockdowns
                fight_stats[5].text.split(' of ')[0], # significant strikes successful
                fight_stats[5].text.split(' of ')[1], # significant strikes attempted
                fight_stats[9].text.split(' of ')[0], # total strikes successful
                fight_stats[9].text.split(' of ')[1] # total strikes attempted
            )
        except:
            return (
                'NULL',
                'NULL',
                'NULL',
                'NULL',
                'NULL',
            )



def get_grappling_stats(fight_stats, fighter):
    if fighter == 1:
        try:
            return (
                fight_stats[10].text.split(' of ')[0], # taekdowns successful
                fight_stats[10].text.split(' of ')[1], # takedowns attempted
                fight_stats[14].text, # submissions attempted
                fight_stats[16].text, # reversals
                fight_stats[18].text # control time

            )
        except:
            return (
                'NULL',
                'NULL',
                'NULL',
                'NULL',
                'NULL',
            )
        
    elif fighter == 2:
        try:
            return (
                fight_stats[11].text.split(' of ')[0], # taekdowns successful
                fight_stats[11].text.split(' of ')[1], # takedowns attempted
                fight_stats[15].text, # submissions attempted
                fight_stats[17].text, # reversals
                fight_stats[19].text # control time
            )
        except:
            return (
                'NULL',
                'NULL',
                'NULL',
                'NULL',
                'NULL',
            )

def scrape_fightstats():
    if 'fight_stats.csv' not in os.listdir(file_path):
        with open(file_path + '/' + 'fight_stats.csv', 'w', newline='') as fight_stats:
            writer = csv.writer(fight_stats)
            writer.writerow(['fighter_name',
                             'knockdowns',
                             'sig_strikes_attempted',
                             'sig_strikes_succeeded',
                             'total_strikes_attempted',
                             'total_strikes_succeeded',
                             'takedowns_attempted',
                             'takedown_succeeded',
                             'submission_attempted',
                             'reversals',
                             'control_time',
                             'event_name',
                             'fight_url'])
        print('fight_stats has been created.')
    else:
        print('Scraping to existing fight_stats file...')

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
    print(f'Scraping {urls_to_scrape} fights...')
    urls_scraped = 0

    with open(file_path + '/' + 'fight_stats.csv', 'a+', newline='') as csv_f:
        writer = csv.writer(csv_f)

        for url in fight_url:
            fight_url = requests.get(url)
            fight_url_soup = bs4.BeautifulSoup(fight_url.text, 'lxml')
            fight_stats = fight_url_soup.select('p.b-fight-details__table-text')

            # stats for first fighter
            fighter_name = get_fighter_name(fight_url_soup, fight_stats, 1)
            (knockdowns,
            sig_strikes_attempted,
            sig_strikes_succeeded,
            total_strikes_attempted,
            total_strikes_succeeded) = get_striking_stats(fight_stats, 1)

            (takedowns_attempted,
            takedown_succeeded,
            submission_attempted,
            reversals,
            control_time) = get_grappling_stats(fight_stats, 1)

            event = fight_url_soup.h2.text

            writer.writerow([fighter_name.strip(),
                             knockdowns.strip(),
                             sig_strikes_attempted.strip(),
                             sig_strikes_succeeded.strip(),
                             total_strikes_attempted.strip(),
                             total_strikes_succeeded.strip(),
                             takedowns_attempted.strip(),
                             takedown_succeeded.strip(),
                             submission_attempted.strip(),
                             reversals.strip(),
                             control_time.strip(),
                             event.strip(),
                             url])
            
            # stats for second fighter
            fighter_name = get_fighter_name(fight_url_soup, fight_stats, 2)
            (knockdowns,
            sig_strikes_attempted,
            sig_strikes_succeeded,
            total_strikes_attempted,
            total_strikes_succeeded) = get_striking_stats(fight_stats, 2)

            (takedowns_attempted,
            takedown_succeeded,
            submission_attempted,
            reversals,
            control_time) = get_grappling_stats(fight_stats, 2)

            writer.writerow([fighter_name.strip(),
                             knockdowns.strip(),
                             sig_strikes_attempted.strip(),
                             sig_strikes_succeeded.strip(),
                             total_strikes_attempted.strip(),
                             total_strikes_succeeded.strip(),
                             takedowns_attempted.strip(),
                             takedown_succeeded.strip(),
                             submission_attempted.strip(),
                             reversals.strip(),
                             control_time.strip(),
                             event.strip(),
                             url])
            
            urls_scraped += 1

    print(f'{urls_scraped}/{urls_to_scrape} links scraped successfully')

