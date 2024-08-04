import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import openpyxl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_savings_window(root):
    
    def ahorros_list():
        filepath = "./Gastos.xlsx"
        workbook = openpyxl.load_workbook(filepath)
        #print(selected_month)
        sheet = workbook["Ahorros"]
        ahorros = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
           if row[0]:
            ahorros.append(row[0])
        
        return ahorros
    
    def new_ahorro():
        filepath = "./Gastos.xlsx"
        workbook = openpyxl.load_workbook(filepath)
        #print(selected_month)
        sheet = workbook["Ahorros"]
        sheet.append(["Nuevo Ahorro"])
        workbook.save(filepath)
        update_combobox()
        update_charts()
        
    def update_combobox():
        ahorro_select['values']=["Nuevo Ahorro"] + ahorros_list()
    
    def get_values():

        filepath = "./Gastos.xlsx"
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook["Ahorros"]

        ahorros = []
        amounts_saved = []
        objectives = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            ahorros.append(row[0])
            amounts_saved.append(row[1])
            objectives.append(row[2])
        return ahorros, amounts_saved, objectives

    def update_charts():
    
        ahorros, amounts_saved, objectives = get_values()

        fig, axs = plt.subplots(len(ahorros), 2, figsize=(8, 1.1*len(ahorros)))
        fig2, axs2 = plt.subplots(len(ahorros), 1, figsize=(4, 2*len(ahorros)))
                                

        for i, (ahorro, amount_saved, objective) in enumerate(zip(ahorros, amounts_saved, objectives)):

            # Horizontal bar chart
            axs[i, 0].barh(0, amount_saved, height=0.4,color='#84b86d') #Bar color
            axs[i, 0].set_yticks([0])
            axs[i, 0].set_yticklabels([ahorro])
            axs[i, 0].set_xlabel('Total Ahorrado')
            axs[i, 0].set_title('Estado de ahorros')
            axs[i, 0].set_facecolor('#808080') #background color
            axs[i, 0].set_ylim(-0.8, 0.8)
            axs[i, 0].set_xlim(0,objective)
            axs[i, 0].set_xticks([0, objective])  # Only show the objective value on the x-axis
            axs[i, 0].text(amount_saved, 0, f'${amount_saved:.2f}', ha='left', va='center')  # Print the amount next to the bar
        for i, (ahorro, amount_saved, objective) in enumerate(zip(ahorros, amounts_saved, objectives)):
             # Circular progress bar
             percentage = (amount_saved / objective) * 100
             axs2[i].pie([percentage, 100 - percentage], colors=['#4CAF50', '#ccc'], startangle=90, autopct='%1.1f%%')
             axs2[i].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
             axs2[i].set_title(ahorro)  # Set the title of each pie chart
                 # Layout so plots do not overlap
        fig.tight_layout()
        fig2.tight_layout()
        fig.patch.set_facecolor("#808080")
        fig2.patch.set_facecolor("#808080")
        # Update the canvas
        canvas = FigureCanvasTkAgg(fig, master=visual_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        canvas2 = FigureCanvasTkAgg(fig2, master=visual_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    #import the tcl file to style the window
    style = ttk.Style(root)
    #root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")
    
    frame = ttk.Frame(root)
    frame.pack()
    
    widgets_frame = ttk.LabelFrame(frame,text="Ingresar Datos")
    widgets_frame.grid(row=0,column=0,padx=20,pady=20)
    
    # Insert data
    
    # Values come from ahorros_list function to update combobox
    lista_ahorros = ahorros_list()
    ahorro_select = ttk.Combobox(widgets_frame,values=["Nuevo Ahorro"] + lista_ahorros)
    ahorro_select.insert(0,"Seleccionar ahorro")
    ahorro_select.current(0)
    ahorro_select.grid(row=0,column=0,padx=5,pady=5,sticky="ew")
    
    ahorro_amount = ttk.Entry(widgets_frame)
    ahorro_amount.insert(0,"Ingrese el monto a reservar")
    ahorro_amount.grid(row=1,column=0,padx=5,pady=5,sticky="ew")
    
    ahorro_final = ttk.Entry(widgets_frame)
    ahorro_final.insert(0,"Objetivo")
    ahorro_final.grid(row=2,column=0,padx=5,pady=5,sticky="ew")
    
    # save/update ahorro button
    new_savings_button = ttk.Button(widgets_frame,text="Guardar",command=new_ahorro)
    new_savings_button.grid(row=3,column=0,padx=5,pady=5,sticky="ew")
 
    separator = ttk.Separator(widgets_frame)
    separator.grid(row=4, column=0, padx=(20,10), pady=10, sticky="ew")
    
    
    visual_frame = ttk.Frame(frame)
    visual_frame.grid(row=0,column=1,padx=30,pady=10)
    
    update_charts()
    
  
    
    
    
    