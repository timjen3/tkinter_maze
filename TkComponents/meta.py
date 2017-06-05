from tkinter import *


class MetaBar(Frame):
	def __init__(self, master):
		super().__init__(master)
		self.vars = [
			StringVar(),
			StringVar()
		]
		self.widgets = [
			Label(self, textvariable=self.vars[0]),
			Label(self, textvariable=self.vars[1])
		]
		self.widgets[0].grid(row=0, column=0)
		self.widgets[1].grid(row=0, column=1)
		self.vars[0].set("0")
		self.vars[1].set("")

	def change_floor(self, current, furthest):
		self.vars[0].set("Floor: {}".format(current))
		self.vars[1].set("Record: {}".format(furthest))
