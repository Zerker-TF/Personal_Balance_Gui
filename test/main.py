import tkinter as tk
from tkinter import ttk
import gui
import graphs

root = tk.Tk()
root.title("Balance personal")
root.minsize(1100,356)

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

frame = ttk.Frame(root)
frame.pack()

gui_widgets = gui.create_widgets(frame)
graph_frame = graphs.create_graph_frame(frame)

root.mainloop()