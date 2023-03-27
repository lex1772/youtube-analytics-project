import os
import isodate
from datetime import timedelta

from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YouTube-API')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id

    def print_info(self) -> None:
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        print(playlist_videos)

    @property
    def title(self):
        video_id = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                     part='contentDetails',
                                                     maxResults=50,
                                                     ).execute()['items'][0]['contentDetails']['videoId']
        video_response = str({
            self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()[
                'items'][0]['snippet']['title']})
        index = video_response.index("/")
        title = video_response[index + 1:-2]
        title = title.split()
        return f'{title[0]}. {title[1]}'

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        total = timedelta(seconds=0)
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total += duration

        return total

    def show_best_video(self):
        top_video = ''
        top_likes = 0
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > top_likes:
                top_video = video['id']
        return f'https://youtu.be/{top_video}'
