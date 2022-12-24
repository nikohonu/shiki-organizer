import json
from shiki_organizer.paths import get_user_config_dir
from pathlib import Path


class SettingsMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Settings(metaclass=SettingsMeta):
    def __init__(self) -> None:
        self.save_path = get_user_config_dir() / "settings.json"
        self.save_path.parent.mkdir(exist_ok=True, parents=True)
        if self.save_path.exists():
            with self.save_path.open() as file:
                self.data = json.load(file)
        else:
            self.data = {}

    @property
    def github_token(self):
        if "github_token" in self.data:
            return self.data["github_token"]
        return None

    @github_token.setter
    def github_token(self, value):
        self.data["github_token"] = value
        self._save()

    def _save(self):
        with self.save_path.open("w") as file:
            json.dump(self.data, file)
