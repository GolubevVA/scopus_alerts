from config import PushyConfig

DEFAULT_ENDPOINT = "https://api.pushy.tg"


class NotificationService:
    def __init__(self, config: PushyConfig):
        self.config = config

    def send_notifications(self, notifications):
        print("Sending notifications...")
