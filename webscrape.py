# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import demjson
import json 

base_url = "https://www.tsb.kz/bankomates"

html = requests.get(base_url).text
soup = BeautifulSoup(html, "html.parser")
ul = soup.find("ul", {"class":"ul_city"})
print("ul=", ul)

cities = {}
for li_a in ul.find_all("a"):
    print("href=", li_a["href"], ", text=", li_a.text)
    if li_a.text is not None and len(li_a.text) > 0:
        cities[li_a.text] = li_a["href"]
print("length=", len(cities), cities)   

cities['Астана'] = base_url

all_atms_info = []
for (city, param) in cities.items():
    print(city, param)
    html = requests.get(base_url + param).text     
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", text=re.compile("var points = new Array"))    
    if script is not None:
        # print("script=", script)
        json_text = "[" + re.search(r"\s*var points = new Array\s*\(\s*({.*?})\s*\)\s*;\s*", script.string, flags=re.MULTILINE | re.DOTALL).group(1) + "]"        
        all_atms_info.append(demjson.decode(json_text))
        # print(city_atms_info)

all_atms_info = {'atms':all_atms_info}
print("all_atms_info=", all_atms_info)
with open("all_atms_info.json", "w") as f:
    json.dump(all_atms_info, f)
