"""
BeautifulSoup -> is used to get data from a web
requests -> is used to send a request and receive a response to and from a web page
pandas -> is used to to manipulate data 
matplotlib -> is used for data visualization
re -> a library used to compile regulat expressions in python
"""
import pandas as pd 
import numpy as np
import requests 
import re
from bs4 import BeautifulSoup


#This is used to style the displaying plot 
# %matplotlib inline 

# Getting html page using requests
url = "https://www.hubertiming.com/results/2017GPTR10K"
headerz = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
page = requests.get(url, headers=headerz)

# Getting html document using bs4 and lxml html parser
soup = BeautifulSoup(page.content, 'lxml')

# Extracting Data from the soup object
data_list = []
data_rows = soup.find_all("tr")
for data in data_rows:
    data_items = data.find_all("td")
    #Convert data items into a string
    string_data = str(data_items)
    cleaner = re.compile("<.*?>")
    clean_data_items = (re.sub(cleaner,"",string_data))
    data_list.append(clean_data_items)

# Extracting Headers from the sopu object
head_list = []
head_rows = soup.find_all("tr", class_="header")
for head in head_rows:
    heads = head.find_all("th")
    string_heads = str(heads)
    cleaner = re.compile("<.*?>")
    clean_heads = (re.sub(cleaner,"",string_heads))
    head_list.append(clean_heads)

# Converting head_list and data_list into respective dataframes
data_df = pd.DataFrame(data_list)
head_df = pd.DataFrame(head_list)

# Splitting and expanding dataframes for better table views

# Data
new_data_df = data_df[0].str.split(",",expand=True)
new_data_df[0] = new_data_df[0].str.strip("[")
new_data_df[0] = new_data_df[0].str.strip("]")
new_data_df[1] = new_data_df[1].str.strip("]")
new_data_df[13] = new_data_df[13].str.strip("]")

# Heads
new_head_df = head_df[0].str.split(",",expand=True)
new_head_df[0] = new_head_df[0].str.strip("[")
new_head_df[13] = new_head_df[13].str.strip("]")

# Concatinating dataframes into one
frames = [new_head_df,new_data_df]
initial_dataframe = pd.concat(frames)

# Assigning first row to be a table header
initial_dataframe = initial_dataframe.rename(columns=initial_dataframe.iloc[0])
initial_dataframe =initial_dataframe.drop(initial_dataframe.index[0])

# Dropping rows with missing data
initial_dataframe = initial_dataframe.dropna(axis=0, how='any')

# DATA ANALYSIS AND VISUALIZATION
# Qn 1. What was the average finish time in minutes for the runners?
# Procedures
# 1) first convert the time chip column into a list
chip_time_list = initial_dataframe[' Chip Time'].tolist()

# 2) Converting chip time into a minutes
time_min = []
for tim in chip_time_list:
    m = tim.split(":")
    if len(m) == 3:
        mins = (int(m[0]) * 3600 + int(m[1]) * 60 + int(m[2]))/60
        time_min.append(mins)

    else:
        mins = (int(m[0]) * 60 + int(m[1]))/60
        time_min.append(mins)

# 3) Adding the minutes into a data frame
initial_dataframe['Runner_mins'] = time_min

# 4) Calculating statistics for numeric columns using numpy library
initial_dataframe.describe(include=[np.number])
