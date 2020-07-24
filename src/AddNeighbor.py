import pandas as pd
import numpy as np
from shapely.geometry import Point, Polygon
import geopandas as gpd

class AddNeighbor:
    
    def __init__(self, data):
        self.data = data
        self.sp = gpd.read_file("../data/yvr_area/bounds.shp")        
        self.sp.index = self.sp.name
    
    def convert_point(self, long, lat):
        return Point(long, lat)
    
    def find_neighb(self, point):
        neighb = self.sp.name.unique()
        name = None

        for n in neighb:
            if point.within(self.sp.at[n,"geometry"]):
                name = n
                return name
        return name
    
    def add_neighb(self):
        self.data["Point"] = np.vectorize(lambda x,y: self.convert_point(x,y), otypes=[Point])(self.data["Longitude"], self.data["Latitude"])
        self.data["Neighborhood"] = np.vectorize(lambda x:self.find_neighb(x))(self.data["Point"])
        self.data = self.data.query("Neighborhood!='None'")
    
    def get_data(self):
        self.add_neighb()
        return self.data