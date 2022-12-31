import json
import os
from .log_setup import logger
from .version import VERSION  # load version, other modules can access without extra import
from typing import Dict, Optional

### @package environment
#
# Interactions with the environment variables.
#

def load_env(key: str, default: str, config_dict=None) -> str:

    env_value = os.getenv(key)
    conf_val = None
    if isinstance(config_dict, dict):
        conf_val = config_dict.get(key, None)

    if env_value and conf_val:
        logger.info(f"Gained '{key}' from environment and config - preferring env-variable")
        value = env_value
    elif env_value:
        logger.debug(f"Gained '{key}' from environment only, using this value")
        value = env_value
    elif conf_val:
        logger.debug(f"Gained '{key}' from config-file only, using this value")
        value = conf_val
    else:
        value = None

    if key == "TOKEN":
        return value

    if key == "PREFIX":
        if value:
            return value
        else:
            logger.warning(f"Can't load env-variable for: '{key}' - falling back to DEFAULT {key}='{default}'")
            return default

    if value is not None:
        try:
            return value.replace("{PREFIX}", PREFIX)
        except NameError as e:
            logger.error(
                f"Can't replace expressions for: '{key}' {e.__repr__()}.\n"
                f"This happens if a referenced env-variable isn't initiated yet. "
                f"You may wanna change the load order - falling back to DEFAULT {key}='{default}' "
            )
            return default
    logger.warning(f"Can't load env-variable for: '{key}' - falling back to DEFAULT {key}='{default}'")
    return default

def load_conf_file(config_file='./data/config.json') -> Optional[Dict[str, str]]:
    if os.path.isfile(config_file):
        logger.debug(f"Config file '{config_file}' exists, trying to read")
        try:
            with open(config_file, "r") as jsonfile:
                return json.load(jsonfile)

        except OSError:
            logger.warning(f"Can't open or read config file: '{config_file}'")

    else:
        logger.debug(f"No config-file was found under '{config_file}', trying to continue")


cfg_dict = load_conf_file('./data/config.json')

TOKEN = load_env("TOKEN", '', config_dict=cfg_dict)
PREFIX = load_env("PREFIX", "b!", config_dict=cfg_dict)
OWNER_NAME = load_env("OWNER_NAME", "Veriz0wn#5299", config_dict=cfg_dict)  # Veriz0wn#5299
OWNER_ID = int(load_env("OWNER_ID", "986654955115016242", config_dict=cfg_dict))
ACTIVITY_NAME = load_env("ACTIVITY_NAME", f"{PREFIX}help", config_dict=cfg_dict)
