import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import openpyxl
import os
import openpyxl.workbook
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gui

# Make and show chart for the selected month
def show_chart(refresh = False):
   global chart_shown, canvas, pie_canvas
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
   
   if chart_shown or refresh:
          
    # Set the active sheet based on the selected month
    filepath = "./Gastos.xlsx"
    workbook = openpyxl.load_workbook(filepath)
    selected_month = gui.month_select.get()
    #print(selected_month)
    try:
      sheet = workbook[selected_month]
    except KeyError:
      sheet = workbook.active
   
    data = list(sheet.values)
    categorias =["Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Transporte","Salud","Bolucompra"]
    
    amounts = [sum(float(row[2]) for row in data if row[1] == category) for category in categorias]
    sorted_categories = [category for _, category in sorted(zip(amounts, categorias), reverse=True)]
    sorted_amounts = [amount for amount, _ in sorted(zip(amounts, categorias), reverse=True)]
    total = sum(amounts)

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
    figure.suptitle(f"Total gastado por categoria para el mes {selected_month}", y=0.98)
    ax.set_xlabel("Categoria")
    ax.set_ylabel("Total ($ARS)")

    # Plot the bar chart  
    bars = ax.bar(sorted_categories, sorted_amounts, color=[colors[category][0] for category in sorted_categories], edgecolor='black', linewidth=1)
    # Add shadows
    ax.bar([x - 0.5 for x in range(len(sorted_categories))], sorted_amounts, color=[colors[category][1] for category in sorted_categories], edgecolor='black', linewidth=1, zorder=10)
    
    ax.set_xticks([x - 0.25 for x in range(len(categorias))])
    ax.set_xticklabels(sorted_categories, rotation=45, ha='right')
    ax.set_facecolor('#c0c0c0')
    ax.text(0.95, 0.95, f"Total: ${int(total):,}", ha="right", va="top", 
        fontweight='bold', color='black', fontsize=10, transform=ax.transAxes, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    figure.patch.set_facecolor("#808080")
    figure.tight_layout() # makes the labels fit the plot area
    
    # Create the canvas for the bar chart
    canvas = FigureCanvasTkAgg(figure, master=gui.graphframe)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)
    
    # pctdistance moves the label x amount from the center to the outside
    ax2.pie(pie_amounts,  autopct=lambda p: '{:.1f}%'.format(p), startangle=90, pctdistance=0.75, textprops={'fontsize':10, 'fontweight': 'bold'}  ,colors=['#4CAF50', '#FF9800', '#009688', '#2196F3', '#66c0f4', '#c7d5e0', '#ffd700', '#ff7f50', '#d11141', '#808080'], labels=pie_categorias)
    ax2.axis('equal')
    figure2.suptitle("Porcentaje por categoria", y=0.98)
    figure2.patch.set_facecolor("#808080")
    
    # Add each category total to the top of each bar
    for bar, amount in zip(bars.patches, sorted_amounts):
       if int(amount) >= 1000:
          text = f"{amount/1000:.1f}k"
       else:
          text= f"{int(amount):,}"
       ax.text(bar.get_x() - 0.15 + bar.get_width()/2, bar.get_y() + bar.get_height(), text, ha='center', va='bottom', fontweight='bold', color='black',fontsize=9)
    
    # Canvas for pie chart
    pie_canvas = FigureCanvasTkAgg(figure2, master=gui.graphframe)
    pie_canvas.draw()
    pie_canvas.get_tk_widget().grid(row=0, column=1)
    
        
    # Resize window when chart is shown
    gui.graphframe.grid_rowconfigure(0, weight=1)
    gui.graphframe.grid_columnconfigure(0, weight=1)
    gui.frame.rowconfigure(gui.graphframe, weight=1)
    gui.frame.columnconfigure(gui.graphframe, weight=1)
    gui.root.rowconfigure(0, weight=1)
    gui.root.columnconfigure(0, weight=1)
    gui.root.geometry("1100x780")
    chart_shown = False
   else:
      # Hide the chart
      for widget in gui.graphframe.winfo_children():
         widget.grid_remove()
      gui.graphframe.grid_rowconfigure(0, weight=0)
      gui.graphframe.grid_columnconfigure(0, weight=0)
      gui.frame.rowconfigure(0, weight=0)
      gui.frame.columnconfigure(0, weight=0)
      gui.root.rowconfigure(0, weight=0)
      gui.root.columnconfigure(0, weight=0)
      gui.root.geometry("1050x356")
      chart_shown = True