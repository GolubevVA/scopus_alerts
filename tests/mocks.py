from internal.scheduler.repository import SchedulerRepositoryInterface
from internal.scheduler.job import SchedulerJobInterface
from datetime import datetime

class FakeSchedulerRepo(SchedulerRepositoryInterface):
    def __init__(self, initial: datetime | None = None):
        self._ts = initial

    def get_timestamp(self) -> datetime | None:
        return self._ts

    def set_timestamp(self, ts: datetime) -> None:
        self._ts = ts

class FakeSchedulerJob(SchedulerJobInterface):
    def __init__(self):
        self.calls: list[tuple[datetime, datetime]] = []

    async def work(self, last_run: datetime, current_run: datetime) -> None:
        self.calls.append((last_run, current_run))

FIXED_TIME_FOR_SCHEDULER_NOW = datetime(2025, 1, 1, 0, 0, 0)
class FakeDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return FIXED_TIME_FOR_SCHEDULER_NOW
