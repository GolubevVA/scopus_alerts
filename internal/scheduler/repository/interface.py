from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class SchedulerRepositoryInterface(ABC):
	@abstractmethod
	def get_timestamp(self) -> Optional[datetime]:
		"""
		Returns the last saved timestamp.
		"""
		pass
    
	@abstractmethod
	def set_timestamp(self, timestamp: datetime) -> None:
		"""
		Sets a new timestamp.
		"""
		pass
