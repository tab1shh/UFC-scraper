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

def filter_duplicates(fighter_url):
    # first check if the file is even in the specified path
    if 'fighter_stats.csv' in os.listdir(file_path):
        with open(file_path + '/' + 'fighter_stats.csv', 'r') as stats_csv_file:
            reader = csv.DictReader(stats_csv_file)
            # want to iterate throught each row in the csv file, and append the url to the list
            # then want to iterate through the list and remove duplicates
            scraped_urls = []
            for row in reader:
                scraped_urls.append(row['fighter_url'])

            for url in scraped_urls:
                if url in fighter_url:
                    fighter_url.remove(url)


def get_name(name):
    return name.split()[0].strip()

def get_SLpM(SLpM):
    SLpM_text = SLpM.text.split(':')[1]

    if '0.00' in SLpM_text:
        return 'NULL'
    else:
        return SLpM_text.split()[0].strip()

def get_strAcc(strAcc):
    strAcc_text = strAcc.text.split(':')[1]

    if '0%' in strAcc_text:
        return 'NULL'
    else:
        return strAcc_text.split()[0].strip()
    
def get_SApM(SApM):
    SApM_text = SApM.text.split(':')[1]

    if '0.00' in SApM_text:
        return 'NULL'
    else:
        return SApM_text.split()[0].strip()


def get_strDef(strDef):
    strDef_text = strDef.text.split(':')[1]

    if '0%' in strDef_text:
        return 'NULL'
    else:
        return strDef_text.split()[0].strip()

def get_TD_Avg(TD_Avg):
    TD_Avg_text = TD_Avg.text.split(':')[0]

    if '0.00' in TD_Avg_text:
        return 'NULL'
    else:
        return TD_Avg_text.split()[0].strip()
    
def get_TD_Acc(TD_Acc):
    TD_Acc_text = TD_Acc.text.split(':')[1]

    if '0%' in TD_Acc_text:
        return 'NULL'
    else:
        return TD_Acc_text.split()[0].strip()

def get_TD_Def(TD_Def):
    TD_Def_text = TD_Def.text.split(':')[1]

    if '0%' in TD_Def_text:
        return 'NULL'
    else:
        return TD_Def_text.split()[0].strip()

def get_Sub_Avg(Sub_Avg):
    Sub_Avg_text = Sub_Avg.text.split(':')[1]

    if '0.00' in Sub_Avg_text:
        return 'NULL'
    else:
        return Sub_Avg_text.split()[0].strip()

def scrape_test():
    if 'fighter_stats.csv' not in os.listdir(file_path):
        with open(file_path + '/' + 'fighter_stats.csv', 'w', newline='') as fighter_stats:
            writer = csv.writer(fighter_stats)
            writer.writerow(['fighter_name',
                             'career_SLpM',
                             'career_StrAcc',
                             'career_SApM',
                             'career_StrDef',
                            #  'career_TD_Avg',
                             'career_TD_Acc',
                             'career_TD_Def',
                             'career_Sub_Avg',
                             'fighter_url'])
        print('fighter_stats has been created.')
    else:
        print('Scraping to existing fighter_stats file...')

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
    print(f'Scraping {urls_to_scrape} fighters...')
    urls_scraped = 0

    with open(file_path + '/' + 'fighter_stats.csv', 'a+', newline='') as csv_f:
        writer = csv.writer(csv_f)

        for url in fighter_url:
            fighter_url = requests.get(url)
            fighter_url_soup = bs4.BeautifulSoup(fighter_url.text, 'lxml')
            fighter_stats = fighter_url_soup.select('li.b-list__box-list-item')

            name = fighter_url_soup.select('span')[0].text
            SLpM = get_SLpM(fighter_stats[5])
            StrAcc = get_strAcc(fighter_stats[6])
            SApM = get_SApM(fighter_stats[7])
            StrDef = get_strDef(fighter_stats[8])
            # TD_Avg = get_TD_Avg(fighter_stats[9])
            TD_Acc = get_TD_Acc(fighter_stats[10])
            TD_Def = get_TD_Def(fighter_stats[11])
            Sub_Avg = get_Sub_Avg(fighter_stats[12])

            writer.writerow([name.strip(), 
                             SLpM,
                             StrAcc,
                             SApM,
                             StrDef,
                            #  TD_Avg,
                             TD_Acc,
                             TD_Def,
                             Sub_Avg,
                             url])
            
            urls_scraped += 1

    print(f'{urls_scraped}/{urls_to_scrape} links scraped successfully')

