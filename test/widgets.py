import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
from data_manager import insert_row, load_data,show_chart

#Ingresar datos widgets
def create_widgets(frame):
    combo_list = ["Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Transporte","Salud","Bolucompra","Ingresos","Ahorros"]
    cuota_list = ["1","3","6","12","24","36","48"]
    global treeview
    expense_date = DateEntry(frame)
    #date_from = DateEntry(frame,selecmode="day",year=2024,month=1,day=1)
    
    expense_type = ttk.Combobox(frame,values=combo_list)
    expense_type.insert(0,"Clasificacion")
    
    expense_value = ttk.Entry(frame)
    expense_value.insert(0,"Monto")
    expense_value.bind("<FocusIn>", lambda e: expense_value.delete('0','end'))
    
    expense_entry = ttk.Entry(frame)
    expense_entry.insert(0, "Descripcion")
    expense_entry.bind("<FocusIn>", lambda e: expense_entry.delete('0', 'end'))
    
    expense_cuota = ttk.Combobox(frame,values=cuota_list)
    expense_cuota.insert(0,"Cuotas")
    save_value = ttk.Button(frame,text="Guardar",command=insert_row(expense_date,expense_type,expense_value,expense_cuota,expense_entry,treeview)) 
    separator = ttk.Separator(frame)
    
    expense_date.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")
    expense_type.grid(row=1,column=0, padx=5, pady=(0, 5), sticky="ew")
    expense_value.grid(row=2, column=0, padx=5, pady=(0,5), sticky="ew")
    expense_entry.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="ew")
    expense_cuota.grid(row=4,column=0,padx=5, pady=(0,5), sticky="ew")
    save_value.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
    separator.grid(row=6,column=0,padx=(20,10),pady=10,sticky="ew")

#Treeview table widgets   
#frame is treeframe, graph is graphframe, window is the main frame 
def create_table(frame,graph,mainframe,window):
    months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    cols = ("Fecha","Clasificacion","Monto","Descripcion")
    global treeview
    
    treeScroll = ttk.Scrollbar(frame)
    button_frame = ttk.Frame(frame)
    treeview = ttk.Treeview(frame,show="headings",
                            yscrollcommand=treeScroll.set,columns=cols,height=10)
    month_select = ttk.Combobox(button_frame,values=months)
    load_month = ttk.Button(button_frame, text="Cargar",command=load_data) #calls function load_data
    ver_button = ttk.Button(button_frame, text="Ver",command=show_chart(graph,mainframe,window,month_select)) #calls function show_chart
    
    treeview.column("Fecha", width=100, anchor="center")
    treeview.column("Clasificacion", width=150, anchor="center")
    treeview.column("Monto", width=150, anchor="center")
    treeview.column("Descripcion", width=250, anchor="center")
    treeview.heading("Fecha", text="Fecha",anchor="center")
    treeview.heading("Clasificacion", text="Clasificacion", anchor="center")
    treeview.heading("Monto", text="Monto", anchor="center")
    treeview.heading("Descripcion", text="Descripcion", anchor="center")
    
    treeScroll.grid(row=1,column=2,sticky="ns")
    treeScroll.config(command=treeview.yview)
    button_frame.grid(row=0,column=1,pady=5)
    month_select.grid(row=0, column=0, columnspan=3, sticky="ew", pady=3)
    load_month.grid(row=1, column=0, sticky="e", padx=0.5)
    ver_button.grid(row=1,column=2, sticky="w",padx=0.5)
    treeview.grid(row=1,column=1)
    
  
    