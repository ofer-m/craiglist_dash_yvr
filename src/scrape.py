import pandas as pd
import time
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import time
import numpy as np
from datetime import datetime
from shapely.geometry import Point, Polygon
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')

from CraiglistScraper  import CraiglistScraper
from DataClean import DataClean
from AddNeighbor import AddNeighbor
from AddRemainList import AddRemainList 

if __name__ == '__main__':

    print("Scraping listings...")
    start = time.time()
    scraper = CraiglistScraper("https://vancouver.craigslist.org/search/apa?s=")
    data = scraper.get_craiglist_data()
    end = time.time()
    print("Scraping listings took %0.2f mins" %((end-start)/60))

    print("Cleaning data...")
    start = time.time()
    dc = DataClean(data)
    data_clean = dc.get_clean_data()
    end = time.time()
    print("Cleaning data took %0.2f mins" %((end-start)/60))

    print("Adding neighborhoods...")
    start = time.time()
    nb = AddNeighbor(data_clean)
    d = nb.get_data()
    end = time.time()
    print("Adding neighborhoods took %0.2f mins" %((end-start)/60))

    print("Adding remaining listings...")
    start = time.time()
    rm = AddRemainList(d)
    today_data = rm.add_remaining_listings()
    end = time.time()
    print("Adding remaining listings took %0.2f mins" %((end-start)/60))

    print("Writing data to csv...")
    today_data.to_csv('../data/craiglist_data.csv', mode='a', header=False, index = False)


    