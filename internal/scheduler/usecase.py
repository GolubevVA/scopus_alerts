from abc import ABC, abstractmethod

class Scheduler(ABC):
	@abstractmethod
	async def run(self) -> None:
		"""
		Tracks changs in Scopus and sends notifications about new articles.
		"""
		pass

	@abstractmethod
	async def stop(self) -> None:
		"""
		Stops the scheduler.
		"""
		pass
