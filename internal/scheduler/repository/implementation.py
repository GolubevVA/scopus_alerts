from .interface import SchedulerRepositoryInterface
from datetime import datetime
from pathlib import Path
from typing import Optional

TIMESTAMP_FILE = "timestamp.txt"

class SchedulerRepository(SchedulerRepositoryInterface):
	"""
	File-based implementation of the Repository interface for storing a single timestamp.

	The timestamp is persisted as an ISO-formatted string in: "_storage_dir_/timestamp.txt"
	"""

	def __init__(self, storage_dir: str | Path):
		"""
		Initializes the repository.

        Args:
            storage_dir: directory under which the timestamp file will live.
            
        If the directory does not exist, it will be created.
        """
		directory = Path(storage_dir)
		directory.mkdir(parents=True, exist_ok=True)
		self.timestamp_path: Path = directory / TIMESTAMP_FILE
	
	def get_timestamp(self) -> Optional[datetime]:
		"""
        Read and return the stored timestamp.

        Returns:
            datetime parsed from the ISO string in the file,
            or None if the file does not exist or empty.
            
        Raises ValueError if the content is not a valid ISO timestamp.
        """
		if not self.timestamp_path.exists():
			return None

		text = self.timestamp_path.read_text(encoding="utf-8").strip()
		if not text:
			return None
		try:
			return datetime.fromisoformat(text)
		except ValueError as e:
			raise ValueError(f"Invalid timestamp format in {self.timestamp_path}: {text}") from e
		
	def set_timestamp(self, timestamp: datetime) -> None:
		"""
        Write the given timestamp to the file in ISO format.

        Args:
            timestamp: the datetime to persist.
        """
		self.timestamp_path.parent.mkdir(parents=True, exist_ok=True)
		self.timestamp_path.write_text(timestamp.isoformat(), encoding="utf-8")
