import pandas as pd
import time
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import re
import time
import numpy as np
from datetime import datetime

class DataClean:
    
    def __init__(self, data):
        self.data = data
    
    def clean_data(self):
        self.data = self.data.dropna(subset=["Price", "Latitude", "Longitude", "Property_Type", "Bedrooms", "Bathrooms"])
        self.data["Price"] = np.vectorize(lambda x: int(x[1:]))(self.data["Price"])
        self.data["City"] = self.data.City.apply(lambda x: x.title())
        self.data["Property_Type"] = self.data.Property_Type.apply(lambda x: x.title())
        self.data["Size"] = self.data.Size.astype(float)
        self.data["Description"] = np.vectorize(lambda x: re.sub("\n\nQR Code Link to This Post\n\n\n|\n", "", x))(self.data["Description"])
        self.data["Posting_ID"] = np.vectorize(lambda x: re.sub("post id: ", "", x))(self.data["Posting_ID"])
        self.data["Posting_ID"] = self.data.Posting_ID.astype(int)
        self.data["Bedrooms"] = np.vectorize(lambda x: int(re.sub("BR", "", x)))(self.data["Bedrooms"])
        self.data["Bathrooms"] = np.vectorize(lambda x: re.sub("Ba", "", x))(self.data["Bathrooms"])
        self.data["Date_Posted"] = np.vectorize(lambda x: re.sub("posted: ", "", x))(self.data["Date_Posted"])
        self.data["Date_Posted"] = pd.to_datetime(self.data["Date_Posted"])
        self.data["Date_Updated"] = self.data.Date_Updated.apply(lambda x:self.updated_date(x))
        self.data["Date_Available"] = pd.to_datetime(self.data.Date_Available)
        self.data["Latitude"]= self.data.Latitude.astype(float)
        self.data["Longitude"]= self.data.Longitude.astype(float)
        self.data["Date"] = datetime.today().strftime('%Y-%m-%d')
        
        self.data = self.data.drop_duplicates(["URL"])
        self.data = self.data.query("Price >=100 & Price <= 50000")

    def updated_date(self, date):
        if pd.isnull(date):
            return date
        else:
            date = re.sub("updated: ", "", date)
            return pd.to_datetime(date)
    
    def get_clean_data(self):
        self.clean_data()
        return self.data