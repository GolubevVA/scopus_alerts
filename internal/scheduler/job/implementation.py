from .interface import SchedulerJobInterface
from pkg.scopus import ScopusClient, Article
from datetime import datetime, timedelta, timezone

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

	def __init__(self, scopus_client: ScopusClient):
		"""
		Initializes the use case with a scopus client and a timestamp repository instance.
		"""
		self.scopus_client = scopus_client

	async def work(self, last_run: datetime, current_run: datetime) -> None:
		"""
		Retrieves articles from SCOPUS, sends notifications to the users, updates the timestamp.
		
		This method should be implemented with the actual logic for retrieving articles, 
		marking them with languages and sending notifications.
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

		results: list[Article] = await self.scopus_client.search(date_from=date_from, date_to=date_to)

		# TODO: calling lang marker

		# TODO: calling pushy

		raise NotImplementedError("Awaiting for pushy and langs marker classes to be implemented.")
