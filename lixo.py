import arcpy
import os

arcpy.env.overwriteOutput = True

def get_shapefiles_recursive(folder_path):
    """Recursively searches for shapefiles in a folder and its subfolders."""
    shapefiles = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.shp'):
                shapefiles.append(os.path.join(dirpath, filename))
    return shapefiles

def replace_spaces_and_dashes_with_underscores(file_path):
    """Replaces spaces in a file path with underscores."""
    return file_path.replace(' ', '_').replace('-', '').replace('(', '').replace(')', '').replace(',', '').replace('.', '')

input_folder = arcpy.GetParameterAsText(0)
arcpy.env.workspace = input_folder
area_interesse = arcpy.GetParameterAsText(1)
definition_query = arcpy.GetParameterAsText(2)
dataset = arcpy.GetParameterAsText(3)
ai = arcpy.SelectLayerByAttribute_management(area_interesse, "NEW_SELECTION", definition_query)
featureclasses = get_shapefiles_recursive(input_folder)

# Caminho do arquivo de texto de saída
output_file = os.path.join(input_folder, "contagem_registros.txt")

with open(output_file, 'w') as file:
    for fc in featureclasses:
        arcpy.AddMessage(fc)
        selected_fc = arcpy.SelectLayerByLocation_management(fc, "INTERSECT", ai, "", "NEW_SELECTION", "NOT_INVERT")
        if selected_fc is not None:
            name = replace_spaces_and_dashes_with_underscores(os.path.splitext(os.path.basename(fc))[0])
            new_fc = arcpy.conversion.FeatureClassToFeatureClass(selected_fc, dataset, name, "")
            folder_name = os.path.basename(os.path.dirname(fc))
            new_name = f"{name}_{folder_name}"
            
            #count = 1
            #while arcpy.Exists(os.path.join(dataset, new_name)):
             #   new_name = f"{name}_{folder_name}_{count}"
              #  count += 1
            
            
            arcpy.management.Rename(new_fc, os.path.join(dataset, new_name))
            new_fc = os.path.join(dataset, new_name)
            
            count_result = arcpy.GetCount_management(new_fc)
            count = int(count_result.getOutput(0))
            arcpy.AddMessage(f"Feature Class: {new_name} - Count: {count}")
            
            # Escrever a contagem no arquivo de texto
            file.write(f"Feature Class: {new_name} - Count: {count}\n")

# Mensagem informando a localização do arquivo de texto
arcpy.AddMessage(f"Contagem de registros salva em: {output_file}")