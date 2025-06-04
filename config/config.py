import os
from dotenv import load_dotenv
import yaml
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, model_validator

LOCAL_MODE_FLAG = "LOCAL"

CONFIG_FILE_PATH = Path("config/config.yml")

load_dotenv()

def check_flag_set(flag: str) -> bool:
	"""Check if a specific environment variable is set."""
	return os.getenv(flag) is not None

def get_env_var(name: str) -> str:
	"""Retrieve an environment variable, raising an error if not set."""
	value = os.getenv(name)
	if value is None:
		raise ValueError(f"Environment variable {name} is not set")
	return value

class LoggerConfig(BaseModel):
	log_level: str = Field("INFO", alias="LogLevel")
	model_config = ConfigDict(populate_by_name=True)

class ScopusConfig(BaseModel):
	scopus_api_key: str = Field(default_factory=lambda: get_env_var("SCOPUS_API_KEY"))
	model_config = ConfigDict()

class PushyConfig(BaseModel):
	model_config = ConfigDict()

class OpenAIConfig(BaseModel):
	model_config = ConfigDict()

class AlertsConfig(BaseModel):
    scheduling_interval_in_days: int = Field(7, alias="SchedulingIntervalInDays")
    first_run_time: datetime = Field(default_factory=datetime.now, alias="FirstRunTime")
    model_config = ConfigDict(populate_by_name=True)

class StorageConfig(BaseModel):
   storage_dir: Path

   model_config = ConfigDict(populate_by_name=True)

   @model_validator(mode="before")
   def _parse_storage_dir(cls, data: dict[str, str]) -> dict[str, Path]:
       """
       Receives the raw dict
           {"LocalStorageDir": "...", "ProdStorageDir": "..."}
       and returns only {"storage_dir": Path(chosen)}.
       """
       local = data.get("LocalStorageDir")
       prod = data.get("ProdStorageDir")
       chosen = local if check_flag_set(LOCAL_MODE_FLAG) else prod
       return {"storage_dir": Path(chosen)}

class Config(BaseModel):
	scopus_config: ScopusConfig = Field(default_factory=ScopusConfig)
	pushy_config: PushyConfig = Field(default_factory=PushyConfig)
	openai_config: OpenAIConfig = Field(default_factory=OpenAIConfig)
	alerts_config: AlertsConfig = Field(alias="Alerts")
	storage_config: StorageConfig = Field(alias="Storage")
	logger_config: LoggerConfig = Field(alias="Logger")

	model_config = ConfigDict(populate_by_name=True)

	@classmethod
	def from_yml(cls, path: Path = CONFIG_FILE_PATH) -> 'Config':
		"""Load config from YAML file with validation via Pydantic models"""
		raw = yaml.safe_load(path.read_text(encoding="utf-8"))
		return cls.model_validate(raw)
