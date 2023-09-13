import os
from googleapiclient.discovery import build


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                       id=video_id).execute()

        self.title = self.response['items'][0]['snippet']['title']
        self.description = self.response['items'][0]['snippet']['description']
        self.likeCount = int(self.response['items'][0]['statistics']['likeCount'])
        self.viewCount = int(self.response['items'][0]['statistics']['viewCount'])
        self.duration = self.response["items"][0]['contentDetails']['duration']
        self.url_video = 'https://www.youtube.com/' + self.response['items'][0]['snippet']['customUrl']

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
