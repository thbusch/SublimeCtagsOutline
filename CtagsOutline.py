import platform
import subprocess

import sublime, sublime_plugin

class Entry(object):
	def __init__(self, ctags_output):
		ctags_split = ctags_output.split("\t")
		itemname = ctags_split[0]
		del ctags_split[0]
		del ctags_split[0]
		self.linenum = int(ctags_split[0].strip(';"'))
		del ctags_split[0]

		itemtypename = ctags_split[0]
		del ctags_split[0]
		itemtypes = {
			"c": "Class",
			"m": "Method",
		}
		itemtypename = itemtypes.get(itemtypename, "Unknown Type")

		self.items = [itemname, itemtypename]

class CtagsOutlineCommand(sublime_plugin.TextCommand):
	ctags_command = "/usr/local/bin/ctags" if (platform.system() == "Darwin") else "ctags"

	def run(self, edit):
		if self.view.file_name() == None:
			return
		else:
			ctags_output = subprocess.check_output([self.ctags_command, "-n", "-f", "-", self.view.file_name()], stderr=subprocess.STDOUT).decode("utf-8")
			res = ctags_output.splitlines()
			self.entries = []
			for item in res:
				self.entries.append(Entry(item))
			self.entries = sorted(self.entries, key=lambda item: item.linenum)
			entries = []
			for entry in self.entries:
				entries.append(entry.items)
			print(entries)
			self.view.window().show_quick_panel(entries, self.on_selected, sublime.MONOSPACE_FONT, 0, self.on_highlighted)

	def on_selected(self, index):
		pass

	def on_highlighted(self, index):
		row = self.entries[index].linenum
		col = 0
		pt = self.view.text_point(row, col)
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(pt, pt))
		self.view.show_at_center(pt)
