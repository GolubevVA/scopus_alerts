from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

class SchedulerRepositoryInterface(ABC):
	@abstractmethod
	def get_timestamp(self) -> Optional[datetime]:
		"""
        Reads and returns the stored timestamp.

        Returns:
            datetime or None if the file does not exist or empty.
        
        Raises ValueError if the content of the file con not be parsed as a datetime.
        """
		pass
    
	@abstractmethod
	def set_timestamp(self, timestamp: datetime) -> None:
		"""
        Writes the given timestamp to the file.

        Args:
            timestamp: the datetime to persist.
        """
		pass
