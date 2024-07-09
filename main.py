import tkinter as tk
from blacklist import add_to_blacklist, search_blacklist, delete_from_blacklist, load_blacklist
from utils import export_blacklist_csv

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

button_add_value = tk.Button(window, text='Adicionar', command=lambda: add_to_blacklist(entry_value, entry_reason, listbox_values))
button_add_value.grid(row=0, column=2, padx=5, pady=5)

button_search_value = tk.Button(window, text='Pesquisar', command=lambda: search_blacklist(listbox_values))
button_search_value.grid(row=1, column=2, padx=5, pady=5)

button_delete_value = tk.Button(window, text='Deletar', command=lambda: delete_from_blacklist(listbox_values))
button_delete_value.grid(row=2, column=2, padx=5, pady=5)

button_export_value = tk.Button(window, text='Exportar', command=lambda: export_blacklist_csv(listbox_values))
button_export_value.grid(row=3, column=2, padx=5, pady=5)

listbox_values = tk.Listbox(window, width=50)
listbox_values.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# lista do CSV na inicialização
load_blacklist(listbox_values)

window.mainloop()
