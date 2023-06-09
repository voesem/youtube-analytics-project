import json

from googleapiclient.discovery import build

# метод os.getenv('YOUTUBE_API_KEY')
# выдает ошибку google.auth.exceptions.DefaultCredentialsError, поэтому ключ ввожу прямо здесь
api_key: str = 'AIzaSyASr8OrVL1W1yIxfphOLonE_Y9PMn45ZNg'
youtube = build('youtube', 'v3', developerKey=api_key)


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется по id канала. Остальные данные подтягиваются по API."""
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

        self.__channel_id = channel_id
        self.title = channel['items'][0]['snippet']['title']
        self.channel_description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)

    @property
    def channel_id(self):
        return self.__channel_id

    def to_json(self, filename):
        data = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'channel_description': self.channel_description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(filename, encoding='utf-8', mode='w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=api_key)
