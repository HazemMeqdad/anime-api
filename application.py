import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import typing as t
from database import Database
from objects import AnimeType, EpisodeType
from cache import Cache

BASE_URL = "https://witanime.com/"

class WitClient:
    def __init__(self, db: Database):
        self.db = db
        self.cache = Cache(60 * 60 * 24)

    def _process_anime(self, anime: Tag) -> AnimeType:
        return {
            "name": anime.find("div", {"class": "anime-card-title"}).get("title"),
            "description": anime.find("div", {"class": "anime-card-title"}).get("data-content"),
            "page": anime.find("a").get("href"),
            "image": anime.find("img").get("src"),
            "type": anime.find("div", {"class": "anime-card-type"}).find('a').text,
        }

    def search_anime(self, query: str) -> t.List[AnimeType]:
        """
        Search for an anime
        
        Parameters
        ----------
        query : str
            The query to search for
        """
        if self.cache.get(f"search:query:{query}") is not None:
            return self.cache.get(f"search:query:{query}")
        results = []
        res = requests.get(BASE_URL+f"/?search_param=animes&s={query.replace(' ', '+')}")
        soup = BeautifulSoup(res.text, "lxml")
        anime_list = soup.find("div", {"class": "anime-list-content"})
        if not anime_list:
            return None
        animes: t.List[Tag] = anime_list.find_all("div", {"class": "col-lg-2 col-md-4 col-sm-6 col-xs-6 col-no-padding col-mobile-no-padding"})
        for anime in animes:
            results.append(self._process_anime(anime))
        self.db.update_search(query, {"results": results})
        return results
    
    def get_anime(self, name: str):
        anime = self.cache.get(f"anime:{name}") or self.db.get_anime(name)
        if not anime:
            anime = WitClient.search_anime(name)
            if not anime:
                return None
            self.db.add_anime(anime)
        if not self.db.get_anime(name):
            self.cache.set(f"anime:{name}", anime)
        return anime
    
    def get_espiodes(self, page: str) -> t.List[EpisodeType]:
        """
        Get episodes from a page
        
        Parameters
        ----------
        page : str
            The page to get episodes from (e.g. https://witanime.com/anime/one-piece)
        """
        if self.cache.get(f"episodes:page:{page}") is not None:
            return self.cache.get(f"episodes:page:{page}")
        results = []
        res = requests.get(page)
        soup = BeautifulSoup(res.text, "lxml")
        episodes: t.List[Tag] = soup.find_all("div", {"class": "col-lg-3 col-md-3 col-sm-12 col-xs-12 col-no-padding col-mobile-no-padding DivEpisodeContainer"})
        for episode in episodes:
            results.append({
                "title": episode.find("a").text,
                "image": episode.find("img").get("src"),
                "watch_page": episode.find("a").get("href") 
            })
        self.cache.set(f"episodes:page:{page}", results)
        self.db.update_episodes(page, {"episodes": results})
        return results

    def get_servers(self, page: str):
        """
        Get servers from a page

        Parameters
        ----------
        page : str
            The page to get servers from watch page (e.g.  )
        """
        if self.cache.get(f"servers:page:{page}") is not None:
            return self.cache.get(f"servers:page:{page}")
        data = []
        res = requests.get(page)
        soup = BeautifulSoup(res.text, "lxml")
        servers = soup.find("ul", {"id": "episode-servers"})
        if not servers:
            return None
        servers: t.List[Tag] = servers.find_all("a")
        for server in servers:
            data.append({
                "title": server.text,
                "url": server.get("data-ep-url")
            })
        self.cache.set(f"servers:page:{page}", data)
        return data




