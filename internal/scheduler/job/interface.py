from abc import ABC, abstractmethod
from datetime import datetime

class SchedulerJobInterface(ABC):
	"""
	Interface of a job, which is scheduled to run periodically.
	"""
	@abstractmethod
	async def work(self, last_run: datetime, current_run: datetime) -> None:
		"""
		Args:
			last_run (datetime): The timestamp of the last run of the job.
			current_run (datetime): The timestamp of the current run of the job.
		"""
		pass
