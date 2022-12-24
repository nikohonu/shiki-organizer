import json

from shiki_organizer.gui.ui.settings_tab import Ui_SettingsTab
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QValidator
from shiki_organizer.settings import Settings


class SettingsTab(QWidget, Ui_SettingsTab):
    def __init__(self):
        super(SettingsTab, self).__init__()
        self.setupUi(self)
        self.settings = Settings()
        if self.settings.github_token:
            self.github_token.setText(self.settings.github_token)
        self.github_token.editingFinished.connect(self.save)
        self.github_token.setValidator(GithubTokenValidator())

    def save(self):
        self.settings.github_token = self.github_token.text()


class GithubTokenValidator(QValidator):
    def validate(self, string, index):
        if len(string) > 40:
            state = QValidator.Invalid
        elif len(string) < 40:
            state = QValidator.Intermediate
        else:
            state = QValidator.Acceptable
        return (state, string, index)
