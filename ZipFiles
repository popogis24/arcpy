import os
import zipfile

def zip_each_pdf_to_directory(source_directory, destination_directory):
    # Verifica se os diretórios de origem e destino existem
    if not os.path.isdir(source_directory):
        print(f"O diretório de origem '{source_directory}' não existe.")
        return

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)
        print(f"Diretório de destino '{destination_directory}' criado.")

    # Percorre todos os arquivos no diretório de origem
    pdf_files = [file for file in os.listdir(source_directory) if file.lower().endswith('.pdf')]

    # Se não houver arquivos PDF no diretório de origem, exibe uma mensagem e sai da função
    if not pdf_files:
        print(f"Não foram encontrados arquivos PDF no diretório de origem '{source_directory}'.")
        return

    # Cria um arquivo zip para cada arquivo PDF no diretório de destino
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(source_directory, pdf_file)
        zip_file_name = os.path.join(destination_directory, f"{os.path.splitext(pdf_file)[0]}.zip")

        with zipfile.ZipFile(zip_file_name, "w") as zip_file:
            zip_file.write(pdf_file_path, pdf_file)

        print(f"{zip_file_name} criado com sucesso!")

if __name__ == "__main__":
    source_directory_to_zip = fr"C:\Users\anderson.souza\Downloads\PDF\Alternativas_Locacionais_Tecnologicas\Otimizacao_Alt_Locacional_A1"  # Substitua pelo caminho do diretório que contém os PDFs
    destination_directory = fr"C:\Users\anderson.souza\Downloads\PDF\Zipados\Alternativas_Locacionais_Tecnologicas\Otimizacao_Alt_Locacional_A1"  # Substitua pelo caminho do diretório de destino dos ZIPs
    zip_each_pdf_to_directory(source_directory_to_zip, destination_directory)
