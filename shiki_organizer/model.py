import datetime as dt
import sqlite3
from pathlib import Path

from appdirs import user_config_dir, user_data_dir

database_path = Path(user_data_dir("shiki-organizer", "Niko Honu")) / "database.db"
con = sqlite3.connect(database_path)
cur = con.cursor()


def build_dict(data, keys):
    result = []
    for row in data:
        d = {}
        for i, key in enumerate(keys):
            d[key] = row[i]
        result.append(d)
    return result
