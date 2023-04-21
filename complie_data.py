
import unittest
import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt
import random



#url = 'https://api.github.com/users'
#params = {"per_page": 5, "since": 140}
#response = requests.get(url, params=params)
#users = response.json()
#link = response.links
#print(link)
#print(users)
#print(len(users))

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


#Uses both databases to calculate the percent of github users with reddit accounts
def calculate_reddit_github_ratio(cur,conn):
    cur.execute("SELECT * FROM Users")
    Users_list = cur.fetchall()
    print("---")
    print(len(Users_list))
    print("---")
    cur.execute("SELECT * FROM Reddit_info")

    reddit_list = cur.fetchall()
    labels = ['Github Users with Reddit', 'Github Users without Reddit']
    sizes = [len(reddit_list)/len(Users_list), 1-len(reddit_list)/len(Users_list)]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

    ax1.set_title('Reddit Vs No Reddit')

    plt.show()
    return len(reddit_list)/len(Users_list)

#Uses the github databased to calculate which location is the most prevalent on github
def calculate_location_ratio(cur,conn):
    cur.execute("SELECT location FROM Users")
    Users_list = cur.fetchall()
    total = len(Users_list)
    loc_dict ={}
    for location in Users_list:
        loc_dict[location[0]]=0
    for location in Users_list:
        loc_dict[location[0]]=loc_dict[location[0]]+1
    loc_dict = dict(sorted(loc_dict.items(), key=lambda x: x[1]))
    categories = list(loc_dict.keys())
    values = list(loc_dict.values())

    newvals=[]
    for i in range(len(values)):
        newvals.append(str(values[i]))

    print(newvals)
    print(categories)
    newcat =[]
    for cate in categories:
        if cate == None:
            newcat.append("None")
        else:
            newcat.append(cate)
    print(newcat)
    colors = rainbow_colors(len(newvals))
    plt.barh(newcat, newvals, color=colors)
    plt.title('Caluclates Which location is most prevelate on github')
    plt.xlabel('Value')
    plt.ylabel('Category')
    plt.show()
    return loc_dict

def rainbow_colors(length):
    fin_colors = []
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:pink',
     'tab:brown', 'tab:gray', 'tab:olive', 'tab:cyan', 'xkcd:sky blue', 'xkcd:grass green', 'xkcd:rosy pink',
     'xkcd:purple', 'xkcd:light blue', 'xkcd:dark red', 'xkcd:teal', 'xkcd:mustard', 'xkcd:yellow', 'xkcd:lime green',
     'xkcd:orange', 'xkcd:pink', 'xkcd:brown', 'xkcd:gray', 'xkcd:olive', 'xkcd:cyan', 'xkcd:lavender',
     'xkcd:mint green', 'xkcd:beige', 'xkcd:maroon', 'xkcd:magenta', 'xkcd:tan', 'xkcd:navy', 'xkcd:periwinkle',
     'xkcd:salmon', 'xkcd:khaki', 'xkcd:plum', 'xkcd:gold', 'xkcd:apricot', 'xkcd:forest green', 'xkcd:slate blue',
     'xkcd:hot pink', 'xkcd:puce', 'xkcd:sage green', 'xkcd:brick red', 'xkcd:eggplant', 'xkcd:peach', 'xkcd:cerulean',
     'xkcd:chocolate', 'xkcd:wine', 'xkcd:powder blue', 'xkcd:coral', 'xkcd:navy blue']
    for i in range(length):
        random_index = random.randint(0, len(colors)-1)
        fin_colors.append(colors[random_index])
    return fin_colors

#Uses the reddit database and the github database to get the location
#of the users and calculate which location hs the highest karma on average
def calculate_location_reddit_karma_ratio(cur,conn):
    cur.execute('SELECT location, link_karma FROM Users JOIN Reddit_info ON Users.id = Reddit_info.id')
    Users_list = cur.fetchall()
    counts = calculate_location_ratio(cur,conn)
    fin_dict={}
    #init the dict
    for data in Users_list:
        fin_dict[data[0]]=0
    #get the data
    for data in Users_list:
        fin_dict[data[0]]=fin_dict[data[0]]+int(data[1])
    #average out the data
    for item,val in fin_dict.items():
        fin_dict[item]=round(fin_dict[item]/counts[item])
    fin_dict = dict(sorted(fin_dict.items(), key=lambda x: x[1]))
    categories = list(fin_dict.keys())
    values = list(fin_dict.values())
    newvals = []
    for i in range(len(values)):
        newvals.append(str(values[i]))

    print(newvals)
    print(categories)
    newcat = []
    for cate in categories:
        if cate == None:
            newcat.append("None")
        else:
            newcat.append(cate)
    print(newcat)
    colors = rainbow_colors(len(newvals))
    print(colors)
    plt.barh(newcat, newvals, color=colors)
    plt.title('Calculates Which location get the most karma on average')
    plt.xlabel('Value')
    plt.ylabel('Category')
    plt.show()

    return fin_dict

def run_and_write_to_file():
    cur, conn = open_database('Github_users.db')
    cur.execute("SELECT * FROM Users")
    Users_list = cur.fetchall()

    with open('Data_interpretation.txt', 'w') as file:
        file.write("First we want to calculate each out of"
                   " how many github accounts we find, what percentage of them possess reddit accounts")
        file.write('\n')
        file.write(f"From the data we can assess that out of {len(Users_list)} github user accounts {calculate_reddit_github_ratio(cur, conn)} percent of them have reddit accounts")
        file.write('\n')
        file.write(f"Next we want to calculate the spread of locations of the github users, to see which area is most popular")
        file.write('\n')
        dicct = calculate_location_ratio(cur,conn)
        fin_name = None
        fin_val = None
        for key, value in dicct.items():
            file.write("("+str(key)+"),")
            fin_name = str(key)
        file.write('\n')
        for key, value in dicct.items():
            file.write("("+str(value)+"),")
            fin_val = str(value)
        file.write('\n')
        file.write(f'As we can see, the location with the greatest concentration of users for this dataset is {fin_name} with {fin_val} occurances our datasize')
        file.write('\n')
        file.write('Finally, we are going to calculate which location, on average recieves the most karma per user')
        file.write('\n')
        file.write(f'The following are the results:')
        dicct2 = calculate_location_reddit_karma_ratio(cur, conn)
        for key, value in dicct2.items():
            file.write("("+str(key)+"),")
            fin_name = str(key)
        file.write('\n')
        for key, value in dicct2.items():
            file.write("("+str(value)+"),")
            fin_val = str(value)

        file.write(
            f'On average per user for this dataset is the region highest amount of karma per user is {fin_name} with {fin_val} karma per user')


def main():
    cur, conn = open_database('Github_users.db')
    run_and_write_to_file()

if __name__ == "__main__":
    main()
