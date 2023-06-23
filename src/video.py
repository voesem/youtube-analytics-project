import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:

    def __init__(self, video_id: str):
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        self.__video_id = video_id
        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.__video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title

    @property
    def video_id(self):
        return self.__video_id


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()

        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()
        self.title = playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']
        self.__playlist_id = playlist_id

    def __str__(self):
        return self.title

    @property
    def playlist_id(self):
        return self.__playlist_id
