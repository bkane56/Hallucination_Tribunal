import os

import pytest

from src.core.config import get_settings
from src.core.dependencies import reset_provider_cache


@pytest.fixture(autouse=True)
def test_environment() -> None:
    os.environ["APP_ENV"] = "test"
    get_settings.cache_clear()
    reset_provider_cache()
    yield
    get_settings.cache_clear()
    reset_provider_cache()
