import platform
import subprocess

import sublime, sublime_plugin

ctags_command = "/usr/local/bin/ctags" if (platform.system() == "Darwin") else "ctags"

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
		self.items = [itemname, itemtypename]

class CtagsOutlineCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		if self.view.file_name() == None:
			return
		else:
			ctags_output = subprocess.check_output([ctags_command, "-n", "-f", "-", "--fields=fKst", self.view.file_name()], stderr=subprocess.STDOUT).decode("utf-8")
			current_line = 0;
			current_line = self.view.rowcol(self.view.sel()[0].a)[0]
			print("%d"%current_line)
			res = ctags_output.splitlines()
			self.entries = []
			for item in res:
				entry = Entry(item)
				if entry.linenum <= current_line:
					selected_entry = len(self.entries)
				self.entries.append(entry)

			self.entries = sorted(self.entries, key=lambda item: item.linenum)
			selected_index = 0
			for entry in self.entries:
				if entry.linenum <= current_line:
					selected_index = self.entries.index(entry)
			entries = []
			for entry in self.entries:
				entries.append(entry.items)
			self.view.window().show_quick_panel(entries, self.on_selected, sublime.MONOSPACE_FONT, selected_index, self.on_highlighted)

	def on_selected(self, index):
		if index == -1:
			self.view.show(self.view.sel()[0].a)
			return
		row = self.entries[index].linenum
		col = 0
		pt = self.view.text_point(row, col)
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(pt))

	def on_highlighted(self, index):
		row = self.entries[index].linenum
		col = 0
		pt = self.view.text_point(row, col)
		self.view.show(pt)
