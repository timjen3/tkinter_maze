from .Tools.new_random_dungeon import NewRandomDungeon
from .Tools.dungeon_from_floorplan import Dungeon


class DungeonFactory:
	def __init__(self, master, height, width):
		self._grid_row = None
		self.master = master
		self.height = height
		self.width = width
		self.start_location = None
		self.end_location = None
		self.current_dungeon = None

	def grid(self, row):
		self._grid_row = row

	def load_dungeon(self, floor_plan, mod_fun):
		is_descending = True
		if self.current_dungeon is not None:
			is_descending = self.current_dungeon.player_coordinates == self.current_dungeon.down
			for child in self.current_dungeon.winfo_children():
				child.destroy()
		self.current_dungeon = Dungeon(
			master=self.master,
			height=self.height,
			width=self.width,
			floor_plan=floor_plan
		)
		self.current_dungeon.grid(row=self._grid_row)
		if is_descending:
			self.current_dungeon.init_player(self.current_dungeon.up[0], self.current_dungeon.up[1])
		else:
			self.current_dungeon.init_player(self.current_dungeon.down[0], self.current_dungeon.down[1])
		self.current_dungeon.nav_fun = mod_fun

	def get_dungeon_regeneration_function(self, navigation_callback):
		return lambda: self.get_dungeon(navigation_callback)

	def get_dungeon(self, mod_fun):
		is_descending = True
		if self.current_dungeon is not None:
			is_descending = self.current_dungeon.player_coordinates == self.current_dungeon.down
			for child in self.current_dungeon.winfo_children():
				child.destroy()
		self.current_dungeon = NewRandomDungeon(
			master=self.master,
			height=self.height,
			width=self.width
		)
		self.current_dungeon.grid(row=self._grid_row)
		if is_descending:
			self.current_dungeon.init_player(self.current_dungeon.up[0], self.current_dungeon.up[1])
		else:
			self.current_dungeon.init_player(self.current_dungeon.down[0], self.current_dungeon.down[1])
		self.current_dungeon.nav_fun = mod_fun
