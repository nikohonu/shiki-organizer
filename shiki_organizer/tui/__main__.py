from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.geometry import Size
from textual.widget import Widget
from textual.widgets import Button, Checkbox, Footer, Header, Label, Tree

from shiki_organizer.cli.formatter import task_to_str
from shiki_organizer.cli.task import _update_tasks
from shiki_organizer.database import Interval, Task
from shiki_organizer.datetime import period_to_datetime


class TaskTree(Tree):
    DEFAULT_CSS = """
    Tree {
            height: auto;
    }
    """

    def add_children(self, root_node, root_task):
        tasks = sorted(
            Task.select().where((Task.parent == root_task)),
            key=lambda x: x.duration,
            reverse=True,
        )
        for task in tasks:
            node = root_node.add(
                task_to_str(task, False),
                expand=True,
                data={"id": task.id},
            )
            self.add_children(node, task)

    def __init__(self, id=None) -> None:
        super().__init__("Tasks", id=id)
        self.show_root = False
        self.update()

    def update(self):
        self.clear()
        min_start = Interval.select().order_by(Interval.start).get().start
        start = period_to_datetime("all", min_start)
        _update_tasks(start, False)
        self.add_children(self.root, None)


class ShikiOrganizer(App):
    DEFAULT_CSS = """#dl {
            dock: left;
            }
#dr {
            dock: left;
            }

    """
    BINDINGS = [
        ("t", "toggle_dark", "Toggle dark mode"),
        ("d", "done", "Done current task"),
        ("u", "update", "Update tree"),
    ]

    def compose(self) -> ComposeResult:
        # tree: Tree[dict] = Tree("Tasks")
        # tree.root.expand()
        # for task in Task.select():
        # tree.root.add(task.name, expand=True)
        # characters = tree.root.add("Game", expand=True)
        # characters.add_leaf("Drakenguard")
        # characters.add_leaf("Minecraft")
        # characters.add_leaf("Warcraft", data={"test": "test"})
        yield Horizontal(TaskTree(), Checkbox(id="dl"))
        # yield Horizontal(Label("Text"), Checkbox(), id="dl")
        yield Footer()

    def action_done(self):
        print(self.query_one("Tree").cursor_node)

    def action_update(self):
        self.query_one("Tree").update()


def main():
    app = ShikiOrganizer()
    app.run()


if __name__ == "__main__":
    main()
