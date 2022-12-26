# Changelog

# Changelog

## [Unreleased]

### Added

- Settings tab.
- Repository tab.
- Add, delete and modify task.

### Changed
- Improve task tables.

## [0.8.0] - 2022-12-24

### Added

- Period, archived, uuid, root and duration option for so tree command.
- uuid option for so ls
- Duration in so-interval ls command.
- Period option for so-interval ls command.
- Interval tab in GUI with equivalent of ls, modify, delete and add commands.
- Sorting to the table on the Interval tab.

### Removed

- Divider, today_duration, score, today_score for tasks.
- so today command.

## [0.7.0] - 2022-12-23

### Added

- so-repository modify command.
- so-repository pull command show info about its own work.
- Basic GUI with "Today" and "Tasks" tabs ([#13](https://github.com/nikohonu/shiki-organizer/issues/13), [#18](https://github.com/nikohonu/shiki-organizer/issues/18)).
- Start, stop, done commands for gui.
- Show new scheduled date when user complete recurring tasks.

### Changed

- Reverse tree sorting by score.

### Fixed

- so-repository ls command.
- so-interval command ([#17](https://github.com/nikohonu/shiki-organizer/issues/17)).

## [0.6.0] - 2022-12-13

### Added

- Option for show or hide archived tasks.
- pygithub dependency.
- repository-add command.
- repository-ls command.
- repository-delete command.
- repository-pull command.
- tree command.
- done command can close issue.
- split commands by different entry points.
- today option for tree command.

### Changed

- return the ability to set a parent for a task (for add command).

### Removed

- projects command.
- tags command.

## [0.5.0] - 2022-12-05

### Added

- click dependency.
- colorama dependency.
- status command.
- modify command.
- normalize command.
- interval-list command.
- modify-interval command.
- delete-interval command.
- ls command.
- tags command.
- projects command.
- today command.

### Changed

- Replace "click" with "argparse".
- Develop new database model.
- Update add command.
- Del command renamed to delete.
- Update delete command.
- Update start command.
- Update stop command.
- Update done command.
- Update status command.
- Update interval-list command.
- Update interval-modify command.
- Update interval-delete command.

### Fixed

- Archived task with parent task do not break the "tree" command

### Removed

- Tree command.
- termcolor dependency.

## [0.4.0] - 2022-11-26

### Added

- actions.py for sharing commands between GUI and CLI.

### Changed

- Update dependencies.
- Change folder structure.
- Develop new database model.
- Update add command.
- Update done(do) command.
- Update edit command.
- Update start command.
- Update stop command.
- Update tree command.
- Update del command.
- Update review command.

### Removed

- Category.
- Field.
- List command.
