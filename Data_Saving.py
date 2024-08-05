import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import openpyxl
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_savings_window(root):

    def ahorros_list():
        filepath = "./Gastos.xlsx"
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook["Ahorros"]
        ahorros = []
        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] not in ahorros:
                ahorros.append(row[0])
        return ahorros

    def new_ahorro():
        if ahorro_select.get() == "Nuevo Ahorro":
            new_ahorro_name = simpledialog.askstring("Nuevo Ahorro", "Ingrese el nombre y ingrese los valores")
            if new_ahorro_name is not None:
                ahorro_select.set(new_ahorro_name)
                update_combobox()
                ahorro_amount.focus_set()
            else:
                messagebox.showerror("Error", "Debe ingresar un nombre para continuar.")
            return

        filepath = "./Gastos.xlsx"
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook["Ahorros"]
        ahorro_name = ahorro_select.get()
        try:
            amount_added = float(ahorro_amount.get())
            objective = float(ahorro_final.get())
        except ValueError:
            messagebox.showerror("Error", "Debe ingresar valores numéricos válidos.")
            return

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] == ahorro_name:
                total_amount = row[1] + amount_added
                sheet.append([ahorro_name, total_amount, objective, date.today(), amount_added])
                break
        else:
            sheet.append([ahorro_name, amount_added, objective, date.today(), amount_added])
        workbook.save(filepath)

        update_combobox()
        update_charts()

    def update_combobox():
        ahorros = ahorros_list()
        ahorro_select['values'] = ["Nuevo Ahorro"] + ahorros
        ahorro_table['values'] = ahorros

    def get_values():
        filepath = "./Gastos.xlsx"
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook["Ahorros"]
        ahorros = []
        amounts_saved = []
        objectives = []
        dates = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] not in ahorros:
                ahorros.append(row[0])
                amounts_saved.append(row[1])
                objectives.append(row[2])
                if isinstance(row[3], str):
                    try:
                        dates.append(datetime.strptime(row[3], "%Y-%m-%d"))
                    except ValueError:
                        dates.append(datetime.strptime(row[3], "%d/%m/%Y"))
                else:
                    dates.append(row[3])

        sorted_data = sorted(zip(ahorros, amounts_saved, objectives, dates), key=lambda x: x[3], reverse=True)
        latest_data = []
        for ahorro, _, _, _ in sorted_data:
            if ahorro not in [x[0] for x in latest_data]:
                latest_data.append(next((x for x in sorted_data if x[0] == ahorro), None))
        ahorros, amounts_saved, objectives, dates = zip(*latest_data)
        return ahorros, amounts_saved, objectives, dates

    def clear_charts():
        for widget in charts_frame.winfo_children():
            widget.destroy()

    def update_charts():
        clear_charts()
        ahorros, amounts_saved, objectives, dates = get_values()
        fig, axs = plt.subplots(len(ahorros), 1, figsize=(8, 1.1 * len(ahorros)))
        fig.suptitle('Listado de Ahorros', color="#bfbfbf")

        for i, (ahorro, amount_saved, objective) in enumerate(zip(ahorros, amounts_saved, objectives)):
            axs[i].barh(0, amount_saved, height=0.3, color='#84b86d')
            axs[i].get_yaxis().set_visible(False)
            axs[i].spines['top'].set_visible(False)
            axs[i].spines['right'].set_visible(False)
            axs[i].spines['left'].set_visible(False)
            axs[i].spines['bottom'].set_color('#808080')
            axs[i].tick_params(axis='x', colors='#808080')
            axs[i].set_yticks([0])
            axs[i].set_yticklabels([ahorro])
            axs[i].set_facecolor('#313131')
            axs[i].set_ylim(-0.4, 0.8)
            axs[i].set_xlim(0, objective)
            axs[i].set_xticks([0, objective])
            axs[i].set_title(ahorro, fontsize=10, loc='left', fontstyle='italic', fontweight='book',
                             bbox=dict(facecolor='#b6d7a8', edgecolor='black', boxstyle='round,pad=0.5'))
            axs[i].text(0.95, 0.98, f"Restante: ${int(objective - amount_saved):,}", ha="right", va="center",
                        fontweight='bold', color='black', fontsize=9,
                        bbox=dict(facecolor='#bac4c1', edgecolor='black', boxstyle='round,pad=0.5'),
                        transform=axs[i].transAxes)

        fig.tight_layout()
        fig.patch.set_facecolor("#313131")

        canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Update scrollbar region
        charts_frame.update_idletasks()
        canvas_scroll.config(scrollregion=canvas_scroll.bbox("all"))

    def insert_table():
        selected_item = ahorro_table.get()
        for item in treeview.get_children():
            treeview.delete(item)
        filepath = "./Gastos.xlsx"
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook["Ahorros"]

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if row[0] == selected_item:
                treeview.insert("", "end", values=(row[3], row[1], row[2]))

    style = ttk.Style(root)
    style.theme_use("forest-dark")

    frame = ttk.Frame(root)
    frame.pack()
    lista_ahorros = ahorros_list()

    # Ingresar frame
    widgets_frame1 = ttk.LabelFrame(frame, text="Ingresar")
    widgets_frame1.grid(row=0, column=0, padx=20, pady=20)

    ahorro_select = ttk.Combobox(widgets_frame1, values=["Nuevo Ahorro"] + lista_ahorros)
    ahorro_select.insert(0, "Seleccionar ahorro")
    ahorro_select.current(0)
    ahorro_select.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    ahorro_amount = ttk.Entry(widgets_frame1)
    ahorro_amount.insert(0, "Ingrese el monto a reservar")
    ahorro_amount.bind("<FocusIn>", lambda e: ahorro_amount.delete('0', 'end'))
    ahorro_amount.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    ahorro_final = ttk.Entry(widgets_frame1)
    ahorro_final.insert(0, "Objetivo")
    ahorro_final.bind("<FocusIn>", lambda e: ahorro_final.delete('0', 'end'))
    ahorro_final.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

    new_savings_button = ttk.Button(widgets_frame1, text="Guardar", command=new_ahorro)
    new_savings_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    separator = ttk.Separator(widgets_frame1)
    separator.grid(row=4, column=0, padx=(10, 10), pady=5, sticky="ew")

    # Retirar frame
    widgets_frame2 = ttk.LabelFrame(widgets_frame1, text="Retirar")
    widgets_frame2.grid(row=5, column=0)

    ahorro_select2 = ttk.Combobox(widgets_frame2, values=lista_ahorros)
    ahorro_select2.insert(0, "Seleccionar ahorro")
    ahorro_select2.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    ahorro_amount2 = ttk.Entry(widgets_frame2)
    ahorro_amount2.insert(0, "Ingrese el monto a retirar")
    ahorro_amount2.bind("<FocusIn>", lambda e: ahorro_amount.delete('0', 'end'))
    ahorro_amount2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    savings_retirar = ttk.Button(widgets_frame2, text="Retirar")
    savings_retirar.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    separator2 = ttk.Separator(widgets_frame2)
    separator2.grid(row=4, column=0, padx=(20, 10), pady=10, sticky="ew")

    # Creating scrollable charts area
    charts_container = ttk.Frame(frame)
    charts_container.grid(row=0, column=1,columnspan=2, padx=5, pady=5, sticky="nsew")
    frame.columnconfigure(1,weight=1) # Expands colum 1

    canvas_scroll = tk.Canvas(charts_container)
    scrollbar = ttk.Scrollbar(charts_container, orient="vertical", command=canvas_scroll.yview)
    canvas_scroll.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas_scroll.pack(side="left", fill="both", expand=True)

    charts_frame = ttk.Frame(canvas_scroll)
    canvas_scroll.create_window((0, 0), window=charts_frame, anchor="nw")

    update_charts()

    visual_frame = ttk.Frame(frame)
    visual_frame.grid(row=2, column=0, padx=20, pady=20)
    frame.rowconfigure(2,weight=1)

    ahorro_table = ttk.Combobox(visual_frame, values=lista_ahorros)
    ahorro_table.insert(0, "Seleccionar ahorro")
    ahorro_table.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    table_button = ttk.Button(visual_frame, text="Ver Tabla", command=insert_table)
    table_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    columns = ("Fecha", "Monto Ahorrado", "Objetivo")
    treeview = ttk.Treeview(visual_frame, columns=columns, show="headings")
    treeview.heading("Fecha", text="Fecha")
    treeview.heading("Monto Ahorrado", text="Monto Ahorrado")
    treeview.heading("Objetivo", text="Objetivo")
    treeview.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
    
    visual_frame.columnconfigure(0, weight=1)
    visual_frame.rowconfigure(1,weight=1)


