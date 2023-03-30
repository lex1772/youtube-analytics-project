import os

from googleapiclient.discovery import build

from googleapiclient.errors import HttpError



class Video:
    api_key: str = os.getenv('YouTube-API')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео."""
        self.__video_id = video_id

    def print_info(self) -> None:
        try:
            self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.__video_id).execute()[
                'items'][0]['id']
        except IndexError:
            return None
        else:
            video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                        id=self.__video_id
                                                        ).execute()
            print(video_response)


    @property
    def video_id(self):
        try:
            return \
                self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.__video_id).execute()[
                'items'][0]['id']
        except IndexError:
            return self.video_id

    @property
    def video_title(self):
        try:
            return self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                      id=self.__video_id).execute()[
            'items'][0]['snippet']['title']
        except IndexError:
            return None

    @property
    def url(self):
        try:
            self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.__video_id).execute()[
                'items'][0]['id']
        except IndexError:
            return None
        else:
            return "https://www.youtube.com/watch?v=" + self.__video_id

    @property
    def views_count(self):
        try:
            return \
            self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.__video_id).execute()[
                'items'][0]['statistics']['viewCount']
        except IndexError:
            return None

    @property
    def like_count(self):
        try:
            return \
            self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=self.__video_id).execute()[
                'items'][0]['statistics']['likeCount']
        except IndexError:
            return None

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    def print_info(self) -> None:
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        print(playlist_videos)

    @property
    def video_id(self):
        return super().video_id

    @property
    def video_title(self):
        return super().video_title

    @property
    def url(self):
        return super().url

    def views_count(self):
        return super().views_count

    def like_count(self):
        return super().like_count

    def playlist_id(self):
        return self.youtube.playlistItems().list(playlistId=self.__playlist_id, part='contentDetails',
                                                 maxResults=50, ).execute()['items']['0']['id']


