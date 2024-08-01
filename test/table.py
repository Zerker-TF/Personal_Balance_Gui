import tkinter as tk
from tkinter import ttk
import openpyxl
import os
import openpyxl.workbook
from tkcalendar import Calendar, DateEntry
import datetime
from tkinter import messagebox
import pyperclip
from data import load_data
from graphs import show_chart
import gui
from gui import (root,frame,graphframe,month_select,treeview)


# Table item select menu and options

#copy the selected row information to clipboard
def copy_row(event=None):
   selected_item = treeview.selection()
   if selected_item:
      values = treeview.item(selected_item[0], 'values')
      if event:
         column_index = int(treeview.identify_column(event.x)[1:]) - 1
         value = values[column_index]
         if value is not None:
            pyperclip.copy(str(values[column_index]))
         else:
            messagebox.showwarning("Error", "La celda seleccionada esta vacia")
      else:
         non_empty_values = [str(value) for value in values if value is not None]
         pyperclip.copy("\t".join(non_empty_values))
   else:
      messagebox.showwarning('ERROR', 'Por favor, seleccione un dato primero y vuelva a intentarlo!')

# Deletes the choosen row from the excel file
def delete_row():
   selected_item = treeview.selection()[0]
   row_values = treeview.item(selected_item, 'values')
   date = row_values[0]
   
   date = datetime.datetime.strptime(date, "%Y-%m-%d").date() #converting to datetime.date format

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
   load_data()
   
#Inserts selected row data into the boxes and deletes the row from the file
def edit_row():

   selected_item = treeview.selection()[0]
   row_values = treeview.item(selected_item, 'values')
   date = row_values[0]
   date = datetime.datetime.strptime(date, "%Y-%m-%d").date() #converting to datetime.date format
   
   # Insert values into widgets
   gui.expense_date.set_date(date)
   gui.expense_type.set(row_values[1])
   gui.expense_value.delete(0,'end')
   gui.expense_value.insert(0, row_values[2])
   gui.expense_entry.delete(0,'end')
   gui.expense_entry.insert(0, row_values[3])
   gui.expense_cuota.set(row_values[4])
   
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