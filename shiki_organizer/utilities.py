from pathlib import Path

from appdirs import user_data_dir


def get_user_data_dir():
    return Path(user_data_dir("shiki-organizer", "Niko Honu"))