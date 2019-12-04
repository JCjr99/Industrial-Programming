
import json
import numpy as np
import matplotlib.pyplot as plt
import string
import collections
import re
import sys
import argparse
import os
import pycountry_convert as py
from tkinter import *
import pandas as pd

def toSet(l):
    s = set()
    for item in l:
        s.add(item)
    return s

class Extract:
    #jsonarr = None
    #def __init__(self, jsonarr):
    #    self.jsonarr = jsonarr

    #def changejson(self, jsonarr):
    #    self.jsonarr = jsonarr
    def display(self,arr, extra = None):
        counter = collections.Counter(arr)
        if extra == None:
            plt.figure(figsize=(200, 30))
            plt.bar(range(len(counter)), counter.values(), align = 'center')
            plt.xticks(range(len(counter)), list(counter.keys()), rotation = 'vertical')

        else:
            set = toSet(arr)
            data = []
            for item in set:
                data.append([extra[item],item,counter[item]])
            df = pd.DataFrame(data,columns = ['continent', 'country', 'No'])
            df.pivot("country", "continent", "No").plot(kind='bar')

        plt.show()


    def findCountries(self,docuuid,jsonarr):
        countries = []
        for item in jsonarr:
            try:
                if item["subject_doc_id"] == docuuid:
                    countries.append(item["visitor_country"])
            except KeyError:
			#do no
                pass

        if countries==[]:
            print("Error: please check that document UUID and file name are correct")
        return countries

    def findContinents(self, countries):
        country_continent = {}
        for country in countries:
            country_continent[country] = py.country_alpha2_to_continent_code(country)
        return country_continent

    def findBrowser(self,docuuid,jsonarr):
    	browsers = []
    	for item in jsonarr:
    		try:
    			if item["subject_doc_id"] == docuuid:
                                browsers.append(item["visitor_useragent"])
    		except KeyError:
    			pass
    	if browsers == []:
            print("Error: please check that document UUID and file name are correct")
    	return browsers

    def refinedBrowsers(self,browsers):
            refined=[]
            for string in browsers:
                    #Chrome|Safari|
                    b = re.findall("(Opera|Mozilla)", string)
                    print(b)
                    for items in b:
                            refined.append(items)
            return refined
