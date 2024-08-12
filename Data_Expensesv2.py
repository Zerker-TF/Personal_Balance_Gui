import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import datetime
import data_functions as df

def create_expense_window(root):
    def cargar_month():
        month = month_select.get()
        df.load_data(month, treeview,graphs)
        
    def insertar():
        date = exp_date.get()
        category = exp_type.get()
        amount = int(exp_value.get())
        cuota = exp_cuota.get()
        desc = exp_entry.get()
        df.insert_data(date,category,amount,cuota,desc,treeview,graphs)
    
    def show_menu(event):
       item = treeview.identify_row(event.y)
       if item:
          menu = tk.Menu(treeview, tearoff=0)
          menu.add_command(label="Copiar",command=lambda: df.copy_row(event,treeview))
          menu.add_command(label="Editar",command=lambda: df.edit_row(exp_date,exp_type,exp_value,exp_entry,exp_cuota,month_select,treeview))
          menu.add_command(label="Eliminar",command=lambda: df.delete_row(month_select,treeview))
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
          
    #def chart():
    #    chart_shown = True
    #    df.show_chart(chart_shown,month_select,graphs)
    ## Table item select menu and options

     #import the tcl file to style the window
    style = ttk.Style(root)
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-dark")

    #types of expenses
    combo_list = ["Comida","Alquiler","Expensas","Internet","Agua","Gas","Luz","Transporte","Salud","Bolucompra","Ingresos","Ahorros"]
    cuota_list = ["1","3","6","12","18","24","36","48"]
    months = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    cols = ["Fecha","Clasificacion","Monto","Descripcion"]
    year_list = [str(i) for i in range (2024,datetime.date.today().year + 6)]
    # Top main frames
    frame = ttk.LabelFrame(root,text="Datos")
    frame.pack(side='top',fill='both')
    
    widgets_frame = ttk.LabelFrame(frame, text="Ingresar Datos")
    widgets_frame.grid(row=0,column=0, padx=20,pady=20)
    
    tableframe = ttk.Frame(frame)
    tableframe.grid(row=0, column=1,columnspan=3,padx=90,pady=5)
    tablescroll = ttk.Scrollbar(tableframe) #Scrollbar
    button_frame = ttk.Frame(tableframe)  
    
 
    # Top Frame widgets
    
    exp_date = DateEntry(widgets_frame)
    date_from = DateEntry(widgets_frame, selecmode="day",year=2024,month=1,day=1)
    
    exp_type = ttk.Combobox(widgets_frame,values=combo_list)
    exp_type.insert(0,"Clasificacion")
    
    exp_value = ttk.Entry(widgets_frame)
    exp_value.insert(0,"Monto")
    exp_value.bind("<FocusIn>",lambda e: exp_value.delete('0','end'))
    
    exp_entry = ttk.Entry(widgets_frame)
    exp_entry.insert(0,"Descripcion")
    exp_entry.bind("<FocusIn>",lambda e: exp_entry.delete('0','end'))
    
    exp_cuota = ttk.Combobox(widgets_frame,values=cuota_list)
    exp_cuota.insert(0,"Cuotas")
        
    save_btt = ttk.Button(widgets_frame,text="Guardar",command=insertar)
    separador = ttk.Separator(widgets_frame)
    
    month_select = ttk.Combobox(button_frame,values=months,width=10)
    month_select.insert(0,months[datetime.date.today().month - 1])
    load_month = ttk.Button(button_frame,text="Cargar",command=cargar_month)
    year_select = ttk.Combobox(button_frame,values=year_list,width=5)
    year_select.insert(0,str(datetime.date.today().year))
    #ver_button = ttk.Button(button_frame,text="Ver",command=chart)
    
    treeview = ttk.Treeview(tableframe,show="headings", yscrollcommand=tablescroll.set,columns=cols, height=10)
    treeview.column("Fecha", width=100, anchor="center")
    treeview.column("Clasificacion", width=150, anchor="center")
    treeview.column("Monto", width=150, anchor="center")
    treeview.column("Descripcion", width=250, anchor="center")
    treeview.heading("Fecha", text="Fecha",anchor="center")
    treeview.heading("Clasificacion", text="Clasificacion", anchor="center")
    treeview.heading("Monto", text="Monto", anchor="center")
    treeview.heading("Descripcion", text="Descripcion", anchor="center")
    treeview.grid(row=1, column=1)
    tablescroll.config(command=treeview.yview)
    menu = None
    treeview.bind("<Button-3>",show_menu)
    
    
    # Placement inside the widget-frame
    exp_date.grid(row=0,column=0, padx=5, pady=5, sticky="ew")
    exp_type.grid(row=1,column=0,padx=5,pady=5,sticky="ew")
    exp_value.grid(row=2,column=0,padx=5,pady=5,sticky="ew")
    exp_entry.grid(row=3,column=0,padx=5,pady=5,sticky="ew")
    exp_cuota.grid(row=4,column=0,padx=5,pady=5,sticky="ew")
    save_btt.grid(row=5,column=0,padx=5,pady=5,sticky="ew")
    separador.grid(row=6,column=0,padx=5,pady=5,sticky="ew")
    
    # Placement for treeview table and scrollbar
   
    tablescroll.grid(row=1,column=2,sticky="ns")
    tablescroll.config(command=treeview.yview)
    button_frame.grid(row=0,column=1,pady=5)
    month_select.grid(row=0,column=0,sticky="e",pady=3)
    load_month.grid(row=1,column=0,columnspan=2,ipadx=40)
    year_select.grid(row=0,column=1,sticky="w",pady=3,padx=2)
    #ver_button.grid(row=1,column=2,sticky="w",padx=0.5)
    
  
    # Bottom main frame
    graphs = ttk.LabelFrame(root, text="Graficas")
    graphs.pack(side="bottom")
    