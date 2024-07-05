import tkinter as tk
from tkinter import messagebox
import re

# CPF/CNPJ é válido
def is_valid_cpf_cnpj(value):
    
    clean_value = re.sub(r'\D', '', value)
    
    if len(clean_value) == 11 or len(clean_value) == 14:
        return clean_value
    return None

# Verificar se o CPF/CNPJ já está na lista
def is_unique(value):
    for idx in range(listbox_values.size()):
        item = listbox_values.get(idx)
        if item.startswith(value):
            return False
    return True

# Adicionar CPF/CNPJ à lista negra
def add_to_blacklist():
    
    value = entry_value.get()
    reason = entry_reason.get()
    
    if not value or not reason:
        messagebox.showwarning("Entrada inválida", "Por favor, preencha todos os campos.")
        return
    
    clean_value = is_valid_cpf_cnpj(value)
    if not clean_value:
        messagebox.showwarning("Entrada inválida", "Por favor, insira um CPF/CNPJ válido.")
        return
    
    if not is_unique(clean_value):
        messagebox.showwarning("Entrada duplicada", "Este CPF/CNPJ já está na lista.")
        return
    
    listbox_values.insert(tk.END, f"{clean_value} - {reason}")
    
    entry_value.delete(0, tk.END)
    entry_reason.delete(0, tk.END)

def search_blacklist():
    search_value = entry_value.get()
    clean_search_value = is_valid_cpf_cnpj(search_value)
    found_items = []
    
    if clean_search_value:
        for idx in range(listbox_values.size()):
            item = listbox_values.get(idx)
            if clean_search_value in item:
                found_items.append(item)
    
    if found_items:
        messagebox.showinfo("Resultados da Pesquisa", "\n".join(found_items))
    else:
        messagebox.showinfo("Resultados da Pesquisa", "Nenhum CPF/CNPJ encontrado.")

# Deletar o CPF/CNPJ 
def delete_from_blacklist():
    selected_items = listbox_values.curselection()
    if not selected_items:
        messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
        return
    
    confirm = messagebox.askyesno("Confirmar deleção", "Você tem certeza que quer apagar o CPF/CNPJ selecionado?")
    if confirm:
        for index in selected_items:
            listbox_values.delete(index)

# Janela principal
window = tk.Tk()
window.title('Lista Negra Personalizada')

label_value = tk.Label(window, text='CPF/CNPJ:')
label_value.grid(row=0, column=0, padx=5, pady=5)
entry_value = tk.Entry(window)
entry_value.grid(row=0, column=1, padx=5, pady=5)

label_reason = tk.Label(window, text='Motivo:')
label_reason.grid(row=1, column=0, padx=5, pady=5)
entry_reason = tk.Entry(window)
entry_reason.grid(row=1, column=1, padx=5, pady=5)

button_add_value = tk.Button(window, text='Adicionar', command=add_to_blacklist)
button_add_value.grid(row=0, column=2, padx=5, pady=5)

button_search_value = tk.Button(window, text='Pesquisar', command=search_blacklist)
button_search_value.grid(row=1, column=2, padx=5, pady=5)

button_delete_value = tk.Button(window, text='Deletar', command=delete_from_blacklist)
button_delete_value.grid(row=2, column=2, padx=5, pady=5)

listbox_values = tk.Listbox(window, width=50)
listbox_values.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
