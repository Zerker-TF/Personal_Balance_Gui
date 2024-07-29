import tkinter as tk
from tkinter import ttk
import openpyxl
import os
import openpyxl.workbook
from tkcalendar import Calendar, DateEntry
import datetime
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# Saves the total spent in each category for the selected month 
def monthly_total(month, amount, category):
 
   global category_totals
   
   month_index = months.index(month)
   
   category_index = combo_list.index(category)
   
   category_totals[month_index][category_index] += amount
   
   return category_totals[month_index]

# Make and show chart for the selected month
def show_chart():
   global chart_shown, canvas
   
   if chart_shown:
    # Set the active sheet based on the selected month
    filepath = "./Gastos.xlsx"
    workbook = openpyxl.load_workbook(filepath)
    selected_month = month_select.get()
    #print(selected_month)
    try:
      sheet = workbook[selected_month]
    except KeyError:
      sheet = workbook.active
   
    data = list(sheet.values)
    categorias =["Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Salud","Bolucompra"]
    
    amounts = [sum(float(row[2]) for row in data if row[1] == category) for category in categorias]
    #print(amounts)
    # Create the figure and axis
    figure, ax = plt.subplots()

    # Title and labels
    ax.set_title(f"Total gastado por categoria para el mes {selected_month}")
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Total ($ARS)")

    # Plot the bar chart
    #                                  comida      alquiler   expensas   internet    agua        gas       luz       salud     bolucompra
    ax.bar(categorias, amounts, color=['#4CAF50', '#FF9800', '#009688', '#2196F3', '#66c0f4', '#c7d5e0', '#ffd700', '#7eb92d', '#1b2838'])
    ax.set_xticklabels(categorias, rotation=45, ha='right')
    ax.set_facecolor('#c0c0c0')
    figure.patch.set_facecolor("#808080")
    figure.tight_layout() # makes the labels fit the plot area
    # Create the canvas
    canvas = FigureCanvasTkAgg(figure, master=graphframe)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)
    
    # Resize window when chart is shown
    graphframe.grid_rowconfigure(0, weight=1)
    graphframe.grid_columnconfigure(0, weight=1)
    frame.rowconfigure(graphframe, weight=1)
    frame.columnconfigure(graphframe, weight=1)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.geometry("1000x720")
    chart_shown = False
   else:
      # Hide the chart
      for widget in graphframe.winfo_children():
         widget.grid_remove()
      graphframe.grid_rowconfigure(0, weight=0)
      graphframe.grid_columnconfigure(0, weight=0)
      frame.rowconfigure(0, weight=0)
      frame.columnconfigure(0, weight=0)
      root.rowconfigure(0, weight=0)
      root.columnconfigure(0, weight=0)
      root.geometry("1000x356")
      chart_shown = True
         
# Save insterted data into the correct excel sheet
def insert_row():
   date = expense_date.get_date().strftime("%Y-%m-%d")
   month = date[5:7]
      
   category = expense_type.get()
   amount = float(expense_value.get())
   cuota = expense_cuota.get()
   desc = expense_entry.get()
   # saving the total of each category ("Ingresos","Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Salud","Bolucompra","Ahorros")
   #print(months[int(month)-1])
   monthly_total(months[int(month)-1], amount, category)
          
   filepath = "./Gastos.xlsx"
   workbook = openpyxl.load_workbook(filepath)
   
   try:
      sheet = workbook[months[int(month)-1]]
   except KeyError:
      sheet = workbook.active
   
   new_row = [date, category, amount, desc if desc else " ", cuota if cuota else 1]
   sheet.append(new_row)
   workbook.save(filepath)
   
   treeview.insert("","end",values=[date,category,amount,desc if desc else " "])

# Load data from excel file on the selected month
def load_data():
   month = month_select.get()

   filepath = "./Gastos.xlsx"
   # Check if excel file exist in path
   if not os.path.exists(filepath):
      messagebox.showerror(title="Error", message="No se encuentra el archivo Gastos.xlsx")
      #workbook = openpyxl.Workbook()
      #sheet = workbook.active
      #heading = ["Fecha","Categoria","Monto","Descripcion","Cuotas"]
      #sheet.append(heading)
      #workbook.save(filepath)
      
   workbook = openpyxl.load_workbook(filepath)
   #print(month)
   try:
      sheet = workbook[month]
   except KeyError:
      sheet = workbook.active
   
   #list_values = list(sheet.values)
   list_values = [list(row) for row in sheet.values]
   # Sort the list by date
   for i, row in enumerate(list_values[1:]):
      if isinstance(row[0], str):
         list_values[i+1][0] = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
      elif isinstance (row[0], datetime.datetime):
         list_values[i+1][0] =row[0].date()
         
   list_values[1:] = sorted(list_values[1:], key=lambda x: x[0])
   #clear the treeview window before printing
   for item in treeview.get_children():
      treeview.delete(item)
      
   for row in list_values[1:]:
      treeview.insert("","end",values=row[0:])

# Theme change from dark to light mode
def toggle_mode():
     if theme_switch.instate(["selected"]):
        style.theme_use("forest-light")
     else:
           style.theme_use("forest-dark")
   
# Table item select menu and options

#copy the selected row information to clipboard
def copy_row():
   i = i+1

# Deletes the choosen row from the excel file
def delete_row():
   selected_item = treeview.selection()[0]
   row_values = treeview.item(selected_item, 'values')
   date = row_values[0]
   
   date = datetime.datetime.strptime(date, "%Y-%m-%d").date() #converting to datetime.date format
   
   #load excel and sheet
   filepath = "./Gastos.xlsx"
   workbook = openpyxl.load_workbook(filepath)
   month = month_select.get()
   try:
      sheet = workbook[month]
   except KeyError:
      sheet = workbook.active
      
   # Find the row 
   for i, row in enumerate(list(sheet.values)):
      if i>0:
         row_date = row[0]
         if isinstance(row_date,str):
            
            row_date = datetime.datetime.strptime(row_date, "%Y-%m-%d").date()
         elif isinstance(row_date, datetime.datetime):
            
            row_date = row_date.date()
         if row_date == date:
            sheet.delete_rows(i+1)
         break
   
   workbook.save(filepath)      
   load_data()
   
# Prompts a message that asks what one variable is to edited and insert the row values in the Ingresar datos box
# and let the user insert the new values that will be sent to that specific row (CHECK MONTH BEFORE SAVING)
def edit_row():

   selected_item = treeview.selection()[0]
   row_values = treeview.item(selected_item, 'values')
   date = row_values[0]
   date = datetime.datetime.strptime(date, "%Y-%m-%d").date() #converting to datetime.date format
   
   # Insert values into widgets
   expense_date.set_date(date)
   expense_type.set(row_values[1])
   expense_value.delete(0,'end')
   expense_value.insert(0, row_values[2])
   expense_entry.delete(0,'end')
   expense_entry.insert(0, row_values[3])
   expense_cuota.set(row_values[4])
   
   # Delete the row from treeview
   treeview.delete(selected_item)

   # Delete the row from Excel file
   filepath = "./Gastos.xlsx"
   workbook = openpyxl.load_workbook(filepath)
   month = month_select.get()
   try:
      sheet = workbook[month]
   except KeyError:
      sheet = workbook.active

   # Find the row 
   for i, row in enumerate(list(sheet.values)):
      if i>0:
         row_date = row[0]
         if isinstance(row_date,str):
            row_date = datetime.datetime.strptime(row_date, "%Y-%m-%d").date()
         elif isinstance(row_date, datetime.datetime):
            row_date = row_date.date()
         if row_date == date:
            sheet.delete_rows(i+1)
            break

   workbook.save(filepath)
   
 
              
def show_menu(event):
   item = treeview.identify_row(event.y)
   if item:
      menu = tk.Menu(treeview, tearoff=0)
      menu.add_command(label="Copiar",command=copy_row)
      menu.add_command(label="Editar",command=edit_row)
      menu.add_command(label="Eliminar",command=delete_row)
      menu.post(event.x_root, event.y_root)
      treeview.bind("<Button-1>",close_menu)
      root.bind("<Button-1>",close_menu)
      
def close_menu(event):
   global menu 
   if menu:
      menu.unpost()
      menu = None
      treeview.unbind("<Button-1>")
      root.unbind("<Button-1>")
  
root = tk.Tk()
root.title("Balance personal")
root.minsize(1050,356)

#import the tcl file to style the window
style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")

#types of expenses
combo_list = ["Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Salud","Bolucompra","Ingresos","Ahorros"]
cuota_list = ["1","3","6","12","24","36","48"]
frame = ttk.Frame(root)
frame.pack()

category_totals = [[0] * (len(combo_list) - 2) for _ in range(12)]

widgets_frame = ttk.LabelFrame(frame, text="Ingresar Datos")
widgets_frame.grid(row=0, column=0, padx=20, pady=20)

# Widgets to insert data

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

button = ttk.Button(widgets_frame, text="Guardar", command=insert_row)
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


root.mainloop()
