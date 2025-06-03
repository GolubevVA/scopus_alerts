from config import Config
from internal.scheduler import SchedulerRepository

def main():
	config: Config = Config.from_yml("config/config.yml")
	scheduler_repository = SchedulerRepository(config.storage_config.storage_dir)
	print(f"Scheduler repo initialized: {scheduler_repository.get_timestamp()}")

if __name__ == "__main__":
	main()
