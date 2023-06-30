import os

import isodate as isodate
from datetime import datetime
from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.video import PLVideo

load_dotenv()

api_key: str = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList(PLVideo):

    def __init__(self, playlist_id: str):
        super().__init__(playlist_id)
        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                       part='contentDetails,snippet',
                                                       maxResults=50,
                                                       ).execute()

        self.title = playlist_videos['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.video_id}'
        self.__playlist_id = playlist_id

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

            return sum(duration_list)

    def show_best_video(self):
        pass


# playlist_id = 'PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw'
#
# playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
#                                                part='contentDetails,snippet',
#                                                maxResults=50,
#                                                ).execute()
#
# video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
#
# video_response = youtube.videos().list(part='contentDetails,statistics',
#                                        id=','.join(video_ids)
#                                        ).execute()
#
# duration_list = []
# for video in video_response['items']:
#     # YouTube video duration is in ISO 8601 format
#     iso_8601_duration = video['contentDetails']['duration']
#     duration = isodate.parse_duration(iso_8601_duration)
#     print(duration)

pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
print(pl.title)
