import os
import json
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        try:
            self.response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id).execute()
            self.title = self.response['items'][0]['snippet']['title']
        except IndexError:
            self.response = None
            self.title = None
            self.url_video = None
            self.like_count = None
            self.viewCount = None
            self.duration = None
        else:
            self.description = self.response['items'][0]['snippet']['description']
            self.like_count = int(self.response['items'][0]['statistics']['likeCount'])
            self.viewCount = int(self.response['items'][0]['statistics']['viewCount'])
            self.duration = self.response["items"][0]['contentDetails']['duration']
            self.url_video = f"https://youtu.be/{self.video_id}"

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def __str__(self):
        return f"{self.title}"

class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
