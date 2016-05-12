import sublime, sublime_plugin
import subprocess

class Entry(object):
	def __init__(self, ctags_output):
		ctags_split = ctags_output.split("\t")
		itemtypes = {
			"c": "Class",
			"m": "Method",
		}
		itemtype = itemtypes.get(ctags_split[3], "Unknown Type")

		self.items = [ctags_split[0], itemtype]
		self.linenum = int(ctags_split[2].strip(';"'))

class CtagsOutlineCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if self.view.file_name() == None:
			return
		else:
			ctags_output = subprocess.check_output(["/usr/local/bin/ctags", "-n", "-f", "-", self.view.file_name()], stderr=subprocess.STDOUT).decode("utf-8")
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
			print(self.linenums)

	def on_selected(self, index):
		pass

	def on_highlighted(self, index):
		row = self.entries[index].linenum
		col = 0
		pt = self.view.text_point(row, col)
		print(pt)
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(pt, pt))
		self.view.show_at_center(pt)
