import time

from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd

from modules.scraper import Scraper
from modules.storage import Storage


url = 'https://www.ivoox.com/audios_sa_f_1.html'
scraper = Scraper(url)

scraper.print_url()
categories = scraper.get_categories()



def scrap():
    with ProcessPoolExecutor(max_workers=8) as executor:
        category_subcategories = []
        futures = [ executor.submit(scraper.get_subcategories, category) for category in categories ]
        for completed_futures in as_completed(futures):
            category_subcategories.extend(completed_futures.result())
    return category_subcategories

#for category in categories:
#    category_subcategories = scraper.get_subcategories(category)
#    subcategories.append(category_subcategories)

subcategories = scrap()

df = pd.DataFrame(subcategories)
Storage.save_csv('storage/subcategories.csv', df)