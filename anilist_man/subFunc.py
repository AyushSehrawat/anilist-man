from anilist_man.queryFunc import QueryFunctions
from anilist_man.queries import queryUser, queryManga, queryMangaCollection, querySoonMMangaCollection
from anilist_man.queries import queryUpdateManga

class subFunc():
    def __init__(self):
        pass
    
    def mangaList(query,headers,userid):
        mangalist = QueryFunctions.getMangaStats(query, headers, userid)
        mangalist = mangalist["data"]["MediaListCollection"]["lists"][0]["entries"]
        print(f"Total Current Manga: {len(mangalist)}")

        for m in mangalist:
            index = len(mangalist) - mangalist.index(m)
            if index < 10:
                index = "0" + str(index)
            else:
                index = str(index)
            list_id = m["id"]
            romaji = m["media"]["title"]["romaji"]
            english = m["media"]["title"]["english"]
            progress = m['progress']
            if english == None:
                print(f"{index} {romaji} - {progress}")
            else:
                print(f"{index} {english} - {progress}")