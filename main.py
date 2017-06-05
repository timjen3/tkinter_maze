if __name__ == "__main__":
	from tkinter import *
	from TkComponents.meta import MetaBar
	from TkComponents.nav import NavBox
	from procedural_generator.simple_flat import DungeonFactory

	master = Tk()
	meta = MetaBar(master)
	meta.grid(row=0)
	df = DungeonFactory(
		master=master,
		height=12,
		width=20
	)
	df.grid(row=1)
	nav = NavBox(master, df, meta.change_floor)
	nav.grid(row=2)
	master.mainloop()
