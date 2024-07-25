import tkinter as tk
from tkinter import ttk
import openpyxl
import os

# Load data from excel file
def load_data():
     
   filepath = "K:\Tomas\Arduino proyects\Python\TKinter\Gastos.xlsx"
   # Check if excel file exist
   if not os.path.exists(filepath):
      workbook = openpyxl.Workbook()
      sheet = workbook.active
      heading = ["Fecha","Categoria","Monto","Descripcion","Cuotas"]
      sheet.append(heading)
      workbook.save(filepath)
      
   workbook = openpyxl.load_workbook(filepath)
   sheet = workbook.active
   
   list_values = list(sheet.values)
   print(list_values)
   for row in list_values[0:]:
      treeview.insert("","end",values=row[0:])
     
   

# Theme change from dark to light mode
def toggle_mode():
     if theme_switch.instate(["selected"]):
        style.theme_use("forest-light")
     else:
           style.theme_use("forest-dark")

def insert_row():
   date = expense_date.get()
   category = expense_type.get()
   amount = expense_value.get()
   cuota = expense_cuota.get()
   desc = expense_entry.get()
   
   filepath = "K:\Tomas\Arduino proyects\Python\TKinter\Gastos.xlsx"
   workbook = openpyxl.load_workbook(filepath)
   sheet = workbook.active
   
   new_row = [date, category, amount, desc, cuota]
   sheet.append(new_row)
   workbook.save(filepath)
   
   treeview.insert("","end",values=[date,category,amount,desc])

  
root = tk.Tk()

#import the tcl file to style the window
style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

#types of expenses
combo_list = ["Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Salud","Bolucompra","Ahorros"]
cuota_list = ["1","3","6","12","24","36","48"]
frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Ingresar Datos")
widgets_frame.grid(row=0, column=0, padx=20, pady=20)

# Widgets to insert data

expense_date = ttk.Entry(widgets_frame)
expense_date.insert(0,"YYYY-MM-DD")
expense_date.bind("<FocusIn>", lambda e: expense_date.delete('0', 'end'))
expense_date.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

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

button = ttk.Button(widgets_frame, text="Guardar", command=insert_row)
button.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
#

separator = ttk.Separator(widgets_frame)
separator.grid(row=6, column=0, padx=(20,10), pady=10, sticky="ew")

# change theme color with toggle_mod function
theme_switch = ttk.Checkbutton( 
            widgets_frame, text="Modo", style="Switch", command=toggle_mode)
theme_switch.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

# selected month data tree view 

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

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
treeview.pack()
treeScroll.config(command=treeview.yview)

# Load the data to .xlxs
load_data()


root.mainloop()