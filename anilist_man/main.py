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

try:
    with open("token.txt", "r") as f:
        token = f.read()
except FileNotFoundError:
    print(f"Visit https://anilist.co/api/v2/oauth/authorize?client_id=7501&response_type=token")
    token = str(input("\n[+] Enter your token: "))
    with open("token.txt", "w") as f:
        f.write(token)

base_url = "https://graphql.anilist.co"
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

try:
    with open("id.txt", "r") as f:
        uid = f.read()
except FileNotFoundError:
    print("[!] No user id found")
    c1 = str(input("\n[+] Enter your User Name: "))
    query = queryUser
    resp = QueryFunctions.getUser(query, headers, c1)
    try:
        username = resp["data"]["User"]["name"]
        uid = resp["data"]["User"]["id"]
        print(f"[+] User ID: {uid} | User Name: {username}")
        conf = str(input("\n[+] Do you want to save this user id? [y/n]: "))
        if conf == "y":
            with open("id.txt", "w") as f:
                f.write(str(uid))
        else:
            print("[!] User id not saved")
            sys.exit()
    except KeyError:
        print(f"[!] User {c1} not found")
        sys.exit()

uid = int(uid)

class RefreshFunc():
    def __init__(self):
        pass

    def refreshToken():
        print(f"Visit https://anilist.co/api/v2/oauth/authorize?client_id=7501&response_type=token")
        token = str(input("\n[+] Enter your token: "))
        # Delete token.txt if it exists
        try:
            os.remove("token.txt")
        except FileNotFoundError:
            pass
        with open("token.txt", "w") as f:
            f.write(token)

    def refreshUid():
        uid = str(input("\n[+] Enter your user id: "))
        # Delete token.txt if it exists
        try:
            os.remove("id.txt")
        except FileNotFoundError:
            pass
        with open("id.txt", "w") as f:
            f.write(uid)

@app.command()
def user(user_name: Optional[str] = typer.Option(None, "--user", "-u", help="Tell Info About User")):
    if user_name == None:
        user_name = str(input("[+] Enter user name: "))
    query = queryUser
    resp = QueryFunctions.getUser(query, headers, user_name)
    try:
        username = resp["data"]["User"]["name"]
        uid = resp["data"]["User"]["id"]
        print(f"[+] User ID: {uid} | User Name: {username}")
    except KeyError:
        print(f"[!] User {user_name} not found")

@app.command()
def c_refresh_token():
    RefreshFunc.refreshToken()
    sys.exit()

@app.command()
def c_refresh_uid():
    RefreshFunc.refreshUid()
    sys.exit()

@app.command()
def manga(id : Optional[int] = typer.Option(None, "--manga", "-m", help="Get info about manga via its ID")):
    if id == None:
        id = int(input("[+] Enter Manga ID: "))
    query = queryManga
    resp = QueryFunctions.getManga(query, headers, id)
    try:
        title = resp["data"]["Media"]["title"]["romaji"]
        print(f"[+] Manga ID: {id} | Manga Title: {title}")
    except KeyError:
        print(f"[!] Manga ID {id} not found")

@app.command()
def manga_collection(user_id: Optional[int] = typer.Option(None, "--mangacurrent", "-mc", help="Get your `current` manga collection")):
    if user_id == None:
        user_id = int(uid)
    query = queryMangaCollection
    resp = QueryFunctions.getMangaStats(query, headers, user_id)
    try:
        mangaList = resp["data"]["MediaListCollection"]["lists"][0]["entries"]
        print(f"Total Current Manga: {len(mangaList)}")

        for m in mangaList:
            index = len(mangaList) - mangaList.index(m)
            if index < 10:
                index = "0" + str(index)
            else:
                index = str(index)
            list_id = m["id"]
            romanji = m["media"]["title"]["romaji"]
            english = m["media"]["title"]["english"]
            progress = m['progress']
            if english is None:
                print(f"{index}. {romanji} | Progress: {progress} | List ID: {list_id}")
            else:
                print(f"{index}. {romanji} ({english}) | Progress: {progress} | List ID: {list_id}")

        print("\n")
    except:
        print("[!] Something went wrong")

if __name__ == "__main__":
    app()