import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import datetime
import main
from data import insert_row, load_data
from table import show_menu, show_chart

# Theme change from dark to light mode
def toggle_mode():
     if theme_switch.instate(["selected"]):
        main.style.theme_use("forest-light")
     else:
        main.style.theme_use("forest-dark")

frame = ttk.Frame(main.root)
frame.pack()

#types of expenses
combo_list = ["Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Transporte","Salud","Bolucompra","Ingresos","Ahorros"]
cuota_list = ["1","3","6","12","24","36","48"]
category_totals = [[0] * (len(combo_list) - 2) for _ in range(12)]

# Widgets to insert data

widgets_frame = ttk.LabelFrame(frame, text="Ingresar Datos")
widgets_frame.grid(row=0, column=0, padx=20, pady=20)

expense_date = DateEntry(widgets_frame)
expense_date.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")
date_from = DateEntry(widgets_frame, selecmode="day", year=2024, month=1, day=1)

expense_type = ttk.Combobox(widgets_frame, values=combo_list)
expense_type.insert(0,"Clasificacion")
expense_type.grid(row=1,column=0, padx=5, pady=(0, 5), sticky="ew")

expense_value = ttk.Entry(widgets_frame)
expense_value.insert(0, "Monto")
expense_value.bind("<FocusIn>", lambda e: expense_value.delete('0','end'))
expense_value.grid(row=2, column=0, padx=5, pady=(0,5), sticky="ew")

expense_entry = ttk.Entry(widgets_frame)
expense_entry.insert(0, "Descripcion")
expense_entry.bind("<FocusIn>", lambda e: expense_entry.delete('0', 'end'))
expense_entry.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="ew")

expense_cuota = ttk.Combobox(widgets_frame, values=cuota_list)
expense_cuota.insert(0,"Cuotas")
expense_cuota.grid(row=4,column=0,padx=5, pady=(0,5), sticky="ew")

button = ttk.Button(widgets_frame, text="Guardar", command= insert_row(expense_date,expense_type,expense_value,expense_entry,expense_cuota))
button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

separator = ttk.Separator(widgets_frame)
separator.grid(row=6, column=0, padx=(20,10), pady=10, sticky="ew")

# change theme color with toggle_mod function
theme_switch = ttk.Checkbutton( 
            widgets_frame, text="Modo", style="Switch", command=toggle_mode)
theme_switch.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

# selected month data tree view 
treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, padx=30, pady=5)

treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.grid(row=1, column=2, sticky="ns")

button_frame = ttk.Frame(treeFrame)
button_frame.grid(row=0, column=1, pady=5)

# Button to select month to load
months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
month_select = ttk.Combobox(button_frame, values=months)
month_select.insert(0, "Mes")
month_select.grid(row=0, column=0, columnspan=3, sticky="ew", pady=3)

# Load the information from the selected month
load_month = ttk.Button(button_frame, text="Cargar", command=load_data)
load_month.grid(row=1, column=0, sticky="e", padx=0.5)

# Configure the treeview headings
cols = ("Fecha","Clasificacion","Monto","Descripcion")
treeview = ttk.Treeview(treeFrame, show="headings", 
                        yscrollcommand=treeScroll.set, columns=cols, height=10)
treeview.column("Fecha", width=100, anchor="center")
treeview.column("Clasificacion", width=150, anchor="center")
treeview.column("Monto", width=150, anchor="center")
treeview.column("Descripcion", width=250, anchor="center")
treeview.heading("Fecha", text="Fecha",anchor="center")
treeview.heading("Clasificacion", text="Clasificacion", anchor="center")
treeview.heading("Monto", text="Monto", anchor="center")
treeview.heading("Descripcion", text="Descripcion", anchor="center")
treeview.grid(row=1, column=1)
treeScroll.config(command=treeview.yview)

# Configure the item selection from table
menu = None
treeview.bind("<Button-3>",show_menu)
# Graph frame

graphframe = ttk.LabelFrame(frame, text="Graficas")
graphframe.grid(row=1, column=0, columnspan=2)

chart_shown = True
# show graph button
ver_button = ttk.Button(button_frame, text="Ver", command=show_chart)
ver_button.grid(row=1,column=2, sticky="w",padx=0.5)