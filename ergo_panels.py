# ergo_panels
# Copyright (C) 2011 David Capello
#
# This file is part of ErgoSublime, a port of
# ErgoEmacs functionality to Sublime Text.
# http://github.com/dacap/ErgoSublime
#
# History of changes:
# Version 0.1 - Initial version

import sublime, sublime_plugin

class CloseEmptyGroups:
    pass

class DeleteEmptyGroupsOnClose(sublime_plugin.EventListener):
    def on_close(self, view):
        pass

class DeleteOtherWindowsCommand(sublime_plugin.WindowCommand):
    def run(self):
        # Collect  all clones
        views = dict()
        for view in self.window.views():
            #if view.get_group() != self.window.active_group():
            views[view.buffer_id()] = view
        #for view in self.window.active_group().views():
            #pass
        self.window.set_layout(dict())

class SplitWindowCommand(sublime_plugin.WindowCommand):
    def do(self,stripkey,i1,i2,j1,j2):
        pos = self.window.active_view().viewport_position()
        sel = self.window.active_view().sel()

        active = self.window.active_group()
        newgroup = active+1

        layout = self.window.get_layout()
        print(layout)

        # Insert the new row or col
        layout[stripkey].insert(newgroup, (layout[stripkey][active]+layout[stripkey][active+1])/2)

        cells = layout["cells"]

        # Insert the new cell
        cell = list(cells[active])
        cell[i1] += 1
        cell[i2] += 1
        cells.insert(newgroup, cell)

        # TODO fix this code, cells should be regenerated from scratch
        for i in range(0, len(cells)-1):
            if i != newgroup:
                if cells[i][i1] > cell[i1]:
                    cells[i][i1] = cells[i][i1] + 1
                if cells[i][i2] > cell[i2]:
                    cells[i][i2] = cells[i][i2] + 1

        self.window.set_layout(layout)
        print(layout)

        self.window.run_command("clone_file")
        self.window.run_command("move_to_group", {"group": newgroup})

        newview = self.window.active_view()
        newview.set_viewport_position(pos)
        newview.sel().clear()
        newview.sel().add_all(sel)

class SplitWindowVerticallyCommand(SplitWindowCommand):
    def run(self):
        self.do("rows",1,3,0,2)

class SplitWindowHorizontallyCommand(SplitWindowCommand):
    def run(self):
        self.do("cols",0,2,1,3)

class MoveCursorNextPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        group = self.window.active_group()+1
        if group == self.window.num_groups():
            group = 0
        self.window.focus_group(group)

class MoveCursorPreviousPaneCommand(sublime_plugin.WindowCommand):
    def run(self):
        group = self.window.active_group()-1
        if group < 0:
            group = self.window.num_groups()-1
        self.window.focus_group(group)
