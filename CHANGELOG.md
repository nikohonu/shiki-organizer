# Changelog

# Changelog

## [Unreleased]
### Added
- Option for show or hide archived tasks.

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
