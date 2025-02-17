# UFC Web Scraper
A Python-based web scraping application that collects UFC fighter statistics from the official UFC website, processes relevant data, and prepares it for analysis and prediction modeling.

## Features
- Web Scraping: Extracts fighter details, rankings, and career statistics.
- Data Cleaning & Filtering: Processes raw data, removes duplicates, and retains ranked fighters.
- CSV Export: Saves filtered data for further analysis or use in machine learning models.

## Getting Started
1. Clone the Repository
```bash
git clone https://github.com/yourusername/UFC-scraper.git
cd scraper
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Run the scraper
```bash
python main.py
```

## How It Works
The scraper navigates the UFC website to extract event, fight, and fighter details. It systematically:
- Collects Links – Retrieves URLs for all UFC events, individual fights, and fighter profiles.
- Extracts Data – Gathers key statistics for each fighter, fight, and event, ensuring comprehensive coverage.
- Saves Structured Data – Stores the extracted information in the scraped_files folder for easy access.
- Filters Ranked Fighters – Identifies and processes ranked fighters, integrating their data for advanced - analysis.
- Prepares for Machine Learning – Combines relevant files, creating clean datasets optimized for predictive modeling.

## Improvements
- Active Fighters Not Included – The scraper does not currently differentiate between active and inactive fighters, meaning some fighters who are still competing may be missing from the dataset.
- No File Updates on Rescraping – When rescraping after new fights, the script does not update existing files, which can lead to outdated or duplicated data instead of a continuously updated dataset.
### Planned Enhancements
- Include Active Fighters – Implement logic to detect and prioritize active fighters in the dataset.
- Efficient Data Updating – Modify the scraper to check for new fights and update existing records instead of overwriting or duplicating files.