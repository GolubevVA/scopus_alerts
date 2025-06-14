import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from internal.scheduler.repository import SchedulerRepository
from internal.scheduler.repository.implementation import TIMESTAMP_FILE

def test_get_timestamp_none(tmp_path: Path):
    """If no timestamp file exists, get_timestamp returns None."""
    repo = SchedulerRepository(tmp_path)
    assert repo.get_timestamp() is None

def test_empty_file_returns_none(tmp_path: Path):
	"""If the timestamp file exists but is empty, get_timestamp returns None."""
	repo = SchedulerRepository(tmp_path)
	(tmp_path / TIMESTAMP_FILE).write_text("", encoding="utf-8")
	assert repo.get_timestamp() is None

def test_set_and_get_timestamp(tmp_path: Path):
	"""After setting a timestamp, get_timestamp returns the same datetime."""
	repo = SchedulerRepository(tmp_path)
	ts = datetime(2025, 6, 10, 10, 0, 0)
	repo.set_timestamp(ts)
	read_ts = repo.get_timestamp()
	assert isinstance(read_ts, datetime)
	assert read_ts == ts

def test_invalid_timestamp_format_raises(tmp_path: Path):
	"""If the timestamp file contains malformed text, get_timestamp raises ValueError."""
	repo = SchedulerRepository(tmp_path)
	(tmp_path / TIMESTAMP_FILE).write_text("not-a-valid-timestamp", encoding="utf-8")
	with pytest.raises(ValueError):
		repo.get_timestamp()
