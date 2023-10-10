import arcpy
import os
import shutil

root_directory = fr'C:\Users\anderson.souza\Downloads\municipios\municipios'
for dirpath, dirnames, filenames in os.walk(root_directory):
    #busca o arquivo "AREA_IMOVEL" em cada uma das pastas e renomeia ele com o nome da pasta que ele tá
    for file_name in filenames:
        if 'RESERVA_LEGAL' in file_name:
            file_path = os.path.join(dirpath, file_name)
            #quero extrair o nome da pasta que o arquivo está
            prefix = os.path.basename(os.path.dirname(file_path))
            new_file_name = f"{prefix}_{file_name}"
            # Faz uma cópia do arquivo na nova pasta com o novo nome
            nova_pasta = fr'C:\Users\anderson.souza\Downloads\municipios\reserva_legal'
            shutil.copy(file_path, os.path.join(nova_pasta, new_file_name))
            
            
arcpy.env.workspace = nova_pasta
arcpy.Merge_management(arcpy.ListFeatureClasses(), fr'C:\Users\anderson.souza\Downloads\municipios\reserva_legal\reserva_legal.shp')
        
