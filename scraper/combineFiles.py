import pandas as pd


fight_data = pd.read_csv('scraper/scraped_files/fight_data.csv', encoding='latin-1')
fight_stats = pd.read_csv('scraper/scraped_files/fight_stats.csv', encoding='latin-1')
fighter_data = pd.read_csv('scraper/scraped_files/fighter_data.csv', encoding='latin-1')
fighter_stats = pd.read_csv('scraper/scraped_files/fighter_stats.csv', encoding='latin-1')


# combine fighter
fighter_combined = pd.merge(fighter_data, fighter_stats, on='fighter_url', how='left')

# add fighter stats to the fight data
fighter_1_stats = fighter_combined.rename(columns={col: f'fighter1_{col}' for col in fighter_combined.columns})
fighter_2_stats = fighter_combined.rename(columns={col: f'fighter2_{col}' for col in fighter_combined.columns})

# merge into fight data
fight_combined = pd.merge(fight_data, fight_stats, on=['fight_url', 'event'], how='left')
fight_combined = fight_combined.merge(fighter_1_stats, left_on='fighter1', right_on='fighter1_fighter_name', how='left')
fight_combined = fight_combined.merge(fighter_2_stats, left_on='fighter2', right_on='fighter2_fighter_name', how='left')

fight_combined.to_csv('ai_fight_predictor_data.csv', index=False)


