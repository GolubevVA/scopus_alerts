from ..job import SchedulerJobInterface
from datetime import timedelta, datetime
from typing import Optional
from ..repository import SchedulerRepositoryInterface
from pkg.logger import get_logger
import asyncio

class Scheduler:
	"""
	Scheduler class that orchestrates the scheduling of jobs.
	"""
	def __init__(
		self,
		repository: SchedulerRepositoryInterface,
		job: SchedulerJobInterface,
		scheduling_interval: timedelta = timedelta(days = 7), 
		first_run_time: Optional[datetime] = None
	):
		"""
		Initializes the scheduler with a use case instance.
		
		Args:
			repository: An instance of the repository for managing timestamps.
			job: The job to be scheduled regularly.
			scheduling_interval: The interval at which the job should be run.
			first_run_time: The time when the job should first run. If it's None and there's no stored timestamp, it defaults to the current time. If it's set and the stored timestamp is later, it will be ignored.
		"""
		self.repository = repository
		self.job = job
		self.scheduling_interval = scheduling_interval
		self._stop_event = asyncio.Event()

		stored_timestamp = self.repository.get_timestamp()
		if stored_timestamp is None:
			if first_run_time is None:
				self.next_run_time = datetime.now()
			else:
				self.next_run_time = first_run_time
		else:
			if first_run_time is not None and first_run_time > stored_timestamp:
				self.next_run_time = first_run_time
			else:
				self.next_run_time = stored_timestamp + self.scheduling_interval

		self.logger = get_logger()
	
	async def _run_once(self) -> None:
		"""
		Runs the job once and updates the next run time.
		
		Returns:
			bool: True if the job was run successfully, False if it was not run due to the next run time not being reached.
		"""
		self.logger.info(f"Running job at {datetime.now()}. Next run scheduled for {self.next_run_time}.")

		current_time = datetime.now()
		if current_time < self.next_run_time:
			self.logger.info("Not running job yet, waiting for next scheduled time.")
			return

		self.logger.info("Running job now.")
		await self.job.work(
			self.repository.get_timestamp() or current_time - timedelta(days=self.scheduling_interval.days),
			current_time
		)
		self.logger.info("Job completed successfully.")

		self.repository.set_timestamp(current_time)

		self.next_run_time += self.scheduling_interval
		self.logger.info(f"Next run time updated to {self.next_run_time}.")
	
	async def run(self) -> None:
		"""
        Starts the scheduling loop. The loop will sleep until the next run time,
        wake up to execute the job if due, then repeat. Call `stop()` to exit.
        """
		self._stop_event.clear()
		while not self._stop_event.is_set():
			await self._run_once()

			delay = (self.next_run_time - datetime.now()).total_seconds()
			if delay > 0:
				try:
					await asyncio.wait_for(self._stop_event.wait(), timeout=delay)
					self.logger.info("Scheduler stopped.")
				except asyncio.TimeoutError:
					continue

	async def stop(self) -> None:
		"""
        Signals the scheduling loop to stop. The loop will exit at the next check.
        """
		self.logger.info("Stopping the scheduler...")
		self._stop_event.set()
