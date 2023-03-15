import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YouTube-API')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(channel)

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, name):
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        with open(name, "w", encoding='utf-8') as file:
            json.dump(channel, file)

    @property
    def channel_id(self):
        return self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()['items'][0]['id']

    @property
    def title(self):
        return self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()['items'][0]['snippet']['title']

    @property
    def description(self):
        return self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()['items'][0]['snippet']['description']

    @property
    def url(self):
        return "https://www.youtube.com/channel/" + self.channel_id

    @property
    def video_count(self):
        return  self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()['items'][0]['statistics']['videoCount']

    @property
    def subscriber_count(self):
        return self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()['items'][0]['statistics']['subscriberCount']

    @property
    def view_Count(self):
        return self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'"{self.title}" ("{self.url}")'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __ne__(self, other):
        return int(self.subscriber_count) != int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)
