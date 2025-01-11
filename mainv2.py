import tkinter as tk
from tkinter import ttk
from Data_Expensesv2 import create_expense_window
import sqlite3
import os
from tkinter import messagebox, simpledialog
import expense_functions as df

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
                               cuotas INTEGER DEFAULT 1,
                               usuario INTEGER NOT NULL
                              )
                           ''')
            # save changes
            cursor.execute('''
                          CREATE TABLE IF NOT EXISTS users (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              usuario TEXT NOT NULL   
                              ) 
                           
                           ''')
            name = simpledialog.askstring("Crear un usuario","Ingrese un nombre de usuario")
            if name:
                cursor.execute("INSERT INTO users (usuario) VALUES (?)",(name,))
           
            conn.commit()
            conn.close()
            print("Se genero la base de datos y tablas correctamente.")
        else:
            print("Usuario se fue a buscar su propia base de datos con juegos de azar y mujerzuelas")
            return False
    else:
        print("Base de datos encontrada, cargando informacion.")
        #Leo la columna usuario de las tablas para presentar el combobox y elegir el usuario a cargar.
        # cada numero de 1 a n corresponde a un usuario, orden dictado en como se guarda en una tabal aparte para usuarios
        # Si solo hay una fila en la tabla de usuarios, carga automaticamente dicho usuario.
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        
        #saco los nombres de los usuarios
        cursor.execute("SELECT usuario FROM users")
        tablas = cursor.fetchall()
        print(tablas)
        
        conn.close()
       
        if len(tablas) == 1:
            tabla_select = tablas[0][0]
            messagebox.showinfo("Usuario detectado",f"Cargando gastos de: {tabla_select}")
            
        return True
        
def create_user_menu(root):
    
    user_menu = tk.Menu()
    barra = tk.Menu(user_menu, tearoff=0)
    user_menu.add_cascade(menu=barra,label="Usuarios")
    barra.add_command(
        label="Nuevo Usuario",command=lambda: df.new_user(root)
    )
    barra.add_command(
        label="Cambiar Usuario",command=lambda: df.change_user()
    )
    barra.add_command(
        label="Eliminar Usuario", command=lambda: df.delete_user()
    )
    barra.add_command(
        label="Salir",command=barra.quit
    )
    
    
    
    root.config(menu=user_menu)
    
    
    
    return

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
    
    # Menu de usuarios
    create_user_menu(root)
    
    
    create_expense_window(frame_gastos)

    
    root.mainloop()
    
if __name__ == "__main__":
    main()
    