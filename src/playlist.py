import os

import isodate as isodate
from datetime import datetime, timedelta
from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.video import PLVideo

load_dotenv()

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:

    def __init__(self, playlist_id: str):
        playlist_videos = youtube.playlists().list(id=playlist_id, part='snippet', maxResults=50, ).execute()

        self.title = playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        self.playlist_id = playlist_id

    @property
    def total_duration(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()

        duration_list = []
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            duration_list.append(duration)

        return timedelta(seconds=sum(td.total_seconds() for td in duration_list))

    def show_best_video(self):
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        max_like_count = 0

        for video in video_response['items']:
            if int(video['statistics']['likeCount']) > int(max_like_count):
                max_like_count = video['statistics']['likeCount']

        for video in video_response['items']:
            if max_like_count == video['statistics']['likeCount']:
                return f'https://youtu.be/{video["id"]}'
