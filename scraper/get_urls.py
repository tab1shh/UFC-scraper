import requests
import bs4
import csv
import os
import time

# helper function to write URLs to a CSV file
def write_urls_to_csv(file, new_urls):
    """Append only new URLs to the existing file."""
    os.makedirs('url_data', exist_ok=True)
    path = os.path.join(os.getcwd(), 'url_data', file)
    
    # Load existing URLs from the file
    existing_urls = set()
    if os.path.exists(path):
        with open(path, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    existing_urls.add(row[0])  # Store existing URLs in a set

    # Filter out already existing URLs
    new_urls = [url for url in new_urls if url not in existing_urls]

    # Append only new URLs
    if new_urls:
        with open(path, 'a', newline='') as f:  # Open in append mode
            writer = csv.writer(f)
            for url in new_urls:
                writer.writerow([url])
        print(f"✅ {len(new_urls)} new URLs added to {file}")
    else:
        print(f"✅ No new URLs found for {file}. Data is already up to date.")


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
    path = os.path.join(os.getcwd(), 'url_data')

    # Load existing fight URLs
    existing_fight_urls = set()
    if os.path.exists(path + '/fight_urls.csv'):
        with open(path + '/fight_urls.csv', 'r', newline='') as csv_fights:
            reader = csv.reader(csv_fights)
            for row in reader:
                if row:
                    existing_fight_urls.add(row[0])  # Store existing fight URLs

    # Load event URLs (to scrape new fights from new events)
    if not os.path.exists(path + '/event_urls.csv'):
        print("⚠️ The file 'event_urls.csv' does not exist. Please scrape events first.")
        return

    with open(path + '/event_urls.csv', 'r', newline='') as csv_events:
        reader = csv.reader(csv_events)
        event_urls = [row[0] for row in reader if row]

    print('🔄 Checking for new fight links...')

    fight_urls = set(existing_fight_urls)  # Start with existing fights

    for url in event_urls:
        if url in fight_urls:  # Skip already scraped events
            continue
        
        event = requests.get(url)
        event_soup = bs4.BeautifulSoup(event.text, 'lxml')

        for item in event_soup.find_all('a', class_='b-flag b-flag_style_green'):
            href = item.get('href')
            if href and 'fight-details' in href:
                fight_urls.add(href)  # Add to the fight URL set

    # Find only new fight URLs
    new_fight_urls = fight_urls - existing_fight_urls

    # Append only new fights to the CSV file
    write_urls_to_csv('fight_urls.csv', new_fight_urls)
    print(f'Fight links successfully scraped.\nTotal:{len(fight_urls)}')

# scrapes url of each UFC fighter from ufcstats.com
def get_fighter_urls():
    print('🔄 Checking for new fighter links...')

    path = os.path.join(os.getcwd(), 'url_data')

    # Load existing fighter URLs
    existing_fighter_urls = set()
    if os.path.exists(path + '/fighter_urls.csv'):
        with open(path + '/fighter_urls.csv', 'r', newline='') as csv_fighters:
            reader = csv.reader(csv_fighters)
            for row in reader:
                if row:
                    existing_fighter_urls.add(row[0])  # Store existing fighter URLs

    # Create a list of alphabetically ordered fighter pages (A-Z)
    fighter_alpha_urls = [f'http://www.ufcstats.com/statistics/fighters?char={letter}&page=all' for letter in 'abcdefghijklmnopqrstuvwxyz']

    new_fighter_urls = set()

    for url in fighter_alpha_urls:
        fighter_page = requests.get(url)
        soup = bs4.BeautifulSoup(fighter_page.text, 'lxml')

        for link in soup.select('a.b-link')[1::3]:  # Get fighter profile links
            href = link.get('href')
            if href and href not in existing_fighter_urls:
                new_fighter_urls.add(href)

    # Append only new fighter URLs to the CSV file
    write_urls_to_csv('fighter_urls.csv', new_fighter_urls)

    print(f'Fight links successfully scraped.\nTotal:{len(new_fighter_urls)}')