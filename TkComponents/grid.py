from tkinter import *
from enum import Enum


class Direction(Enum):
	N = (0, -1)
	S = (0, 1)
	W = (-1, 0)
	E = (1, 0)


class GridRow(Frame):
	def __init__(self, master, width):
		super().__init__(master)
		self._cols = []
		self.columns = []
		for i in range(0, width):
			self.columns.append(StringVar())
			self._cols.append(Label(self, textvariable=self.columns[i]))
			self.columnconfigure(i, minsize=20)
			self._cols[i].grid(row=0, column=i)
			self.columns[i].set("X")


class GridBox(Frame):
	def __init__(self, master, height, width, up=None, down=None, grid_data=None):
		super().__init__(master)
		self.rows = []
		self.player_coordinates = None
		self.nav_fun = None
		self.height = height
		self.width = width
		if not grid_data:
			self.up = up
			self.down = down
			for i in range(0, height):
				self.rows.append(GridRow(self, width))
				self.rows[i].grid(row=i, column=0)
		else:
			for irow, vals in enumerate(grid_data):
				self.rows.append(GridRow(self, len(vals)))
				for icol, v in enumerate(vals):
					self.rows[irow].columns[icol].set(v)
					if v == "/":
						self.up = (icol, irow)
					elif v == "\\":
						self.down = (icol, irow)
				self.rows[irow].grid(row=irow, column=0)

	@property
	def grid_data(self):
		my_data = []
		for r in self.rows:
			my_data.append([
				c.get() for c in r.columns
			])
		my_data[self.up[1]][self.up[0]] = "/"
		my_data[self.down[1]][self.down[0]] = "\\"
		return my_data

	def move_if_valid(self, command):
		new_x = self.player_coordinates[0] + command.value[0]
		new_y = self.player_coordinates[1] + command.value[1]
		good_horizontal = 0 <= new_x <= self.width - 1
		good_vertical = 0 <= new_y <= self.height - 1
		if good_horizontal and good_vertical:
			new_location = self.rows[new_y].columns[new_x]
			if not new_location.get() == "X":
				if self.player_coordinates == self.up:
					self.rows[self.player_coordinates[1]].columns[self.player_coordinates[0]].set("/")
				elif self.player_coordinates == self.down:
					self.rows[self.player_coordinates[1]].columns[self.player_coordinates[0]].set("\\")
				else:
					self.rows[self.player_coordinates[1]].columns[self.player_coordinates[0]].set("_")
				if (new_x, new_y) in (self.up, self.down):
					self.nav_fun([0, 1, 2, 3, 4])
				else:
					self.nav_fun([0, 1, 2, 3])
				self.place_player(new_x, new_y)

	def place_player(self, x, y):
		self.player_coordinates = (x, y)
		self.rows[self.player_coordinates[1]].columns[self.player_coordinates[0]].set("O")
