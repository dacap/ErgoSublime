# shrink_whitespaces
# Copyright (C) 2011 David Capello
#
# This file is part of ErgoSublime, a port of
# ErgoEmacs functionality to Sublime Text.
# http://github.com/dacap/ErgoSublime
#
# History of changes:
# Version 0.1 - Initial version

import sublime, sublime_plugin

def expand_region_in_white_chars(view, reg):
    a = reg.a
    b = reg.b

    # Expand to the beginning of the line
    while True:
        c = view.substr(sublime.Region(a-1, a))
        if c == " " or c == "\t":
            a -= 1
        else:
            break

    # Expand to the end of the line
    while True:
        c = view.substr(sublime.Region(b+1, b))
        if c == " " or c == "\t":
            b += 1
        else:
            break

    return sublime.Region(a, b)

def expand_region_in_white_lines(view, reg):
    # Cover previous white lines
    while True:
        newreg = expand_region_in_white_chars(view, sublime.Region(reg.a-1, reg.a-1))
        fulllinereg = view.full_line(newreg.a)
        if newreg.a == fulllinereg.a and newreg.b == fulllinereg.b-1:
            reg = reg.cover(fulllinereg)
        else:
            break

    # Cover next white lines
    while True:
        newreg = expand_region_in_white_chars(view, sublime.Region(reg.b, reg.b))
        fulllinereg = view.full_line(newreg.a)
        if newreg.a == fulllinereg.a and newreg.b == fulllinereg.b-1:
            reg = reg.cover(fulllinereg)
        else:
            break

    return reg

class ShrinkWhitespacesCommand(sublime_plugin.TextCommand):
    """Removes whitespaces."""

    def run(self, edit):
        eraselines = False

        sel = self.view.sel()
        regions = []
        for r in self.view.sel():
            newreg = expand_region_in_white_chars(self.view, r)
            fulllinereg = self.view.full_line(newreg.a)
            if newreg.a == fulllinereg.a and newreg.b == fulllinereg.b-1:
                eraselines = True
                newreg = expand_region_in_white_lines(self.view, fulllinereg)

            regions.append(newreg)

        self.view.sel().clear()
        for r in regions:
            self.view.sel().add(r)

        for r in self.view.sel():
            newlines = self.view.substr(r).count('\n')
            if newlines > 1:
                self.view.replace(edit, r, '\n')
            elif not eraselines and r.b - r.a > 1:
                self.view.replace(edit, r, ' ')
            else:
                self.view.erase(edit, r)
