import pandas as pd
import time
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import time
import numpy as np
from datetime import datetime

class CraiglistScraper:
    
    def __init__(self, site):
        self.site = site
        self.urls = []
        self.data = []
    
    def get_listings_url(self):
        i = 0
        site = self.site + str(i)
        cl_req = requests.get(site)

        while True:
            cl = BeautifulSoup(cl_req.text)
            listings = cl.find_all("p", {"class":"result-info"})
            if len(listings) == 0:
                break
            for l in listings:
                self.urls.append(l.find("a")["href"])

            i += 120
            site = self.site + str(i)
            cl_req = requests.get(site)
            time.sleep(0.2)
    
    def is_invalid_listing(self, listing):
        if listing.find("div", {"class":"removed"}) != None:
            return True
        city = listing.find("meta", attrs={"name":"geo.placename"})['content']
        
        if city.lower() != "vancouver":
            return True
        
        return False
    
    def get_listing_data(self, link, listing):
        price = np.nan
        if link.find("span", {"class":"price"}) != None:
            price = link.find("span", {"class":"price"}).text
        lat = np.nan 
        if link.find("div", {"id":"map"}) != None:
            lat = link.find("div", {"id":"map"})["data-latitude"]
        long = np.nan
        if link.find("div", {"id":"map"}) != None:
            long = link.find("div", {"id":"map"})["data-longitude"]

        bed = np.nan
        bath = np.nan
        sqft = np.nan

        date_avail = np.nan 
        date = link.find("p", {"class":"attrgroup"}).find("span", {"class":"housing_movein_now property_date shared-line-bubble"})
        if date != None:
            date_avail = date["data-date"]

        furn = False
        prop_type = np.nan

        bubble_line = link.find("p", {"class":"attrgroup"})

        if bubble_line.find("span", {"class":"shared-line-bubble"}) != None:

            line_text = bubble_line.find_all("b")

            for line in line_text:
                if "br" in line.text.lower():
                    bed= line.text
                elif "ba" in line.text.lower():
                    bath = line.text
                elif line.text.isdigit():
                    sqft = line.text        

            next_at = link.find("p", {"class":"attrgroup"}).findNext("p", {"class":"attrgroup"})

            if next_at != None:

                if next_at.find("span", {"class":"otherpostings"}) != None:
                    next_at = next_at.findNext("p", {"class":"attrgroup"})

                for at in next_at.find_all("span"):

                    if "furnished" in at.text.lower():
                        furn = True
                    elif at.text.lower() in ["apartment", "condo", "cottage/cabin", "duplex", "flat", "house", "in-law", "loft", "townhouse", "manufactured"]:
                        prop_type = at.text

        else:
            if bubble_line.find("span", {"class":"otherpostings"}) != None:
                bubble_line = bubble_line.findNext("p", {"class":"attrgroup"})

            for at in bubble_line.find_all("span"):
                if "furnished" in at.text.lower():
                    furn = True
                elif at.text.lower() in ["apartment", "condo", "cottage/cabin", "duplex", "flat", "house", "in-law", "loft", "townhouse", "manufactured"]:
                    prop_type = at.text

        desc = np.nan
        if link.find("section", {"id":"postingbody"}) != None:
            desc= link.find("section", {"id":"postingbody"}).text


        post_id = link.find("div", {"class":"postinginfos"}).find_all("p", {"class":"postinginfo"})[0].text
        date_posted = link.find("div", {"class":"postinginfos"}).find_all("p", {"class":"postinginfo"})[1].text
        date_updated = np.nan
        up = link.find("div", {"class":"postinginfos"}).find_all("p", {"class":"postinginfo"})[2].text
        if "updated" in up.lower():
            date_updated = up

        row = {"URL": listing, "City": "Vancouver", "Price": price, "Latitude": lat, "Longitude": long,
               "Bedrooms": bed, "Bathrooms": bath, "Size": sqft, "Date_Available": date_avail,
               "Furnished": furn, "Property_Type": prop_type, "Description": desc, "Posting_ID": post_id,
               "Date_Posted": date_posted, "Date_Updated": date_updated}
        return row
        
    def get_all_listings_data(self):
        for listing in self.urls:
            link = requests.get(listing)
            link = BeautifulSoup(link.text)
            if self.is_invalid_listing(link):
                continue
            else:
                listing_data = self.get_listing_data(link, listing)
                self.data.append(listing_data)
                time.sleep(0.2)
    
    def get_craiglist_data(self):
        self.get_listings_url()
        self.get_all_listings_data()
        return pd.DataFrame(self.data)