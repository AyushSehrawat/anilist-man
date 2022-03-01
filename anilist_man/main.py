import json
import os
import sys
import re

import webbrowser
from typing import Optional
from typing import List

import typer
import requests

from anilist_man.queries import queryUser, queryManga, queryMangaCollection, querySoonMMangaCollection
from anilist_man.queries import queryUpdateManga

from anilist_man.subFunc import subFunc
from anilist_man.queryFunc import QueryFunctions

app = typer.Typer()
home = os.path.expanduser('~')
location = os.path.join(home, 'Documents')
folder_check = os.path.isdir(location)

if folder_check == False:
    print(f"{location} does not exist.")
    location = str(input("Please enter the location of your documents folder: "))
    folder_check = os.path.isdir(location)
    if folder_check == False:
        print(f"{location} does not exist.")
        sys.exit()

if folder_check == True:
    # Create new folder in location if it doesn't exist
    if os.path.isdir(os.path.join(location, 'anilist_man')):
        dat_dir = os.path.join(location, 'anilist_man')
    
    else:
        # Make a new folder in location
        dat_dir = os.path.join(location, 'anilist_man')
        try:
            os.mkdir(dat_dir)
        except PermissionError:
            print(f"Unable to create folder {dat_dir}")
        
token_dat_dir_file = os.path.join(dat_dir, 'token.txt')
id_dat_dir_file = os.path.join(dat_dir, 'id.txt')

try:
    with open(token_dat_dir_file, "r") as f:
        token = f.read()
except FileNotFoundError:
    try:
        webbrowser.open("https://anilist.co/api/v2/oauth/authorize?client_id=7501&response_type=token",new=0,autoraise=True)
        print(f"Visit https://anilist.co/api/v2/oauth/authorize?client_id=7501&response_type=token")
        try:
            token = str(input("\n[+] Enter your token: "))
            if token == "" or token == None or token == " " or token.strip() == "":
                print("[-] Token is empty")
                sys.exit()
        except BaseException:
            print("\n[-] Invalid token")
            sys.exit()
        try:
            with open(token_dat_dir_file, "w") as f:
                f.write(token)
        except FileNotFoundError or PermissionError:
            print("[-] File not found or permission denied.")
            sys.exit()
    except KeyboardInterrupt:
        sys.exit()

base_url = "https://graphql.anilist.co"
headers = {
    'Authorization': 'Bearer ' + token,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

try:
    with open(id_dat_dir_file, "r") as f:
        uid = f.read()
except FileNotFoundError:
    print(f"[!] No user id found in {dat_dir}")
    try:
        c1 = str(input("\n[+] Enter your User Name: "))
        if c1 == "" or c1 == None or c1 == " " or c1.strip() == "":
            print("[-] User Name is empty")
            sys.exit()
    except BaseException or KeyboardInterrupt:
        sys.exit()
    query = queryUser
    resp = QueryFunctions.getUser(query, headers, c1)
    try:
        username = resp["data"]["User"]["name"]
        uid = resp["data"]["User"]["id"]
        print(f"[+] User ID: {uid} | User Name: {username}")
        conf = str(input("\n[+] Do you want to save this user id? [y/n]: "))
        if conf == "" or conf == None or conf == " " or conf.strip() == "":
            print("[-] Invalid input")
            sys.exit()
        if conf == "y" or conf == "Y":
            try:
                with open(id_dat_dir_file, "w") as f:
                    f.write(str(uid))
            except FileNotFoundError or PermissionError:
                print("[-] File not found or permission denied.")
                sys.exit()
        else:
            print("[!] User id not saved")
            sys.exit()
    except KeyError:
        print(f"[!] User {c1} not found")
        sys.exit()

uid = int(uid)

@app.command(short_help="Get user's name and id")
def user(user: Optional[str] = typer.Option(..., "--user", "-u", help="Information on the provided user")):
    if user == None or user == "" or user == " " or user.strip() == "":
        print("[-] Invalid user")
        sys.exit()
    query = queryUser
    resp = QueryFunctions.getUser(query, headers, user)
    try:
        username = resp["data"]["User"]["name"]
        uid = resp["data"]["User"]["id"]
        print(f"[+] User ID: {uid} | User Name: {username}")
    except KeyError:
        print(f"[!] User {user} not found")
        sys.exit()

@app.command(short_help="Get your current manga collection")
def manga():
    query = queryMangaCollection
    subFunc.mangaList(query, headers, uid)

@app.command(short_help="Update any manga in your current manga collection")
def update():
    query1 = queryMangaCollection
    subFunc.mangaList(query1, headers, uid)

    try:
        index = int(input("[+] Enter index of manga: "))
    except ValueError or KeyboardInterrupt:
        print("[-] Error")
        sys.exit()

    query2 = queryUpdateManga
    mangaList = QueryFunctions.getMangaStats(query1, headers, uid)
    mangaList = mangaList["data"]["MediaListCollection"]["lists"][0]["entries"][::-1]
    

    if index not in range(len(mangaList)):
        print("[-] Index out of range")
    manga = mangaList[index - 1]
    english = manga["media"]["title"]["english"]
    romaji = manga["media"]["title"]["romaji"]
    current_progress = manga["progress"]
    print(f"[+] Updating {english} | ({romaji}) | {current_progress}")
    listEntryId = manga["id"]

    try:
        progress = int(input("[+] Enter progress: "))
    except ValueError or KeyboardInterrupt:
        print("[-] Error")
        sys.exit()

    if progress == 0 or progress < 0:
        print("[-] Progress cannot be 0 or less")
    else:
        QueryFunctions.updateMangaStats(query2, headers, listEntryId, progress)
        print(f"[+] Updated {manga['media']['title']['romaji']} to {progress}")

if __name__ == "__main__":
    app()