from config import Config, CONFIG_FILE_PATH
from internal.scheduler import SchedulerRepository, SchedulerJob, Scheduler
from pkg.notification.pushy_api import NotificationService
from pkg.scopus import ScopusClient
from pkg.logger import setup_logging, get_logger
from internal.article_processing.lang_retriever import LangRetriever
from datetime import timedelta
from internal.article_processing.prompt_builder import initialize_templates
import asyncio

async def main():
	config: Config = Config.from_yml(CONFIG_FILE_PATH)

	setup_logging(config.logger_config.log_level)
	logger = get_logger()
	logger.info("Configuration loaded successfully, logger initialized.")

	initialize_templates()
	logger.info("Templates initialized")

	scopus_client = ScopusClient(config.scopus_config.scopus_api_key)
	logger.info("Scopus client initialized successfully.")

	# pushy instance would be created here when implemented
	logger.warning("Pushy instance is not implemented yet, skipping initialization.")

	lang_retriever = LangRetriever(api_key=config.openai_config.openai_api_key)

	scheduler_repository = SchedulerRepository(config.storage_config.storage_dir)
	logger.info("Scheduler repository initialized successfully.")

	notification_service = NotificationService(config.pushy_config)
	logger.info("Scheduler repository initialized successfully.")

	scheduler_job = SchedulerJob(scopus_client, lang_retriever, notification_service)
	logger.info("Scheduler job initialized successfully.")

	scheduler = Scheduler(
		scheduler_repository,
		scheduler_job,
		timedelta(days=config.alerts_config.scheduling_interval_in_days),
		config.alerts_config.first_run_time
	)
	logger.info("Scheduler initialized successfully.")
	logger.info("Starting the scheduler...")
	try:
		await scheduler.run()
	except Exception as e:
		logger.error(f"An error occurred while running the scheduler: {e}")
		raise e

if __name__ == "__main__":
	asyncio.run(main())
