# sexp
# Copyright (C) 2011 David Capello
#
# This file is part of ErgoSublime, a port of
# ErgoEmacs functionality to Sublime Text.
# http://github.com/dacap/ErgoSublime
#
# History of changes:
# Version 0.1 - Initial version

import sublime, sublime_plugin


# gasg fd s fd( saf s" f das fds a " f dsfdsa df a)

def is_blank_char(chr):
    if chr == " ": return True
    if chr == "\n": return True
    if chr == "\r": return True
    if chr == "\t": return True
    return False

def is_sexp_char(chr):
    if chr >= "0" and chr <= "9": return True
    if chr >= "a" and chr <= "z": return True
    if chr >= "A" and chr <= "Z": return True
    if chr >= "_": return True
    return False

def get_next_char(view, pt, forward):
    if forward:
        return view.substr(sublime.Region(pt, pt+1))
    else:
        return view.substr(sublime.Region(pt-1, pt))

def move_point_by_sexp(view, pt, forward):
    in_sexp = False
    nested = 0
    was_nested = False
    while True:
        char = get_next_char(view, pt, forward)

        if not nested:
            if not in_sexp and nested == 0 and is_blank_char(char):
                pass
            elif not in_sexp and char == "(" or char == "[" or char == "{":
                if not forward:
                    break
                nested += 1
                in_sexp = True
            elif not in_sexp and char == ")" or char == "]" or char == "}":
                if forward:
                    break
                nested -= 1
                in_sexp = True
            elif not in_sexp and not is_sexp_char(char):
                pass
            elif in_sexp and is_sexp_char(char):
                pass
            elif is_sexp_char(char):
                in_sexp = True
            else:
                break
        else:
            if char == "(" or char == "[" or char == "{":
                nested += 1
            elif char == ")" or char == "]" or char == "}":
                nested -= 1

        if nested != 0:
            was_nested = True

        if forward:
            pt += 1
            if pt >= view.size():
                pt = view.size()
                break
        else:
            pt -= 1
            if pt <= 0:
                pt = 0
                break

        if in_sexp and nested == 0 and was_nested:
            break

    return pt

class MoveBySexpCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward, extend):
        pt = self.view.sel()[0].b
        pt2 = move_point_by_sexp(self.view, pt, forward)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt2, pt2))

class ForwardSexpCommand(sublime_plugin.TextCommand):
    def run(self, edit, extend = False):
        self.view.run_command('move_by_sexp', { "forward": True, "extend": extend })

class BackwardSexpCommand(sublime_plugin.TextCommand):
    def run(self, edit, extend = False):
        self.view.run_command('move_by_sexp', { "forward": False, "extend": extend })

class MarkSexpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        pt1 = self.view.sel()[0].begin()
        pt2 = self.view.sel()[0].end()
        pt2 = move_point_by_sexp(self.view, pt2, True)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt1, pt2))
