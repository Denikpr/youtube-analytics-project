import os
import json
import isodate
from datetime import timedelta
from src.video import Video
from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlists = self.get_service().playlists().list(id=self.playlist_id,
                                                                   part='snippet',
                                                                   maxResults=50).execute()

        self.title = self.playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.info_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                   part='contentDetails, snippet',
                                                                   maxResults=50).execute()
        #print(json.dumps(self.info_videos, indent=2, ensure_ascii=False))
        self.videos = self.get_videos()

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def get_videos(self):
        result = []
        for id in self.get_videos_ids():
            video = Video(id)
            result.append(video)
        return result

    def get_videos_ids(self):
        return [video['contentDetails']['videoId'] for video in self.info_videos['items']]

    @property
    def total_duration(self):
        result = timedelta(seconds=0)
        for video in self.videos:
            result += isodate.parse_duration(video.duration)
        return result

    def show_best_video(self):







