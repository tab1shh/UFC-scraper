import get_urls, fights, fighters, fight_stats, fighter_stats
def main():

    # scrapes all urls from ufcstats.com
    # get_urls.get_event_urls()
    # get_urls.get_fight_urls()
    # get_urls.get_fighter_urls()

    fights.scrape_all_fights()
    fighters.scrape_all_fighters()
    fight_stats.scrape_fightstats()
    fighter_stats.scrape_fighterstats()

if __name__ == '__main__':
    main()