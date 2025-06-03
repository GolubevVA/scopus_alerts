from config import Config, CONFIG_FILE_PATH
from internal.scheduler import SchedulerRepository, SchedulerJob, Scheduler
from pkg.scopus import ScopusClient
import asyncio

async def main():
	config: Config = Config.from_yml(CONFIG_FILE_PATH)
	scopus_client = ScopusClient(config.scopus_config.scopus_api_key)
	# pushy and lang marker instances would be created here when implemented
	scheduler_repository = SchedulerRepository(config.storage_config.storage_dir)
	scheduler_job = SchedulerJob(scopus_client)
	scheduler = Scheduler(
		scheduler_repository,
		scheduler_job,
		config.alerts_config.scheduling_interval_in_days,
		config.alerts_config.first_run_time
	)
	await scheduler.run()

if __name__ == "__main__":
	asyncio.run(main())
