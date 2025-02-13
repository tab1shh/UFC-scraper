import requests
import bs4
import csv
import os
import time

# helper function to write URLs to a CSV file
def write_urls_to_csv(file, urls):
    # new directory for the csv files
    os.makedirs('url_data', exist_ok=True)
    path = os.getcwd() + '/url_data'

    # save file to new directory and add urls to the file
    try:
        with open(path + '/' + file, 'w', newline='') as f:
            writer = csv.writer(f)
            for url in urls:
                writer.writerow([url])
    except Exception as e:
        print(f'Error writing to file: {e}')

# need to scrape each event, and from each event can scrape each fight
def get_event_urls():
    print('Scraping for event links...')
    main_url = requests.get('http://ufcstats.com/statistics/events/completed?page=all')
    event_soup = bs4.BeautifulSoup(main_url.text, 'lxml')

    # extract href value from each <a> tag, and ensure that href exists and if the keyword event-details is also present
    event_urls = [] # store the event urls

    # loop through all <a> tags 
    for item in event_soup.find_all('a'):
        # get the href attribvute of the <a> tag, and check if the href and contains the keyword 'event-details'
        href = item.get('href')

        if href and 'event-details' in href:
            event_urls.append(href)

    write_urls_to_csv('event_urls.csv', event_urls)

    print(f'Event links successfully scraped.\nTotal:{len(event_urls)}')

# scrapes url of each UFC fight from ufcstats.com, using the event urls 
def get_fight_urls():
    path = os.getcwd() + '/url_data'

    if os.path.exists(path + '/event_urls.csv'):
        with open(path + '/' + 'event_urls.csv', 'r', newline='') as csv_events:
            reader = csv.reader(csv_events)

            event_urls = [] # used to store the URLs

            for row in reader:
                if row:
                    event_urls.append(row[0]) # adds URL to the list
    else:
        print("The file 'event_urls.csv' does not exist. Please check the path or create the file.")
        return

    print('Scraping for fight links...')

    fight_urls = []

    for url in event_urls:
        event = requests.get(url)
        event_soup = bs4.BeautifulSoup(event.text, 'lxml')

        for item in event_soup.find_all('a', class_='b-flag b-flag_style_green'):
            href = item.get('href')

            if href and 'fight-details' in href:
                fight_urls.append(href)

    write_urls_to_csv('fight_urls.csv', fight_urls)
    print(f'Fight links successfully scraped.\nTotal:{len(fight_urls)}')

# scrapes url of each UFC fighter from ufcstats.com
def get_fighter_urls():
    print('Scraping for fighter links...')

    # create a list of each fighter url alphabetically
    fighter_alpha_url = []

    for letter in 'abcdefghijklmnopqrstuvwxyz':
        fighter_alpha_url.append(requests.get(f'http://www.ufcstats.com/statistics/fighters?char={letter}&page=all'))
        time.sleep(1)

    # iterate through each page and get fighter links
    # so loop through each URL in the fighter_alpha_url list because it contains the pages for each letter of the alphabet
    fighter_list = []

    for url in fighter_alpha_url: 
        soup = bs4.BeautifulSoup(url.text, 'lxml')
        fighter_list.append(soup)

    # get the fighter URLs from the scraped pages
    fighter_urls = [] 
    for fighter in fighter_list:
        for link in fighter.select('a.b-link')[1::3]: # select every third link skipping the first one because there are 3 links and only need one
            fighter_urls.append(link.get('href'))

    write_urls_to_csv('fighter_urls.csv', fighter_urls)

    print(f'Fight links successfully scraped.\nTotal:{len(fighter_urls)}')