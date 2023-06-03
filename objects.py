import typing as t

class AnimeType(t.TypedDict):
    name: str
    description: str
    page: str
    image: str
    type: str

class ServerType(t.TypedDict):
    name: str
    url: str

class EpisodeType(t.TypedDict):
    title: str
    image: str
    watch_page: str
    servers: t.List[ServerType]
