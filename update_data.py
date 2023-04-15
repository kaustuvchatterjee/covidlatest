#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 12:50:53 2022

@author: kaustuv
"""

import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import etree
import requests

# read csv file
df = pd.read_csv('covid_data.csv')
df['obsDate'] = pd.to_datetime(df['obsDate'])

# scrape MOHFW site
py_url = "https://www.mohfw.gov.in/"
py_headers = ({'User-Agent':
'Safari/537.36',\
'Accept-Language': 'en-US, en;q=0.5'})
py_wpage = requests.get (py_url, headers=py_headers)
py_soup = BeautifulSoup (py_wpage.content, "html.parser")
dom = etree.HTML (str(py_soup))

# Date
xpath = '//*[@id="site-dashboard"]/div/div/div[1]/div[1]/h5/span/text()[1]'
# dom.xpath ('//*[@id="firstHeading"]')[0].text
dt = dom.xpath(xpath)[0].strip()
dt = dt.split(' ')
dt = dt[3]+'-'+dt[4]+'-'+dt[5]+' '+dt[6]
dt = datetime.strptime(dt,'%d-%B-%Y, %H:%M')
print(dt)

#Active Cases
xpath = '//*[@id="site-dashboard"]/div/div/div[1]/div[2]/ul/li[1]/strong[2]/text()'
active = dom.xpath(xpath)[0].strip()
print(active)

# Discharged
xpath = '//*[@id="site-dashboard"]/div/div/div[1]/div[2]/ul/li[2]/strong[2]/text()'
recovered = dom.xpath(xpath)[0].strip()
print(recovered)

# Deaths
xpath = '//*[@id="site-dashboard"]/div/div/div[1]/div[2]/ul/li[3]/strong[2]/text()'
deaths = dom.xpath(xpath)[0].strip()
print(deaths)

# df = df.append({'obsDate':dt, 'active': active, 'recovered':recovered, 'deaths':deaths}, ignore_index=True)
df1 = pd.DataFrame({'obsDate':dt, 'active': active, 'recovered':recovered, 'deaths':deaths}, index=[0])
df = pd.concat([df,df1], ignore_index=True)
df.to_csv('covid_data.csv', index=False)
