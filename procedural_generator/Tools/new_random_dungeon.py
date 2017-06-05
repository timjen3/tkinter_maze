from TkComponents.grid import GridBox
import random


def get_two_random_tuples(xlim, ylim):
	t_1 = (random.randint(0, xlim-1), random.randint(0, ylim-1))
	t_2 = None
	while True:
		t_2 = (random.randint(0, xlim-1), random.randint(0, ylim-1))
		if t_2 != t_1:
			break
	return t_1, t_2


class NewRandomDungeon(GridBox):
	def __init__(self, master, height, width):
		self.master = master
		self.height = height
		self.width = width
		stairwells = get_two_random_tuples(width, height)
		super().__init__(master=master, height=height, width=width, up=stairwells[0], down=stairwells[1])
		self.rows[stairwells[0][1]].columns[stairwells[0][0]].set("/")
		self.rows[stairwells[1][1]].columns[stairwells[1][0]].set("\\")
		self.make_path()

	def init_player(self, x, y):
		self.place_player(x, y)

	def make_path(self):
		"""Initiates and maintains path finding until exit is found."""
		visited = []
		blacklist = []
		jump_location = (self.up[0], self.up[1])
		while True:
			this_path = []
			if self.blaze_trail(jump_location[0], jump_location[1], visited, blacklist, this_path):
				return
			while True:
				random_jump_location_index = random.randint(0, len(visited) - 1)
				jump_location = visited[random_jump_location_index]
				if jump_location not in blacklist:
					break

	def blaze_trail(self, x, y, visited, blacklist, this_path):
		if self.rows[y].columns[x].get() == "X":
			self.rows[y].columns[x].set("_")
		visited += [(x, y)]
		this_path += [(x, y)]
		potential_targets = [
			(x+1, y),
			(x-1, y),
			(x, y+1),
			(x, y-1)
		]
		valid_locations = [t for t in potential_targets if (0 <= t[0] <= self.width - 1 and 0 <= t[1] <= self.height - 1)]
		new_locations = [t for t in valid_locations if t not in this_path]
		if self.down in potential_targets:
			return True
		# If only one option left we will be taking it now so never come here again.
		if len(new_locations) == 1:
			blacklist.append((x, y))
		if len(new_locations) > 0:
			rand_list_index = random.randint(0, len(new_locations)-1)
			new_x, new_y = new_locations[rand_list_index]
			if self.blaze_trail(new_x, new_y, visited, blacklist, this_path):
				return True  # End recursive function
