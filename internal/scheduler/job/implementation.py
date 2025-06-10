from .interface import SchedulerJobInterface
from pkg.scopus import ScopusClient, Article
from datetime import datetime, timedelta, timezone
from ...article_processing.lang_retriever import LangRetriever
from pkg.logger import get_logger

def fix_timezone(dt: datetime) -> datetime:
	"""
	Fixes the timezone of a datetime object to UTC.
	
	If the datetime object is naive, it will be set to UTC. If it is already timezone-aware,
	it will be converted to UTC.
	"""
	if dt.tzinfo is None:
		return dt.replace(tzinfo=timezone.utc)
	else:
		return dt.astimezone(timezone.utc)

class SchedulerJob(SchedulerJobInterface):
	"""
	Implementation of the Job interface for scheduling tasks.
	
	This class is responsible for orchestrating the retrieval of articles and sending notifications.
	"""

	def __init__(self, scopus_client: ScopusClient, lang_retriever: LangRetriever):
		"""
		Initializes the Job with a scopus clien and a lang retriever.
		"""
		self.scopus_client = scopus_client
		self.lang_retriever = lang_retriever
		self.logger = get_logger()

	async def work(self, last_run: datetime, current_run: datetime) -> None:
		"""
		Retrieves articles from SCOPUS, sends notifications to the users, updates the timestamp.
		
		This method should be implemented with the actual logic for retrieving articles, 
		marking them with languages and sending notifications.

		Raises errors if any step fails, such as retrieving languages or sending notifications.
		"""

		last_run = fix_timezone(last_run)
		current_run = fix_timezone(current_run)

		date_from = datetime.combine(
            last_run.date(),
            datetime.min.time(),
            tzinfo=timezone.utc
        )

		date_to = datetime.combine(
            current_run.date() - timedelta(days=1),
            datetime.min.time(),
            tzinfo=timezone.utc
        )

		new_articles: list[Article] = await self.scopus_client.search(date_from=date_from, date_to=date_to)

		self.logger.info(f"Retrieved {len(new_articles)} new articles from SCOPUS between {date_from} and {date_to}.")

		articles_by_langs: dict[str, list[Article]] = {}
		for article in new_articles:
			try:
				languages = await self.lang_retriever.retrieve(article.title)
				for lang in languages:
					if lang not in articles_by_langs:
						articles_by_langs[lang] = []
					articles_by_langs[lang].append(article)
			except Exception as e:
				raise Exception(f"Failed to retrieve languages for article '{article.title}': {e}")
		
		self.logger.info(f"Found {len(articles_by_langs)} unique languages: {', '.join(articles_by_langs.keys())}.")

		# TODO: calling pushy

		raise NotImplementedError("Awaiting for pushy to be implemented.")
