from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class ShikiOrganizer(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark


def main():
    app = ShikiOrganizer()
    app.run()
