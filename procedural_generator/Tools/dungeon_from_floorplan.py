from TkComponents.grid import GridBox
import random


class Dungeon(GridBox):
	def __init__(self, master, height, width, floor_plan):
		self.master = master
		self.height = height
		self.width = width
		super().__init__(master=self.master, grid_data=floor_plan, height=height, width=width)

	def init_player(self, x, y):
		self.place_player(x, y)
