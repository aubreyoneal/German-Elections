# -*- coding: utf-8 -*-
"""
Created on Fri Sep 29 21:54:07 2017

@author: Gabriel and Aubrey
"""
import pandas as pd
import json 
''' #Clean json file. May take a while for large data sets
with open('fetched_tweets14.json', "r") as infile:
    with open('output14.json', "w") as outfile:
        
        outfile.write("[")
        
        line=infile.readline()
        for next_line in infile:    
            outfile.write(line.strip("\n"))
            outfile.write(",")
            outfile.write("\n")
            line=next_line
        #ensure that the last element does not have a comma    
        outfile.write(line.strip("\n"))
        outfile.write("]")
            
'''

#%%  
 
#create useable dataframe
df=pd.read_json("output14.json")
#clean data
df=df[["user","created_at","lang","text","entities"]]
    
df=df.dropna(subset=["user","entities"])

df["screen_name"]=df["user"].apply(lambda x: x.get("screen_name"))

df["location"]=df["user"].apply(lambda x: x.get("location"))

df["description"]=df["user"].apply(lambda x: x.get("description"))

df["hashtags"]=df["entities"].apply(lambda x: x.get("hashtags"))
def clean_hashtags(the_list):
    texts = [a_dict.get("text") for a_dict in the_list]
    return " ".join(texts)
df["hashtags"]=df["hashtags"].apply(clean_hashtags)

df=df.drop(["user","entities"],axis=1)


#filter and stuff I guess
de=df[df["lang"]=="de"]
#non_de=df[df["lang"]=="en"]

#network = pd.Series("user")

#network.to_csv("network_analysis.csv",index=False)


#count something
(df["lang"]=="de").sum()
df["hashtags"].str.lower().str.contains("btw")

#%% 
#get @usernames for network analysis
'''
ru=df[df["lang"]=="ru"]
ru["text"].str.contains("@")
tweet_at = ru[ru["text"].str.contains("@") == True]
tweet_at["text"].str.split()

tweet_at["text"].str.split
tweet_at["text"].str.split().str.startswith("@")
print tweet_at["text"].str.split()
tweet_at["text"].str.split()
split = tweet_at["text"].str.split()
split["text"].str.starswith("@")
split["text"].str.contains("@")
print split["text"].str.startswith("@")
print split.loc["text"].str.st
print (split["text"].str.startswith("@"))
s.loc['text'] = "@"
splot.loc['text'] = "@"

#get usernames!!!
#small_sample.str.extract("\@(\w+)")
#de["text"].str.extract("\@(\w+)")
de_network = de["text"].str.extract("\@(\w+)", expand=True)
screen_name = de["screen_name"]
de_networking = pd.concat([screen_name, de_network], axis=1, ignore_index=True)
de_networking.to_csv("de_network.csv",index=True)
#de_network.append(de["screen_name"])

''' 
#translate to English (get rid of special char)
from googletrans import Translator
translator = Translator()
location_en = pd.DataFrame(columns=['location'])
location = de['location']
for x in range(0, 15):
    translations = translator.translate([location[x]], dest='en')
    for translation in translations:
        location_en = location_en.append({'location': translation.text}, ignore_index = True)
    
    location_en["location"] = (str(translation.text))
#Google Maps Geolocator
import time
import urllib.request
import urllib.parse
import urllib.error

def GoogGeoAPI(address,api="",delay=5):
  base = r"https://maps.googleapis.com/maps/api/geocode/json?"
  addP = "address=" + address.replace(" ","+")
  GeoUrl = base + addP + "&key=" + api
  response = urllib.request.urlopen(GeoUrl)
  jsonRaw = response.read()
  jsonData = json.loads(jsonRaw)
  if jsonData['status'] == 'OK':
    resu = jsonData['results'][0]
    finList = [resu['formatted_address'],resu['geometry']['location']['lat'],resu['geometry']['location']['lng']]
  else:
    finList = [None,None,None]
  time.sleep(delay) #in seconds
  return finList

geoLocation = pd.DataFrame(columns = ["place", "long", "lat"])
#Example Use
test = r"1600 Amphitheatre Parkway, Mountain View, CA"
geoR = GoogGeoAPI(address=test)
print (geoR)

for x in range(0, 10):
    geoR.append(GoogGeoAPI(address=location_en["location"].loc[x]))
    

