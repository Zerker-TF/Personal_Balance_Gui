import tkinter as tk
from tkinter import ttk, messagebox
import os
import sqlite3
from tkcalendar import Calendar, DateEntry
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pyperclip




def load_data(month, year, treeview, graphs):
   conn = sqlite3.connect("./Gastos.db")
   cursor = conn.cursor()
   
   month_number = {
          "Enero":"01", "Febrero":"02", "Marzo": "03","Abril":"04","Mayo":"05",
          "Junio":"06", "Julio":"07","Agosto":"08","Septiembre":"09","Octubre":"10",
          "Noviembre":"11","Diciembre":"12"}
       
   month_select = month_number.get(month)
   
   query = '''
      SELECT fecha, categoria, monto, descripcion, cuotas
      FROM gastos
      WHERE strftime('%Y', fecha) = ? AND strftime('%m', fecha) = ?
   '''
   cursor.execute(query, (year, month_select))
   list_values = cursor.fetchall()
   
   if not list_values:
      messagebox.showerror("Error",f"No se encontro informacion para el mes de {month} en {year}. La base de datos podria estar vacia")
      conn.close()
      return
   
   for item in treeview.get_children():
      treeview.delete(item)
   
   for row in list_values:
      treeview.insert("","end", values = row)
      
   conn.close()
   
   show_chart(True,month,year,graphs)
   


def insert_data(exp_date,category,amount,cuota,desc,year_select,treeview,graphs) :
   
   date_obj = datetime.datetime.strptime(exp_date,"%m/%d/%y")
   date = date_obj.strftime("%Y-%m-%d")
   
   conn = sqlite3.connect("./Gastos.db")
   cursor = conn.cursor()
   
   # Calcular cuotas
   if cuota != 1:
      cuota = int(cuota)
      divided_amount = amount / cuota
      month_index = date_obj.month
      year = date_obj.year
      
      for i in range(cuota):
         new_date = f"{year}-{str(month_index).zfill(2)}-{date[8:]}"
         new_row = (new_date, category, divided_amount, desc if desc else " ", cuota if cuota else 1)
         #Guardo las cuotas en los meses correspondientes
         cursor.execute('''
                        INSERT INTO gastos(fecha, categoria, monto, descripcion, cuotas)
                        VALUES (?, ?, ?, ?, ?)
                        ''',new_row)
         month_index += 1
         if month_index > 12:
            month_index = 1
            year += 1
         
   else:
      new_row = (date, category, amount, desc if desc else " ", cuota if cuota else 1)
      cursor.execute('''
                     INSERT INTO gastos (fecha, categoria, monto, descripcion, cuotas)
                     VALUES (?, ?, ?, ?, ?)
                     ''',new_row)

   conn.commit()
   print("data guardada")
   
   treeview.insert("","end",values=[date,category,amount,desc if desc else " "])
   month_select = date_obj.strftime("%B")
   show_chart(True ,month_select,year_select,graphs)
   
   
   conn.close()

import pyperclip
from tkinter import messagebox

def copy_row(event, treeview):
    try:
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showwarning('ERROR', 'Seleccione una fila')
            return
        
        values = treeview.item(selected_item[0], 'values')
        if not values:
            messagebox.showwarning("Error", "La fila seleccionada está vacía")
            return
        
        row_data = "\t".join(map(str,values))
        pyperclip.copy(row_data)
        messagebox.showinfo("Copiado",f"Fila copiada:\n{row_data}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")
        

def edit_row(exp_date,exp_type,exp_value,exp_entry,exp_cuota,treeview):
    try:
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showwarning("Error","Seleccione una fila.")
            return
        
        values = treeview.item(selected_item[0],"values")
        if not values:
            messagebox.showwarning("Error","La fila esta vacia.")
            return
        
        # Data needed if cuota > 1
        cuotas = int(values[4]) if values[4] else 1
        date = datetime.datetime.strptime(values[0], "%Y-%m-%d")
        day = date.day
        
        # Dealing with empty field
        t_values = tuple(value if value else None for value in values)
        # Enter values into widgets
        date_str = t_values[0]
        print(date_str)
        exp_date.set_date(datetime.datetime.strptime(date_str,"%Y-%m-%d"))
        exp_type.set(t_values[1])
        exp_value.delete(0,tk.END)
        exp_value.insert(0,t_values[2])
        exp_entry.delete(0,tk.END)
        exp_entry.insert(0,t_values[3])
        exp_cuota.set(t_values[4])
    
        # Delete row from db
        conn = sqlite3.connect("./Gastos.db")
        cursor = conn.cursor()
        query = '''
            DELETE FROM gastos
            WHERE fecha = ? AND categoria = ? AND monto = ? AND descripcion = ? AND cuotas = ?
        '''
        cursor.execute(query,values)
        
        # if edited row has cuota > 1, deletes from the following months as well
        if cuotas > 1:
            month_index = date.month
            year = date.year
            
            for i in range(1,cuotas):
                month_index += 1
                if month_index > 12:
                    month_index = 1
                    year += 1
                next_date = f"{year}-{str(month_index).zfill(2)}-{str(day).zfill(2)}"
                cursor.execute('''
                               DELETE FROM gastos
                               WHERE fecha = ? AND categoria = ? AND monto = ? AND descripcion = ?
                               ''',next_date,values[1],values[2],values[3])
        
        conn.commit()
        conn.close()
        
        treeview.delete(selected_item[0])
        
       
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

    


 
#def delete_row(month_select,treeview,year,graphs):
#    selected_item = treeview.selection()[0]
#    row_values = treeview.item(selected_item, 'values')
#    date = row_values[0]
#    date = datetime.datetime.strptime(date, "%Y-%m-%d").date() #converting to datetime.date format
#    #Delete the row from treeview
#    treeview.delete(selected_item)
#  # Delete the row from Excel file
#    filepath = "./Gastos.xlsx"
#    workbook = openpyxl.load_workbook(filepath)
#    month = month_select.get()
#    try:
#       sheet = workbook[month]
#    except KeyError:
#       sheet = workbook.active
#  # Find the row 
#    for i, row in enumerate(list(sheet.values)):
#       if i>0:
#          row_date = row[0]
#          if isinstance(row_date,str):
#             row_date = datetime.datetime.strptime(row_date, "%Y-%m-%d").date()
#          elif isinstance(row_date, datetime.datetime):
#             row_date = row_date.date()
#          if row_date == date:
#             sheet.delete_rows(i+1)
#             break
#    workbook.save(filepath)    
#    load_data(month_select,year,treeview,graphs)
    
 
 
def show_chart(chart_shown,month_select,year,graphframe):
       global  canvas, pie_canvas
       
       month_number = {
          "Enero":"01", "Febrero":"02", "Marzo": "03","Abril":"04","Mayo":"05",
          "Junio":"06", "Julio":"07","Agosto":"08","Septiembre":"09","Octubre":"10",
          "Noviembre":"11","Diciembre":"12"}
       
       colors = {

        "Comida": ['#4CAF50', '#2E865F'],

        "Alquiler": ['#FF9800', '#FFC107'],

        "Expensas": ['#009688', '#00796B'],

        "Internet": ['#2196F3', '#1976D2'],

        "Agua": ['#66c0f4', '#45B3FA'],

        "Gas": ['#c7d5e0', '#B2E6CE'],

        "Luz": ['#ffd700', '#F7DC6F'],

        "Transporte": ['#ff7f50', '#cc6540'],

        "Salud": ['#3E69DA', '#2b4998'],

        "Bolucompra": ['#d11141', '#a70d34']

          }
    
       if chart_shown:
            
         conn = sqlite3.connect("./Gastos.db")
         cursor = conn.cursor()
         #print("entra al if show chart")
         
         #print(f"Año:{year}")
         #print(f"Mes:{month_select.zfill(2)}")
         month_n = month_number.get(month_select,None)
         query = '''
            SELECT categoria, SUM(monto)
            FROM gastos
            WHERE strftime('%Y', fecha) =? AND strftime('%m',fecha) = ?
            GROUP BY categoria    
         '''
         #print("Executing query:", query)
         cursor.execute(query, (year, month_n))
         data = cursor.fetchall()
         #print("Resultado de query:",data)
         
         #print("cargo la data")
         if not data:
             return #nada que mostrar
	     
         
         #print("paso el if de no data")
         # preparo la data
         categorias = ["Comida", "Alquiler", "Expensas", "Internet", "Agua", "Gas", "Luz", "Transporte", "Salud", "Bolucompra"]       
         amounts = [0] * len(categorias)
         #print("preparo las categorias")
         for row in data:
            category, total_amount = row
            if category in categorias:
               index = categorias.index(category)
               amounts[index] = total_amount
  
         #print("cargo las filas")
         sorted_categories = [category for _, category in sorted(zip(amounts, categorias), reverse=True)]
         sorted_amounts = [amount for amount, _ in sorted(zip(amounts, categorias), reverse=True)]
         total = sum(amounts)
         ingresos = sum(float(row[2]) for row in data if row[1] == "Ingresos")
         saldo_restante = ingresos-total
          
         # Percentages for pie chart   
         percentages = [f"{(amount/total)*100:.2f}%" for amount in amounts]
  
         # Create a new category "Otros" for pie chart
         otros_amount = sum(amount for amount, percentage in zip(amounts, percentages) if float(percentage.strip('%')) < 3)
         otros_percentage = f"{(otros_amount/total)*100:.2f}%"
        
      
         if otros_amount > 0:
           pie_categorias = [category for category, percentage in zip(categorias, percentages) if float(percentage.strip('%')) >= 3] + ["Otros"]
           pie_amounts = [amount for amount, percentage in zip(amounts, percentages) if float(percentage.strip('%')) >= 3] + [otros_amount]
         else:
           pie_categorias = [category for category, percentage in zip(categorias, percentages) if float(percentage.strip('%')) >= 3]
           pie_amounts = [amount for amount, percentage in zip(amounts, percentages) if float(percentage.strip('%')) >= 3] 
  
  
         # Create the figure and axis
         figure, ax = plt.subplots(figsize=(8, 6))
         # Create the figure and axis for pie chart
         figure2, ax2 = plt.subplots(figsize=(4.5, 6))
  
         # Title and labels
         figure.suptitle(f"Total gastado por categoria para el mes {month_select}", y=0.98)
         ax.set_xlabel("Categoria")
         ax.set_ylabel("Total ($ARS)")
  
         # Plot the bar chart  
         bars = ax.bar(sorted_categories, sorted_amounts, color=[colors[category][0] for category in sorted_categories], edgecolor='black', linewidth=1)
         # Add shadows
         ax.bar([x - 0.5 for x in range(len(sorted_categories))], sorted_amounts, color=[colors[category][1] for category in sorted_categories], edgecolor='black', linewidth=1, zorder=10)
  
         ax.set_xticks([x - 0.25 for x in range(len(categorias))])
         ax.set_xticklabels(sorted_categories, rotation=45, ha='right')
         ax.set_facecolor('#d8d8d8')
  
         # Prints the total spent in the selected month
         ax.text(0.95, 0.95, f"Total: ${int(total):,}", ha="right", va="top", 
             fontweight='bold', color='black', fontsize=10, transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
          
         # Prints the remaining budget for the month
         if saldo_restante >= 0:
              ax.text(0.95, 0.88, f"Saldo: ${int(saldo_restante):,}", ha="right", va="top", 
                 fontweight='bold', color='black', fontsize=10, transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
         else:
             ax.text(0.95, 0.88, f"Saldo: ${int(saldo_restante):,}", ha="right", va="top", 
                 fontweight='bold', color='red', fontsize=10, transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
          
         figure.patch.set_facecolor("#F0F0F0")
         figure.tight_layout() # makes the labels fit the plot area
  
         # Create the canvas for the bar chart
         canvas = FigureCanvasTkAgg(figure, master=graphframe)
         canvas.draw()
         canvas.get_tk_widget().grid(row=0, column=0)
          
         # pctdistance moves the label x amount from the center to the outside
         ax2.pie(pie_amounts, autopct=lambda p: '{:.1f}%'.format(p), startangle=90, pctdistance=0.75, radius=0.8,textprops={'fontsize':10, 'fontweight': 'bold'}  ,colors=['#4CAF50', '#FF9800', '#009688', '#2196F3', '#66c0f4', '#c7d5e0', '#ffd700', '#ff7f50', '#d11141', '#808080'], labels=pie_categorias)
         ax2.axis('equal')
         figure2.suptitle("Porcentaje por categoria", y=0.98)
         figure2.patch.set_facecolor("#F0F0F0")
         figure2.tight_layout()
  
         # Add each category total to the top of each bar
         for bar, amount in zip(bars.patches, sorted_amounts):
            if int(amount) >= 1000:
                text = f"{amount/1000:.1f}k"
            else:
                text= f"{int(amount):,}"
            ax.text(bar.get_x() - 0.15 + bar.get_width()/2, bar.get_y() + bar.get_height(), text, ha='center', va='bottom', fontweight='bold', color='black',fontsize=9)
  
         # Canvas for pie chart
         pie_canvas = FigureCanvasTkAgg(figure2, master=graphframe)
         pie_canvas.draw()
         pie_canvas.get_tk_widget().grid(row=0, column=1)
  
         #print("creo los frames")
         # Resize window when chart is shown
         graphframe.grid_rowconfigure(0, weight=1)
         graphframe.grid_columnconfigure(0, weight=1)    
         
         conn.close()
         #print("cerro la coneccion")
     
     