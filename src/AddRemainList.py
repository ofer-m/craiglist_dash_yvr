import pandas as pd
import time
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import time
import numpy as np
from datetime import datetime

class AddRemainList:
    
    def __init__(self, today):
        self.data = pd.read_csv("../data/craiglist_data.csv")
        yesterday_date = self.data.Date.unique()[-1]
        self.yesterday = self.data.query("Date==@yesterday_date")
        self.today = today
        self.URLs = None
        self.On_Map = []
    
    def check_on_map(self):
        
        for url in self.yesterday.URL:
            if url in self.today.URL.values:
                self.On_Map.append(None)
                
            else:
                link = requests.get(url)
                link = BeautifulSoup(link.text)

                city = link.find("meta", attrs={"name":"geo.placename"})

                if city == None:
                    self.On_Map.append(False)
                else:
                    self.On_Map.append(True)

    def get_remaining_listings(self):
        self.yesterday["On_Map"] = self.On_Map
        self.yesterday["Date"] = datetime.today().strftime('%Y-%m-%d')
        
        return self.yesterday.query("On_Map==True")
    
    def add_remaining_listings(self):
        
        print("Length of Yesterday URL:", str(len(self.yesterday.URL)))
        
        self.check_on_map()

        print("Length of OnMap:", str(len(self.On_Map)))

        rem = self.get_remaining_listings()
        
        rem = rem.drop(columns=["On_Map"])
        
        
        return pd.concat((self.today, rem), axis = 0)
    
    
    