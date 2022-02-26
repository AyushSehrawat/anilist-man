import requests

s = requests.Session()

base_url = "https://graphql.anilist.co"

class QueryFunctions():
    def __init__(self):
        pass

    def getUser(query, headers, name : str):
        variables = {
            "name" : name
        }
        query = query
        resp = s.post(base_url, json={'query': query, 'variables': variables}, headers=headers)
        return resp.json()

    def getManga(query, headers, id):
        variables = {
            "id" : id,
        }
        query = query
        resp = s.post(base_url, json={'query': query, 'variables': variables}, headers=headers)
        return resp.json()

    def getMangaStats(query, headers, userid):
        variables = {
            "userId" : userid,
        }
        query = query
        resp = s.post(base_url, json={'query': query, 'variables': variables}, headers=headers)
        return resp.json()

    def soonMangaStats(query, headers, userid):
        variables = {
            "userId" : userid,
        }
        query = query
        resp = s.post(base_url, json={'query': query, 'variables': variables}, headers=headers)
        return resp.json()

    def updateMangaStats(query, headers, listEntryId : int, progress : int):
        variables = {
            "listEntryId" : listEntryId,
            "updated_chap" : progress
        }
        query = query
        resp = s.post(base_url, json={'query': query, 'variables': variables}, headers=headers)
        return resp.json()
