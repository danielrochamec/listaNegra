import csv
from tkinter import filedialog, messagebox

CSV_FILE = "blacklist.csv"

def read_csv():
    data = []
    try:
        with open(CSV_FILE, "r", newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  
            data = [row for row in reader]
    except FileNotFoundError:
        pass
    return data

def write_csv(data):
    with open(CSV_FILE, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["CPF/CNPJ", "Motivo"])
        writer.writerows(data)

# Exportar a lista de CPF/CNPJ para um arquivo CSV
def export_blacklist_csv(listbox):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not file_path:
        return

    data = [(listbox.get(idx).split(" - ")[0], listbox.get(idx).split(" - ")[1]) for idx in range(listbox.size())]
    
    with open(file_path, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["CPF/CNPJ", "Motivo"])
        writer.writerows(data)

    messagebox.showinfo("Exportação", "Lista exportada com sucesso!")
