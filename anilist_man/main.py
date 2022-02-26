import json
import os
import sys
import re

from typing import Optional

import typer
import requests

from anilist_man.queries import queryUser, queryManga, queryMangaCollection, querySoonMMangaCollection
from anilist_man.queries import queryUpdateManga

from anilist_man.query_func import QueryFunctions

app = typer.Typer()
#Print all files in data folder
try:
    with open("anilist_man/token.txt", "r") as f:
        token = f.read()
except FileNotFoundError:
    print(f"Visit https://anilist.co/api/v2/oauth/authorize?client_id=7501&response_type=token")
    token = str(input("\n[+] Enter your token: "))
    with open("anilist_man/token.txt", "w") as f:
        f.write(token)

base_url = "https://graphql.anilist.co"
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

try:
    with open("anilist_man/id.txt", "r") as f:
        uid = f.read()
except FileNotFoundError:
    print("[!] No user id found")
    c1 = str(input("\n[+] Enter your User Name: "))
    query = queryUser
    resp = QueryFunctions.getUser(query, headers, c1)
    username = resp["data"]["User"]["name"]
    uid = resp["data"]["User"]["id"]
    print(f"[+] User ID: {uid} | User Name: {username}")
    conf = str(input("\n[+] Do you want to save this user id? [y/n]: "))
    if conf == "y":
        with open("anilist_man/id.txt", "w") as f:
            f.write(str(uid))
    else:
        print("[!] User id not saved")
        sys.exit()

uid = int(uid)
print(f"[+] User ID: {uid}")
class RefreshFunc():
    def __init__(self):
        pass

    def refreshToken():
        print(f"Visit https://anilist.co/api/v2/oauth/authorize?client_id=7501&response_type=token")
        token = str(input("\n[+] Enter your token: "))
        # Delete token.txt if it exists
        try:
            os.remove("anilist_man/token.txt")
        except FileNotFoundError:
            pass
        with open("anilist_man/token.txt", "w") as f:
            f.write(token)

    def refreshUid():
        uid = str(input("\n[+] Enter your user id: "))
        # Delete token.txt if it exists
        try:
            os.remove("anilist_man/id.txt")
        except FileNotFoundError:
            pass
        with open("anilist_man/id.txt", "w") as f:
            f.write(uid)

@app.command()
def user(user_name: Optional[str] = typer.Option(None, "--user", "-u", help="Tell Info About User")):
    if user_name == None:
        user_name = str(input("[+] Enter user name: "))
    query = queryUser
    resp = QueryFunctions.getUser(query, headers, user_name)
    username = resp["data"]["User"]["name"]
    uid = resp["data"]["User"]["id"]
    print(f"[+] User ID: {uid} | User Name: {username}")

if __name__ == "__main__":
    app()