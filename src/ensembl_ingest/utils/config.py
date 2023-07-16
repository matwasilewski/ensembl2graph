import datetime
import os
import time
from functools import lru_cache
from typing import Dict, Optional, Union

import pkg_resources
import tomlkit
from pydantic_settings import BaseSettings


def _get_project_meta(name: str = 'unknown') -> Dict:
    """
    Get name and version from pyproject metadata.
    """
    version = "unknown"
    description = ""
    try:
        with open('./pyproject.toml') as pyproject:
            file_contents = pyproject.read()
        parsed = dict(tomlkit.parse(file_contents))['tool']['poetry']
        name = parsed['name']
        version = parsed.get('version', 'unknown')
        description = parsed.get('description', '')
    except FileNotFoundError:
        # If cannot read the contents of pyproject directly (i.e. in Docker),
        # check installed package (there is a risk that this could be stale
        # though):
        try:
            distribution = pkg_resources.get_distribution(name)
            name = distribution.project_name
            version = distribution.version
        except pkg_resources.DistributionNotFound:
            pass
    return {"name": name, "version": version, "description": description}


PKG_META = _get_project_meta()


class Settings(BaseSettings):
    """
    Settings. Environment variables always take priority over values loaded
    from the dotenv file.
    """

    current_timestamp = int(time.time())

    # Meta
    APP_NAME: str = str(PKG_META['name'])
    APP_VERSION: str = str(PKG_META['version'])
    PUBLIC_NAME: str = APP_NAME
    DESCRIPTION: str = str(PKG_META['description'])

    # Logger
    LOGGER_NAME: str = "ensembl_ingest"
    LOG_LEVEL: str = "info"
    VERBOSE_LOGS: Union[bool, int, str] = True
    JSON_LOGS: Union[bool, int, str] = False
    LOG_DIR: str = os.sep.join(
        ["logs", f"{current_timestamp}-{LOGGER_NAME}-{LOG_LEVEL}.log"]
    )
    SYSLOG_ADDR: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        secrets_dir = "secrets"


@lru_cache()
def get_settings() -> Settings:
    return Settings(_env_file=f"{os.getcwd()}/.env")


settings = get_settings()
