import tkinter as tk
from tkinter import messagebox, simpledialog
from validation import is_valid_cpf_cnpj
from utils import read_csv, write_csv, export_blacklist_csv

def load_blacklist(listbox):
    data = read_csv()
    for row in data:
        listbox.insert(tk.END, f"{row[0]} - {row[1]}")

# Verificar se o CPF/CNPJ já está na lista
def is_unique(value):
    data = read_csv()
    for row in data:
        if row[0] == value:
            return False
    return True

# ADD CPF/CNPJ à lista negra
def add_to_blacklist(entry_value, entry_reason, listbox):
    value = entry_value.get()
    reason = entry_reason.get()

    if not value or not reason:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")
        return

    clean_value = is_valid_cpf_cnpj(value)
    if clean_value.startswith("CPF inválido") or clean_value.startswith("CNPJ inválido") or clean_value.startswith("CPF/CNPJ inválido"):
        messagebox.showwarning("Entrada inválida", clean_value)
        return

    if not is_unique(clean_value):
        messagebox.showwarning("Entrada duplicada", "Este CPF/CNPJ já está na lista.")
        return

    listbox.insert(tk.END, f"{clean_value} - {reason}")
    data = read_csv()
    data.append([clean_value, reason])
    write_csv(data)

    entry_value.delete(0, tk.END)
    entry_reason.delete(0, tk.END)

# Pesquisar um CPF/CNPJ na lista
def search_blacklist(listbox):
    search_value = simpledialog.askstring("Pesquisar", "Digite o CPF ou CNPJ que deseja pesquisar:")
    if not search_value:
        return

    clean_search_value = is_valid_cpf_cnpj(search_value)
    found_items = []

    data = read_csv()
    for row in data:
        if clean_search_value in row[0]:
            found_items.append(f"{row[0]} - {row[1]}")

    if len(clean_search_value) == 11:  # Se for um CPF, perguntar se é responsável por algum CNPJ
        is_responsible = messagebox.askyesno("Verificação", "Este CPF é responsável por algum CNPJ?")
        if is_responsible:
            for row in data:
                if clean_search_value in row[0] and len(row[0]) == 14:
                    found_items.append(f"{row[0]} - {row[1]}")

    if found_items:
        messagebox.showinfo("Resultados da Pesquisa", "\n".join(found_items))
    else:
        messagebox.showinfo("Resultados da Pesquisa", "Nenhum CPF/CNPJ encontrado.")

# Deletar o CPF/CNPJ selecionado da lista
def delete_from_blacklist(listbox):
    selected_items = listbox.curselection()
    if not selected_items:
        messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
        return

    confirm = messagebox.askyesno("Confirmar deleção", "Você tem certeza que quer apagar o CPF/CNPJ selecionado?")
    if confirm:
        for index in selected_items:
            item = listbox.get(index)
            clean_value = item.split(" - ")[0]
            listbox.delete(index)
            data = read_csv()
            data = [row for row in data if row[0] != clean_value]
            write_csv(data)
