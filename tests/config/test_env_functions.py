import pytest
from config.config import check_flag_set, get_env_var

def test_get_env_var_missing_and_present(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("MISSING_VAR", raising=False)
    with pytest.raises(ValueError, match="Environment variable MISSING_VAR is not set"):
        get_env_var("MISSING_VAR")

    monkeypatch.setenv("MISSING_VAR", "some_value")
    assert get_env_var("MISSING_VAR") == "some_value"

def test_check_flag_set(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("SOME_FLAG", raising=False)
    assert not check_flag_set("SOME_FLAG")
    monkeypatch.setenv("SOME_FLAG", "1")
    assert check_flag_set("SOME_FLAG")
    monkeypatch.setenv("SOME_FLAG", "2")
    assert check_flag_set("SOME_FLAG")
