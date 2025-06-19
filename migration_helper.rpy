###############################################################################
# MigrationHelper for Ren'Py
# Copyright (c) 2025 Mispeled
#
# Author: Mispeled (https://github.com/snaplemouton)
#
# Description:
#     A utility library for Ren'Py visual novels to handle migration of variables
#     across save versions. Stores variables outside of the standard save-pickling
#     system for safe migration and future-proofing, without polluting the global
#     namespace.
#
# Features:
#     - Save/load custom variables as JSON-compatible pseudo-vars.
#     - Automatic migration of pseudo-vars into new global variables when upgrading.
#     - Designed for easy plug-and-play in any Ren'Py project.
#
# Usage:
#     See the included functions and screens for integrating migration into
#     your game’s menus.
###############################################################################
init python:
    import renpy.store as store

    class MigrationHelper(object):
        def __init__(self):
            self._vars = {}

        def set_var(self, name, value):
            self._vars[name] = value

        def get_var(self, name, default=None):
            return self._vars.get(name, default)

        def remove_var(self, name):
            if name in self._vars:
                del self._vars[name]

        def all_vars(self):
            return dict(self._vars)

        def clear(self):
            self._vars.clear()

    migration_helper = MigrationHelper()

    def migration_json_callback(d):
        for k, v in migration_helper._vars.items():
            d["psv_" + k] = v

    config.save_json_callbacks.append(migration_json_callback)

init python:
    import renpy.store as store
    import time

    def migrate_current_save_vars(slot):
        slotjson = renpy.slot_json(slot)
        if slotjson is None:
            renpy.log("No JSON for slot: {}".format(slot))
            return

        migration_helper.clear()

        migrated_count = 0
        for k, v in slotjson.items():
            if k.startswith("psv_"):
                varname = k[4:]
                renpy.log("Varname: {}".format(varname))
                if hasattr(store, varname):
                    setattr(store, varname, v)
                    migrated_count += 1
                else:
                    migration_helper.set_var(varname, v)

        renpy.save(slot)
        renpy.log("Migration done for slot {}: {} variables migrated.".format(slot, migrated_count))

    def migrate_logic(slot):
        migrate_current_save_vars(slot)
        renpy.hide_screen("migrate_slots")

screen migrate_slots():
    fixed:
        text "Migrate save file" xalign 0.5 size 48 yoffset 100
        grid gui.file_slot_cols gui.file_slot_rows:
            style_prefix "slot"
            xalign 0.5
            yalign 0.5
            spacing gui.slot_spacing

            for i in range(gui.file_slot_cols * gui.file_slot_rows):
                $ slot = i + 1
                $ slotnumber = FileSlotName(slot, gui.file_slot_cols * gui.file_slot_rows)
                $ slotname = str(math.floor(int(slotnumber) / 6) + 1) + "-" + str(int(slotnumber) % 6)

                button:
                    action Function(migrate_logic, slotname)

                    has vbox

                    add FileScreenshot(slot) xalign 0.5

                    text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                        style "slot_time_text"

                    text FileSaveName(slot):
                        style "slot_name_text"

        vbox:
            style_prefix "page"
            xalign 0.5
            yalign 1.0

            hbox:
                xalign 0.5
                spacing gui.page_spacing

                textbutton _("<") action FilePagePrevious()
                key "save_page_prev" action FilePagePrevious()

                if config.has_autosave:
                    textbutton _("{#auto_page}A") action FilePage("auto")

                if config.has_quicksave:
                    textbutton _("{#quick_page}Q") action FilePage("quick")

                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)

                textbutton _(">") action FilePageNext()
                key "save_page_next" action FilePageNext()
        
default some_value = 0
label migration_helper_samples():
    $ renpy.say(None, "Our global some_value is: " + str(some_value))
    $ migration_helper.set_var("some_value", 1)
    $ migration_helper.set_var("some_other_value", 2)
    "We just added some_value with a value of 1 to our Migration Helper."
    $ renpy.say(None, "Our global some_value is still: " + str(some_value))
    "Save your game."
    show screen migrate_slots
    "Now migrate the save we just did to update our global some_value with our saved pseudo_save_value"
    $ renpy.say(None, "Our global some_value is now: " + str(some_value))
    $ log_all_save_json()

init python:
    def log_all_save_json():
        slots = renpy.list_slots()
        renpy.log("==== Save File JSON Dump ====")
        for slot in slots:
            try:
                slotjson = renpy.slot_json(slot)
                if slotjson is None:
                    renpy.log("[{}] Slot is empty or not found.".format(slot))
                else:
                    renpy.log("[{}]".format(slot))
                    for k, v in slotjson.items():
                        renpy.log("    {}: {!r}".format(k, v))
            except Exception as e:
                renpy.log("[{}] Error reading slot: {}".format(slot, e))
        renpy.log("==== End of Dump ====")
