from tkinter import *
from .grid import Direction
from copy import deepcopy
from procedural_generator.Tools import data_access


def move(dm, dir):
	return lambda: dm.current_dungeon.move_if_valid(dir)


class NavBox(Frame):
	def __init__(self, master, dm, update_floor_fun):
		super().__init__(master)
		self.dm = dm
		self.buttons = list()
		self.floors = data_access.load_data()
		self.floor = 0
		self.active = [0, 1, 2, 3, 4]
		self.update_floor_fun = update_floor_fun
		self.buttons.append(Button(self, text="North", command=move(self.dm, Direction.N)))
		self.buttons.append(Button(self, text="West", command=move(self.dm, Direction.W)))
		self.buttons.append(Button(self, text="East", command=move(self.dm, Direction.E)))
		self.buttons.append(Button(self, text="South", command=move(self.dm, Direction.S)))
		self.buttons.append(Button(self, text="Climb", command=dm.get_dungeon_regeneration_function(self.mod_me)))
		self.buttons[0].grid(row=0, column=1)
		self.buttons[1].grid(row=1, column=0)
		self.buttons[2].grid(row=1, column=2)
		self.buttons[3].grid(row=2, column=1)
		self.buttons[4].grid(row=1, column=1)
		self.nav_dungeon(target_floor=0)
		self.master.bind_all('<Key>', self.key)

	def mod_me(self, active):
		self.active = active
		for i, b in enumerate(self.buttons):
			if i in active:
				self.buttons[i].config(state="normal")
			else:
				self.buttons[i].config(state="disabled")

	def nav_dungeon(self, target_floor):
		"""Either loads or generates dungeon floor depending if new."""
		if len(self.floors) >= target_floor + 1:
			print("loading...")
			self.dm.load_dungeon(self.floors[target_floor], self.mod_me)
		else:
			print("generating...")
			self.dm.get_dungeon_regeneration_function(self.mod_me)()
			self.floors.append(deepcopy(self.dm.current_dungeon.grid_data))
		self.floor = target_floor
		self.update_floor_fun((self.floor + 1), len(self.floors))

	def key(self, event):
		if event.keysym == "Up":
			if 0 in self.active:
				move(self.dm, Direction.N)()
		elif event.keysym == "Left":
			if 1 in self.active:
				move(self.dm, Direction.W)()
		elif event.keysym == "Right":
			if 2 in self.active:
				move(self.dm, Direction.E)()
		elif event.keysym == "Down":
			if 3 in self.active:
				move(self.dm, Direction.S)()
		elif event.keysym == "space":
			if 4 in self.active:
				if self.dm.current_dungeon.player_coordinates == self.dm.current_dungeon.down:
					target_floor = self.floor + 1
				else:
					if self.floor == 0:
						return
					target_floor = self.floor - 1
				self.nav_dungeon(target_floor)
		elif event.keysym == "Escape":
			data_access.save_data(self.floors)
			self.master.quit()
