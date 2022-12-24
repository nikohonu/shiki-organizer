from pathlib import Path

from appdirs import user_data_dir, user_config_dir


def get_user_data_dir():
    return Path(user_data_dir("shiki-organizer", "Niko Honu"))


def get_user_config_dir():
    return Path(user_config_dir("shiki-organizer", "Niko Honu"))
