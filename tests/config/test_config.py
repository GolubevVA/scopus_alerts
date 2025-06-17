import pytest
from pathlib import Path
from datetime import datetime
from pydantic import ValidationError
from config.config import Config, LOCAL_MODE_FLAG

def test_config_load_nonexistent(tmp_path: Path):
    missing = tmp_path / "no_such.yml"
    with pytest.raises(FileNotFoundError):
        Config.from_yml(missing)

def test_config_load_valid(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SCOPUS_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-openai")
    monkeypatch.setenv("PUSHY_FEED", "test-pushy-feed")

    content = """
Alerts:
  SchedulingIntervalInDays: 5
  FirstRunTime: "2025-06-15T12:30:00"

Storage:
  LocalStorageDir: "./local_data"
  ProdStorageDir: "/prod_data"

Logger:
  LogLevel: "ERROR"
"""
    cfg_file = tmp_path / "config.yml"
    cfg_file.write_text(content, encoding="utf-8")

    monkeypatch.delenv(LOCAL_MODE_FLAG, raising=False)

    conf = Config.from_yml(cfg_file)

    assert conf.alerts_config.scheduling_interval_in_days == 5
    assert isinstance(conf.alerts_config.first_run_time, datetime)
    assert conf.alerts_config.first_run_time == datetime.fromisoformat("2025-06-15T12:30:00")

    assert conf.logger_config.log_level == "ERROR"

    assert conf.scopus_config.scopus_api_key == "test-key"

    assert conf.openai_config.openai_api_key == "test-key-openai"

    assert conf.storage_config.storage_dir == Path("/prod_data")

    monkeypatch.setenv(LOCAL_MODE_FLAG, "1")
    conf_local = Config.from_yml(cfg_file)
    assert conf_local.storage_config.storage_dir == Path("./local_data")

def test_config_missing_section(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("SCOPUS_API_KEY", "another-key")
    monkeypatch.setenv("OPENAI_API_KEY", "another-key-openai")
    monkeypatch.setenv("PUSHY_FEED", "test-pushy-feed")
    content = """
Alerts:
  SchedulingIntervalInDays: 3
  FirstRunTime: "2025-07-01T00:00:00"

Storage:
  LocalStorageDir: "./ld"
  ProdStorageDir: "/pd"
"""
    cfg_file = tmp_path / "config.yml"
    cfg_file.write_text(content, encoding="utf-8")

    with pytest.raises(ValidationError):
        Config.from_yml(cfg_file)
