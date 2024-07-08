import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from validators import is_valid_cpf_cnpj

def is_unique(listbox_values, value):
    for idx in range(listbox_values.size()):
        item = listbox_values.get(idx)
        if item.startswith(value):
            return False
    return True

def add_to_blacklist(entry_value, entry_reason, listbox_values):
    value = entry_value.get()
    reason = entry_reason.get()

    if not value or not reason:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")
        return

    clean_value = is_valid_cpf_cnpj(value)
    if clean_value.startswith("CPF inválido") or clean_value.startswith("CNPJ inválido") or clean_value.startswith("CPF/CNPJ inválido"):
        messagebox.showwarning("Entrada inválida", clean_value)
        return

    if not is_unique(listbox_values, clean_value):
        messagebox.showwarning("Entrada duplicada", "Este CPF/CNPJ já está na lista.")
        return

    listbox_values.insert(tk.END, f"{clean_value} - {reason}")

    entry_value.delete(0, tk.END)
    entry_reason.delete(0, tk.END)

def search_blacklist(entry_value, listbox_values):
    search_value = entry_value.get()
    clean_search_value = is_valid_cpf_cnpj(search_value)
    found_items = []

    if clean_search_value and not clean_search_value.startswith("CPF inválido") and not clean_search_value.startswith("CNPJ inválido") and not clean_search_value.startswith("CPF/CNPJ inválido"):
        for idx in range(listbox_values.size()):
            item = listbox_values.get(idx)
            if clean_search_value in item:
                found_items.append(item)

    if found_items:
        messagebox.showinfo("Resultados da Pesquisa", "\n".join(found_items))
    else:
        messagebox.showinfo("Resultados da Pesquisa", "Nenhum CPF/CNPJ encontrado.")

def delete_from_blacklist(listbox_values):
    selected_items = listbox_values.curselection()
    if not selected_items:
        messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
        return

    confirm = messagebox.askyesno("Confirmar deleção", "Você tem certeza que quer apagar o CPF/CNPJ selecionado?")
    if confirm:
        for index in selected_items:
            listbox_values.delete(index)

def export_blacklist(listbox_values):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return

    with open(file_path, "w") as file:
        for idx in range(listbox_values.size()):
            file.write(listbox_values.get(idx) + "\n")

    messagebox.showinfo("Exportação", "Lista exportada com sucesso!")

def import_blacklist(listbox_values):
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if not file_path:
        return

    try:
        df = pd.read_excel(file_path)
        if 'CPF/CNPJ' not in df.columns or 'Motivo' not in df.columns:
            messagebox.showwarning("Formato inválido", "O arquivo deve conter as colunas 'CPF/CNPJ' e 'Motivo'.")
            return

        for _, row in df.iterrows():
            value = str(row['CPF/CNPJ'])
            reason = str(row['Motivo'])
            clean_value = is_valid_cpf_cnpj(value)

            if not clean_value.startswith("CPF inválido") and not clean_value.startswith("CNPJ inválido") and not clean_value.startswith("CPF/CNPJ inválido"):
                if is_unique(listbox_values, clean_value):
                    listbox_values.insert(tk.END, f"{clean_value} - {reason}")

        messagebox.showinfo("Importação", "Dados importados com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível importar os dados: {e}")
