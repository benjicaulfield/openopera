import requests
from airscraper import AirScraper

def import_mpv():
    mpv_url = 'https://airtable.com/shroOenW19l1m3w0H/tblxearKzw8W7ViN8'
    mpv_client = AirScraper(mpv_url)
    data = mpv_client.get_table()
    with open('datasets_to_be_cleaned/dirty_mpv.csv', 'w') as f:
        f.write(data)

def import_wapo():
    wapo_url = 'https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv'
    table = requests.get(wapo_url).text
    with open('datasets_to_be_cleaned/dirty_wapo.csv', 'w') as f:
        f.write(table)

if __name__ == '__main__':
    import_mpv()
    import_wapo()






