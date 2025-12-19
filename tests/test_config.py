import os
from aldi_hoc_companion.core.config import Settings


def test_settings_loads_with_required_env():
    # Set ONLY required env variables
    os.environ["DB_NAME"] = "aldi_rag_local"
    os.environ["DB_USER"] = "aldi_rag_user"
    os.environ["DB_PASSWORD"] = "123456"

    # Create settings instance
    settings = Settings()

    # Basic sanity checks
    assert settings.db_name == "aldi_rag_local"
    assert settings.db_user == "aldi_rag_user"
    assert settings.db_password == "123456"
    assert settings.db_host == "localhost"   # default
    assert settings.db_port == 5432          # default
