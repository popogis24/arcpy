import tkinter as tk
import os
import shutil

def copy_files():
    # Obtém o caminho da pasta raiz
    root_directory = root_directory_entry.get()

    # Cria uma nova pasta para armazenar as cópias dos arquivos zip
    new_directory = os.path.join(root_directory, 'ZipFiles')
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)

    # Obtém o nome do arquivo alvo
    alvo = alvo_entry.get()

    # Obtém o caminho da pasta de destino
    dest_directory = dest_directory_entry.get()

    # Procura todos os arquivos zip com o nome alvo nas pastas e subpastas
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for file_name in filenames:
            if file_name.endswith('.zip') and alvo in file_name:
                # Cria o caminho completo do arquivo
                file_path = os.path.join(dirpath, file_name)

                # Cria o novo nome do arquivo usando um prefixo com base no caminho da pasta
                prefix = os.path.basename(os.path.dirname(file_path))
                new_file_name = f"{prefix}_{file_name}"

                # Faz uma cópia do arquivo na nova pasta com o novo nome
                shutil.copy(file_path, os.path.join(dest_directory, new_file_name))

                print(f"Arquivo copiado: {file_name}")

    print("Fim do processo.")

# Cria a janela principal
root = tk.Tk()
root.title("Copiar arquivos")
root.geometry("400x250")

# Cria o campo de entrada para o caminho da pasta raiz
root_directory_label = tk.Label(root, text="Insira o caminho da pasta raiz:")
root_directory_label.pack()
root_directory_entry = tk.Entry(root)
root_directory_entry.pack()

# Cria o campo de entrada para o nome do arquivo alvo
alvo_label = tk.Label(root, text="Insira o nome do arquivo zip que você quer extrair:")
alvo_label.pack()
alvo_entry = tk.Entry(root)
alvo_entry.pack()

# Cria o campo de entrada para o caminho de destino
dest_directory_label = tk.Label(root, text="Insira o caminho da pasta de destino:")
dest_directory_label.pack()
dest_directory_entry = tk.Entry(root)
dest_directory_entry.pack()

# Cria o botão para executar o script
copy_files_button = tk.Button(root, text="Copiar arquivos", command=copy_files, bg="orange", fg="white")
copy_files_button.pack(pady=10)

# Inicia o loop principal do Tkinter
root.mainloop()
