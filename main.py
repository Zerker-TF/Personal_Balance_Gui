import tkinter as tk
from tkinter import ttk
from Data_Expenses import create_expense_window
from Data_Saving import create_savings_window

def main():
    root = tk.Tk()
    root.title("Balance Personal")
    root.minsize(1110,356)
    
    Ventana = ttk.Notebook(root)
    Ventana.grid(row=0,column=0)
    
    frame_gastos = ttk.Frame(Ventana)
    frame_ahorros =ttk.Frame(Ventana)
    
    Ventana.add(frame_gastos,text="Gastos")
    Ventana.add(frame_ahorros,text="Ahorros")
    
    create_expense_window(frame_gastos)
    create_savings_window(frame_ahorros)
    
    
    root.mainloop()
    
if __name__ == "__main__":
    main()