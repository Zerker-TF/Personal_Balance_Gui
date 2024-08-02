import tkinter as tk
from tkinter import ttk
from widgets import create_widgets
from widgets import create_table

def create_frames(root):
    style = ttk.Style(root)
    root.tk.call("source","forest-light.tcl")
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")
    #main frame
    frame = tk.Frame(root)
    frame.pack()
    
    #Ingresar datos frame
    widgets_frame = ttk.LabelFrame(frame,text="Ingresar Datos")
    widgets_frame.grid(row=0, column=0, padx=20, pady=20)

    
    #Treeview table frame
    treeframe = ttk.Frame(frame)
    treeframe.grid(row=0,column=1,padx=30,pady=5)
 
    
    #Graphs frame
    graphframe = ttk.Frame(frame)
    graphframe.grid(row=1,column=0,columnspan=2)
    treeview, month_select = create_table(treeframe,graphframe,frame,root)
    create_widgets(widgets_frame, treeview, month_select, graphframe, root, frame)
    