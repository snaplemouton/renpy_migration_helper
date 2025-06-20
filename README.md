# MigrationHelper for Ren’Py
A utility library for Ren’Py that provides future-proof variable migration support.
Created by Mispeled.

## Do not use this library unless you plan on updating it
Migration Helper isn't rollback compliant, therefore using it is not recommended unless you plan on updating the code to make it rollback compliant.
The only way I can personally think of doing it in the current version of Ren'py is by creating a custom rollback system that works in parallel with Ren'py's rollback system.
Which is more work than it's worth. Just use a better Game Engine at that point.

## Features
Migration of variables to new global variables after game updates.

Clean, global-namespace-friendly variable management.

## Why?
Ren’Py only saves variables that exist at the time the game is saved.
If you add new variables to future versions of your game, you can’t recover “old” player choices that weren’t previously saved—unless you future-proof.

MigrationHelper lets you store and migrate variables in a way that:
- Doesn’t clutter your global namespace with unnecessary variables,
- Enables seamless migration when your game or save system changes.

Here's a table comparing other built-in solutions with the Migration Helper:
| Feature                    | `store` (default vars) | `persistent` | `jsondb` | `MultiPersistent` | **Migration Helper**     |
| -------------------------- | ---------------------- | ------------ | -------- | ----------------- | ------------------------ |
| Per-save data              | ✅ Yes                  | ❌ No         | ❌ No     | ❌ No              | ✅ Yes                    |
| Supports rollback          | ✅ Yes                  | ❌ No         | ❌ No     | ❌ No              | ⚠️ No (Needs a lot of work to make it work)     |
| Persistent across sessions | ✅ Yes (per save file)  | ✅ Yes        | ✅ Yes    | ✅ Yes             | ❌ No (cold storage only) |
| Safe for migrating data    | ❌ No                   | ⚠️ Risky     | ⚠️ Risky | ⚠️ Partial        | ✅ Yes                    |
| Version upgrade support    | ❌ No                   | ❌ Manual     | ❌ Manual | ⚠️ Manual         | ⚠️ Built-in (Might need some tweaking)      |

## How It Works
MigrationHelper stores custom variables (with a psv_ prefix) in Ren’Py’s save JSON using config.save_json_callbacks.
When you update your game and add new globals, you can use migrate_current_save_vars(slot) to migrate a specific save slot.
You can use the provided migration screen (see included samples label for example usage) or make your own migration logic.

## Usage
Copy migration_helper.rpy into your /game folder.
Use the provided helper in your code:

```
# Example: set and get a migration-variable
$ migration_helper.set_var("my_flag", 1)
$ some_value = migration_helper.get_var("my_flag", default=0)
```

## License
This code is public domain.  
Do whatever you want with it.  
Credit is appreciated but not required.

## Credits
Written by Mispeled (https://github.com/snaplemouton)
Special thanks to ChatGPT because I'm too lazy to write a README
