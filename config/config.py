import os
from dotenv import load_dotenv
import yaml
from typing import Optional
from pathlib import Path

LOCAL_MODE_FLAG = "LOCAL"

load_dotenv()

def check_flag_set(flag: str) -> bool:
	return os.getenv(flag) is not None

def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable {name} is not set")
    return value

class ScopusConfig:
	scopus_api_key: str

	def __init__(self):
		self.scopus_api_key = get_env_var("SCOPUS_API_KEY")

class PushyConfig:
	pass

class OpenAIConfig:
	pass

class AlertsConfig:
	period_in_days: int

	def __init__(self, period_in_days: int = 7):
		self.period_in_days = period_in_days

class StorageConfig:
	storage_dir: Path

	def __init__(self, prod_storage_dir: str = "../data", local_storage_dir: str = "./data"):
		if check_flag_set(LOCAL_MODE_FLAG):
			self.storage_dir = Path(local_storage_dir)
		else:
			self.storage_dir = Path(prod_storage_dir)

class Config:
	scopus_config: ScopusConfig
	pushy_config: PushyConfig
	openai_config: OpenAIConfig
	alerts_config: AlertsConfig
	storage_config: StorageConfig

	def __init__(self, scopus_config: Optional[ScopusConfig] = None, 
				 pushy_config: Optional[PushyConfig] = None, 
				 openai_config: Optional[OpenAIConfig] = None,
				 alerts_config: Optional[AlertsConfig] = None,
				 storage_config: Optional[StorageConfig] = None):
		self.scopus_config = scopus_config if scopus_config is not None else ScopusConfig()
		self.pushy_config = pushy_config if pushy_config is not None else PushyConfig()
		self.openai_config = openai_config if openai_config is not None else OpenAIConfig()
		self.alerts_config = alerts_config if alerts_config is not None else AlertsConfig()
		self.storage_config = storage_config if storage_config is not None else StorageConfig()

	def from_yml(path: str | None) -> 'Config':
		if path is None:
			path = os.path.join(os.path.dirname(__file__), './config.yml')
		with open(path, 'r') as file:
			data: dict[str, dict] = yaml.safe_load(file)
			alerts = AlertsConfig(data.get('Alerts', {}).get('PeriodInDays', 7))
			storage = StorageConfig(prod_storage_dir=data.get('Storage', {}).get('ProdStorageDir', '/data'),
								 local_storage_dir=data.get('Storage', {}).get('LocalStorageDir', './data'))
			return Config(alerts_config=alerts, storage_config=storage)
