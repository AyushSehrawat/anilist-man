queryUser = """
query ($name: String) {
    User (name: $name) {
        id
        name
    }
}
"""

queryManga = """
query ($id: Int) {
  Media (id: $id, type: MANGA) {
    id
    synonyms
    title {
      romaji
      english
    }
  }
}
"""

queryMangaCollection = """
query ($userId: Int) {
  MediaListCollection(userId: $userId, type: MANGA, status: CURRENT, sort: UPDATED_TIME) {
    lists {
      entries {
        id
        progress
        media {
          id
          title {
            romaji
            english
          }
        }
      }
    }
  }
}
"""

querySoonMMangaCollection = """
query ($userId: Int) {
  MediaListCollection(userId: $userId, type: MANGA, status: PLANNING, sort: UPDATED_TIME) {
    lists {
      entries {
        id
        media {
          id
          title {
            romaji
            english
          }
        }
      }
    }
  }
}
"""

queryUpdateManga = """
mutation ($listEntryId: Int, $updated_chap : Int) {
  SaveMediaListEntry(id: $listEntryId, progress: $updated_chap) {
    id
    progress
  }
}
"""