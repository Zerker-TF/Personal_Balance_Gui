import tkinter as tk
from tkinter import ttk
from Data_Expensesv2 import create_expense_window
import sqlite3
import os
from tkinter import messagebox

def initialize_database():
    filepath = "./Gastos.db"
    
    #Check if db exists
    if not os.path.exists(filepath):
        
        answer = messagebox.askokcancel(title="Base de datos no encontrada", message="Desea generar una nueva base de datos?")
        
        if answer:
            
            conn = sqlite3.connect(filepath)
            cursor = conn.cursor()

            # Create 'gastos' table for everything
    
            cursor.execute('''
                           CREATE TABLE IF NOT EXISTS gastos (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               fecha TEXT NOT NULL,
                               categoria TEXT NOT NULL,
                               monto REAL NOT NULL,
                               descripcion TEXT,
                               cuotas INTEGER DEFAULT 1
                              )
                           ''')
            # save changes
            conn.commit()
            conn.close()
            print("Se genero la base de datos y tablas correctamente.")
        else:
            print("Usuario se fue a buscar su propia base de datos con juegos de azar y mujerzuelas")
            return False
    else:
        print("Base de datos encontrada, cargando informacion.")
        return True
        

def main():
    global root
    
    initialize_database()
    root = tk.Tk()
    root.title("Balance Personal")
    root.minsize(1260, 410)
    root.maxsize(1260, 950)
    root.grid_rowconfigure(0,weight=1)
    root.columnconfigure(0,weight=1)
    
    Ventana = ttk.Notebook(root)
    Ventana.grid(row=0,column=0,sticky="new")
    Ventana.columnconfigure(0,weight=1)
    
    
    frame_gastos = ttk.Frame(Ventana)
    
    
    Ventana.add(frame_gastos,text="Gastos")
    
    
    create_expense_window(frame_gastos)
    #create_savings_window(frame_ahorros)
    
   # Ventana.bind("<<NotebookTabChanged>>", resize)
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
    