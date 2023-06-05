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
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)
