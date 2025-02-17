import get_urls, fight_data as fight_data, fighter_data as fighter_data, fight_stats, fighter_stats, test
def main():

    # scrapes all urls from ufcstats.com
    get_urls.get_event_urls()
    get_urls.get_fight_urls()
    get_urls.get_fighter_urls()

    fight_data.scrape_all_fights()
    fighter_data.scrape_all_fighters()
    fight_stats.scrape_fightstats()
    fighter_stats.scrape_fighterstats()

if __name__ == '__main__':
    main()