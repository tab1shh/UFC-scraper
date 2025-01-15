import pandas as pd 
import glob
import os
import numpy as np

file_path = "scraper/scraped_files/"
fighter_data_file = file_path + "fighter_data.csv"
fighter_stats_file = file_path + "fighter_stats.csv"

fighter_data = pd.read_csv(fighter_data_file, encoding='latin-1')
fighter_stats = pd.read_csv(fighter_stats_file, encoding='latin-1')

# merge the two dataframes on the 'fighter_url' column because its common between the two
merged_data = pd.merge(fighter_data, fighter_stats, on='fighter_url', how='inner')

# desired columns
combined_data = merged_data[[
    'fighter_name', 'height_cm', 'weight_pounds', 'reach_cm', 'stance', 
    'date_of_birth', 'f_wins', 'f_losses', 'f_draws', 'f_dc_nc', 
    'career_SLpM', 'career_StrAcc', 'career_SApM', 'career_StrDef', 
    'career_TD_Acc', 'career_TD_Def', 'career_Sub_Avg'
]]

# fill missing values in f_wins etc with 0 so calculations are proper
combined_data[['f_wins', 'f_losses', 'f_draws', 'f_dc_nc']] = combined_data[['f_wins', 'f_losses', 'f_draws', 'f_dc_nc']].fillna(0)

total_fights = combined_data['f_wins'] + combined_data['f_losses'] + combined_data['f_draws'] + combined_data['f_dc_nc']

# calculate the win rate, loss rate, draw rate, and dc_nc rate
# some fighter have 0 total fights, need to handle that to not divide by 0
combined_data['win_rate'] = np.where(total_fights > 0, combined_data['f_wins'] / total_fights, 0)
combined_data['loss_rate'] = np.where(total_fights > 0, combined_data['f_losses'] / total_fights, 0)
combined_data['draw_rate'] = np.where(total_fights > 0, combined_data['f_draws'] / total_fights, 0)
combined_data['dc_nc_rate'] = np.where(total_fights > 0, combined_data['f_dc_nc'] / total_fights, 0)

combined_data['win_rate'] = combined_data['win_rate'] * 100
combined_data['loss_rate'] = combined_data['loss_rate'] * 100
combined_data['draw_rate'] = combined_data['draw_rate'] * 100
combined_data['dc_nc_rate'] = combined_data['dc_nc_rate'] * 100

combined_data['win_rate'] = combined_data['win_rate'].round(0).astype(int).astype(str) + '%'
combined_data['loss_rate'] = combined_data['loss_rate'].round(0).astype(int).astype(str) + '%'
combined_data['draw_rate'] = combined_data['draw_rate'].round(0).astype(int).astype(str) + '%'
combined_data['dc_nc_rate'] = combined_data['dc_nc_rate'].round(0).astype(int).astype(str) + '%'

col_order = [
    'fighter_name', 'height_cm', 'weight_pounds', 'reach_cm', 'stance', 
    'date_of_birth', 'f_wins', 'win_rate', 'f_losses', 'loss_rate', 'f_draws', 'draw_rate', 'f_dc_nc', 'dc_nc_rate', 
    'career_SLpM', 'career_StrAcc', 'career_SApM', 'career_StrDef', 
    'career_TD_Acc', 'career_TD_Def', 'career_Sub_Avg'
]

combined_data = combined_data[col_order]

combined_data.to_csv('scraper/combined_fighter_data.csv', index=False, na_rep='NA')

print("Files successfully merged and saved.")
