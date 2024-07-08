import tkinter as tk
from tkinter import messagebox, filedialog
import re

# Função para validar o CPF
def is_valid_cpf(cpf):
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Calculando o primeiro dígito verificador
    sum = 0
    for i in range(9):
        sum += int(cpf[i]) * (10 - i)
    check_digit1 = 11 - (sum % 11)
    if check_digit1 >= 10:
        check_digit1 = 0

    # Calculando o segundo dígito verificador
    sum = 0
    for i in range(10):
        sum += int(cpf[i]) * (11 - i)
    check_digit2 = 11 - (sum % 11)
    if check_digit2 >= 10:
        check_digit2 = 0

    return cpf[-2:] == f"{check_digit1}{check_digit2}"

# Função para validar o CNPJ
def is_valid_cnpj(cnpj):
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    # Calculando o primeiro dígito verificador
    sum = 0
    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(12):
        sum += int(cnpj[i]) * weights1[i]
    check_digit1 = 11 - (sum % 11)
    if check_digit1 >= 10:
        check_digit1 = 0

    # Calculando o segundo dígito verificador
    sum = 0
    weights2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    for i in range(13):
        sum += int(cnpj[i]) * weights2[i]
    check_digit2 = 11 - (sum % 11)
    if check_digit2 >= 10:
        check_digit2 = 0

    return cnpj[-2:] == f"{check_digit1}{check_digit2}"

# Função para verificar se o CPF/CNPJ é válido
def is_valid_cpf_cnpj(value):
    clean_value = re.sub(r'\D', '', value)
    if len(clean_value) == 11:
        if is_valid_cpf(clean_value):
            return clean_value
        else:
            return "CPF inválido: Falha na verificação dos dígitos."
    elif len(clean_value) == 14:
        if is_valid_cnpj(clean_value):
            return clean_value
        else:
            return "CNPJ inválido: Falha na verificação dos dígitos."
    return "CPF/CNPJ inválido: Número incorreto de dígitos."

# Função para verificar se o CPF/CNPJ já está na lista
def is_unique(value):
    for idx in range(listbox_values.size()):
        item = listbox_values.get(idx)
        if item.startswith(value):
            return False
    return True

# Função para adicionar CPF/CNPJ à lista negra
def add_to_blacklist():
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

    listbox_values.insert(tk.END, f"{clean_value} - {reason}")

    entry_value.delete(0, tk.END)
    entry_reason.delete(0, tk.END)

# Função para pesquisar um CPF/CNPJ na lista
def search_blacklist():
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

# Função para deletar o CPF/CNPJ selecionado da lista
def delete_from_blacklist():
    selected_items = listbox_values.curselection()
    if not selected_items:
        messagebox.showwarning("Seleção inválida", "Por favor, selecione um item para deletar.")
        return

    confirm = messagebox.askyesno("Confirmar deleção", "Você tem certeza que quer apagar o CPF/CNPJ selecionado?")
    if confirm:
        for index in selected_items:
            listbox_values.delete(index)

# Função para exportar a lista de CPF/CNPJ para um arquivo de texto
def export_blacklist():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return

    with open(file_path, "w") as file:
        for idx in range(listbox_values.size()):
            file.write(listbox_values.get(idx) + "\n")

    messagebox.showinfo("Exportação", "Lista exportada com sucesso!")

# Criar a janela principal
window = tk.Tk()
window.title('Lista Negra Personalizada')

# Rótulo e campo de entrada para CPF/CNPJ
label_value = tk.Label(window, text='CPF/CNPJ:')
label_value.grid(row=0, column=0, padx=5, pady=5)
entry_value = tk.Entry(window)
entry_value.grid(row=0, column=1, padx=5, pady=5)

# Rótulo e campo de entrada para o motivo
label_reason = tk.Label(window, text='Motivo:')
label_reason.grid(row=1, column=0, padx=5, pady=5)
entry_reason = tk.Entry(window)
entry_reason.grid(row=1, column=1, padx=5, pady=5)

# Botão para adicionar CPF/CNPJ
button_add_value = tk.Button(window, text='Adicionar', command=add_to_blacklist)
button_add_value.grid(row=0, column=2, padx=5, pady=5)

# Botão para pesquisar CPF/CNPJ
button_search_value = tk.Button(window, text='Pesquisar', command=search_blacklist)
button_search_value.grid(row=1, column=2, padx=5, pady=5)

# Botão para deletar CPF/CNPJ
button_delete_value = tk.Button(window, text='Deletar', command=delete_from_blacklist)
button_delete_value.grid(row=2, column=2, padx=5, pady=5)

# Botão para exportar lista de CPF/CNPJ
button_export_value = tk.Button(window, text='Exportar', command=export_blacklist)
button_export_value.grid(row=3, column=2, padx=5, pady=5)

# Lista para exibir CPFs/CNPJs bloqueados
listbox_values = tk.Listbox(window, width=50)
listbox_values.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Executar a interface
window.mainloop()
