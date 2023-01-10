import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import streamlit as st

url ='covid_data.csv'
# url='covid_data.csv'
df = pd.read_csv(url)
df['obsDate'] = pd.to_datetime(df['obsDate'])
df['active'] = pd.to_numeric(df['active'])
df['recovered'] = pd.to_numeric(df['recovered'])
df['deaths'] = pd.to_numeric(df['deaths'])

newcases, newdeaths, newrec = [], [], []
for i in range(len(df)-1):
    numcases = (df.iloc[i+1]['active'] - df.iloc[i]['active']) + (df.iloc[i+1]['recovered'] - df.iloc[i]['recovered']) + (df.iloc[i+1]['deaths'] - df.iloc[i]['deaths'])
    newcases.append(numcases)
    numdeaths = df.iloc[i+1]['deaths'] - df.iloc[i]['deaths']
    newdeaths.append(numdeaths)
    numrec = df.iloc[i+1]['recovered'] - df.iloc[i]['recovered']
    newrec.append(numrec)
    
# Plot
fig, ax = plt.subplots(2,1, figsize=(12,10), sharex=True)

ax[0].plot(df['obsDate'][1:],newcases, label='New Cases', color='r')
ax[0].plot(df['obsDate'][1:],newrec, label='New Recoveries', color='g')
ax[0].plot(df['obsDate'][1:],newdeaths, label='New Deathss', color='k')
ax[0].legend()
ax[0].grid()
ax[0].set_title('New Cases/Recoveries/Deaths')
ax[0].set_ylim(bottom=0)

ax[1].plot(df['obsDate'],df['active'], label='New Recoveries', color='r')
ax[1].grid()
ax[1].set_title('Active Cases')
ax[1].set_ylabel('Count')
ax[1].set_xlabel('Date')
ax[1].set_ylim(bottom=0)

locator = mdates.AutoDateLocator(minticks=3, maxticks=12)
formatter = mdates.ConciseDateFormatter(locator)
formatter.formats = ['%y',  # ticks are mostly years
                     '%b',       # ticks are mostly months
                     '%d',       # ticks are mostly days
                     '%H:%M',    # hrs
                     '%H:%M',    # min
                     '%S.%f', ]  # secs
# these are mostly just the level above...
formatter.zero_formats = [''] + formatter.formats[:-1]
# ...except for ticks that are mostly hours, then it is nice to have
# month-day:
formatter.zero_formats[3] = '%d-%b'

formatter.offset_formats = ['',
                            '%Y',
                            '%b %Y',
                            '%d %b %Y',
                            '%d %b %Y',
                            '%d %b %Y %H:%M', ]

ax[1].xaxis.set_major_locator(locator)
ax[1].xaxis.set_major_formatter(formatter)
fig.tight_layout()

st.pyplot(fig)
