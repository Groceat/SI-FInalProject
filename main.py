import unittest
import sqlite3
import json
import os
import requests
from bs4 import BeautifulSoup
import sqlite3
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

import praw
import requests
from bs4 import BeautifulSoup
import sqlite3

import matplotlib.pyplot as plt





# This function essentiallys gets all the reddit info after using the key

def search_reddit_by_user(username):
    finlist = []
    reddit = praw.Reddit(client_id='npRg-arfVu4FaYFqctuZNQ',
                         client_secret='gxLxmBpZ7CU3dhol-3rW4HX_Gd_N6Q',
                         username='UMichDev',
                         password='Megabhyfc12',
                         user_agent='MYAPI/0.01')
    try:
        user = reddit.redditor(username)
        user_id = user.id
        link_karma = user.total_karma
        comment_karma = user.comment_karma
        created_utc = user.created_utc
        num_posts = 0
        for post in user.submissions.new():
            num_posts += 1
        finlist.append(1)
        finlist.append(link_karma)
        finlist.append(comment_karma)
        finlist.append(num_posts)
        print(link_karma)

        return finlist
    except:
        finlist.append(0)
        print(f'Error: User "{username}" not found')
    return finlist



def read_github_and_reddit_data(con, curr):
    print("we reading github")
    url = 'https://api.github.com/users'
    database_name = 'github_users.db'
    table_name = 'Users'
    table_name_reddit = "Reddit_info"

    conn = con
    c = curr
    #c.execute(f"DROP TABLE {table_name}")
    #c.execute(f"DROP TABLE {table_name_reddit}")

    c.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, Username TEXT, location TEXT, Followersnum TEXT, Followingnum TEXT, Repos TEXT)")

    c.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name_reddit} (id INTEGER PRIMARY KEY, Link_Karma TEXT, Comment_karma TEXT, Post_number TEXT)")

    params = {"per_page": 25}
    response = requests.get(url, params=params)
    users = response.json()
    limiter = 0
    for user in users:
        if limiter == 25:
            break
        print("----------")
        userdata = requests.get(url + "/" + user["login"])
        user1 = userdata.json()
        print(user1)
        # Get user data from JSON response
        user_id = user['id']
        user_login = user['login']
        user_twitter = user1['twitter_username']
        user_followers = user1["following"]
        user_following = user1["followers"]
        user_location = user1["location"]
        user_repos = user1["public_repos"]
        user_bio = user1["bio"]
        # If the reddit user exists, we add that bad boy to the database within the function, otherwise no go bro :(
        redditinfo = search_reddit_by_user(user_login)
        user_url = user['html_url']

        # Now we add the user in the database
        c.execute(f"INSERT OR IGNORE INTO {table_name} (id,Username,location,Followersnum,Followingnum, Repos) VALUES (?,?,?,?,?,?)",
                  (user_id, user_login,user_location,user_followers, user_following, user_repos))
        if redditinfo[0] == 1:
            c.execute(
                f"INSERT OR IGNORE INTO {table_name_reddit} (id, Link_Karma, Comment_karma, Post_number) VALUES (?, ?, ?, ?)",
                (user_id, redditinfo[1], redditinfo[2], redditinfo[3]))

        limiter = limiter + 1

    conn.commit()


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn


def main():

    cur, conn = open_database('github_users.db')
    read_github_and_reddit_data(conn, cur)
    cur.execute("SELECT * FROM Reddit_info")
    players_list = cur.fetchall()
    print(players_list)
    cur.execute("SELECT * FROM Users")
    players_list = cur.fetchall()
    print(players_list)
    conn.close()


if __name__ == "__main__":
    main()




