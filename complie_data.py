
import unittest
import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


#Uses both databases to calculate the percent of github users with reddit accounts
def calculate_reddit_github_ratio(cur,conn):
    cur.execute("SELECT * FROM Reddit_info")
    Users_list = cur.fetchall()
    cur.execute("SELECT * FROM Reddit_info")
    reddit_list = cur.fetchall()
    return len(Users_list)/len(reddit_list)

#Uses the github databased to calculate which location is the most prevalent on github
def calculate_location_ratio(cur,conn):
    cur.execute("SELECT user_location FROM Reddit_info")
    Users_list = cur.fetchall()
    total = len(Users_list)
    loc_dict ={}
    for location in Users_list:
        loc_dict[location]=0
    for location in Users_list:
        loc_dict[location]=loc_dict[location]+1
    return loc_dict


#Uses the reddit database and the github database to get the location
#of the users and calculate which location hs the highest karma on average
def calculate_location_reddit_karma_ratio(cur,conn):
    cur.execute('SELECT location, link_karma FROM Users JOIN Reddit_info ON Users.id = Reddit_info.id')
    counts = calculate_location_ratio()
    Users_list = cur.fetchall()
    fin_dict={}
    #init the dict
    for data in Users_list:
        fin_dict[data[0]]=0
    #get the data
    for data in Users_list:
        fin_dict[data[0]]=fin_dict[data[0]]+int(data[1])
    #average out the data
    for item,val in fin_dict.items():
        fin_dict[item]=fin_dict[item]/counts[item]
    return fin_dict

#Uses the reddit database to calculate on average how much reddit karma does a reddit post provide
#def calculate_reddit_post_karma_ratio():
    #cur, conn = open_database('github_users.db')
    #cur.execute("SELECT link_karma, Post_number FROM Reddit_info")
    Users_list = cur.fetchall()
    #c.execute('SELECT  FROM Users JOIN Reddit_info ON Users.id = Reddit_info.id')





def main():
    cur, conn = open_database('Github_users.db')
    calculate_location_ratio(cur,conn)
    calculate_location_reddit_karma_ratio(cur,conn)
    calculate_reddit_github_ratio(cur,conn)