import aiohttp

from config import PushyConfig
from pkg.scopus import Article

DEFAULT_ENDPOINT = "https://api.pushy.tg"


class NotificationService:
    def __init__(self, config: PushyConfig):
        self.config = config

    async def send_notifications(self, articles: dict[str, list[Article]]):
        for lang, articles in articles.items():
            if len(articles) == 0:
                continue
            message = f"Новые статьи для языка <b>{lang}</b>:\n\n"
            for article in articles:
                message += f"{self._article_to_str(article)}\n\n"
            await self._send_message(message, lang)

    async def _send_message(self, text: str, lang: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{DEFAULT_ENDPOINT}/v1/feeds/{self.config.feed}/text",
                                        params={"tags": lang, "mode": "html"}, data=text) as post:
                    await post.json()
        except Exception as ignored:
            pass

    @classmethod
    def _article_to_str(cls, article: Article) -> str:
        return (f'<b><a href="{article.scopus_link}">{article.title}</a></b>\n'
                f"<b>Автор:</b> {article.creator}\n")
