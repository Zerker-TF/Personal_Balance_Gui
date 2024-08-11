import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime, date


def create_savings_window(root):

    style = ttk.Style(root)
    style.theme_use("forest-dark")

    lista_ahorros = ["test"]
    
    # Frames

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True,side="top")
    frame.pack_propagate(True)
    
    widgets_frame1 = ttk.LabelFrame(frame, text="Ingresar")
    widgets_frame1.grid(row=0, column=0, padx=20, pady=20, sticky="nw")
    
    widgets_frame2 = ttk.LabelFrame(widgets_frame1, text="Retirar")
    widgets_frame2.grid(row=5, column=0, sticky="ew")
    
    charts_container = ttk.Frame(frame)
    charts_container.grid(row=1, column=0, columnspan=4,rowspan=2, padx=5, pady=5, sticky="nsew")
    
    canvas_scroll = tk.Canvas(charts_container)
    scrollbar = ttk.Scrollbar(charts_container, orient="vertical", command=canvas_scroll.yview)
    canvas_scroll.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas_scroll.pack(side="left", fill="both", expand=True)

    charts_frame = ttk.Frame(canvas_scroll)
    canvas_scroll.create_window((0, 0), window=charts_frame, anchor="nw")
    
    visual_frame = ttk.Frame(frame)
    visual_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    
    visual_frame_buttons = ttk.Frame(visual_frame)
    visual_frame_buttons.grid(row=0,column=0,sticky="w")
    
    frame.columnconfigure(1, weight=15)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)
    visual_frame.columnconfigure(0, weight=1)
    visual_frame.rowconfigure(2, weight=1)
    
    # Widgets
    
    ahorro_select = ttk.Combobox(widgets_frame1, values=["Nuevo Ahorro"])
    ahorro_select.insert(0, "Seleccionar ahorro")
    ahorro_select.current(0)

    ahorro_amount = ttk.Entry(widgets_frame1)
    ahorro_amount.insert(0, "Ingrese el monto a reservar")
    ahorro_amount.bind("<FocusIn>", lambda e: ahorro_amount.delete('0', 'end'))
    
    ahorro_final = ttk.Entry(widgets_frame1)
    ahorro_final.insert(0, "Objetivo")
    ahorro_final.bind("<FocusIn>", lambda e: ahorro_final.delete('0', 'end'))
    
    new_savings_button = ttk.Button(widgets_frame1, text="Guardar")
    
    separator = ttk.Separator(widgets_frame1)
    
    ahorro_select2 = ttk.Combobox(widgets_frame2, values=lista_ahorros)
    ahorro_select2.insert(0, "Seleccionar ahorro")
    
    ahorro_amount2 = ttk.Entry(widgets_frame2)
    ahorro_amount2.insert(0, "Ingrese el monto a retirar")
    ahorro_amount2.bind("<FocusIn>", lambda e: ahorro_amount2.delete('0', 'end'))
   
    savings_retirar = ttk.Button(widgets_frame2, text="Retirar")
    separator2 = ttk.Separator(widgets_frame2)

    # Top side widget placement

    ahorro_select.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
    ahorro_amount.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    ahorro_final.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    new_savings_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    separator.grid(row=4, column=0, padx=(10, 10), pady=5, sticky="ew")

    ahorro_select2.grid(row=0, column=0, padx=5, pady=5, sticky="ew") 
    ahorro_amount2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    savings_retirar.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
    separator2.grid(row=4, column=0, padx=(20, 10), pady=10, sticky="ew")

    # Scrollable charts widgets
    
    ahorro_table = ttk.Combobox(visual_frame_buttons, values=lista_ahorros)
    ahorro_table.insert(0, "Seleccionar ahorro")
    ahorro_table.grid(row=0, column=0, padx=0.5, pady=2, sticky="w")

    table_button = ttk.Button(visual_frame_buttons, text="Ver Tabla")
    table_button.grid(row=0, column=1, padx=0.5, pady=2, sticky="w")

    columns = ("Fecha", "Monto Ahorrado", "Objetivo")
    treeview = ttk.Treeview(visual_frame, columns=columns, show="headings")
    treeview.column("Fecha", width=100, anchor="center")
    treeview.column("Monto Ahorrado", width=100, anchor="center")
    treeview.column("Objetivo", width=100, anchor="center")
    treeview.heading("Fecha", text="Fecha", anchor="center")
    treeview.heading("Monto Ahorrado", text="Monto Ahorrado", anchor="center")
    treeview.heading("Objetivo", text="Objetivo", anchor="center")
    treeview.grid(row=2, column=0, columnspan=2, padx=5, sticky="nsew")
    treeview.columnconfigure(0,weight=1)

   