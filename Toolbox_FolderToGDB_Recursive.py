import arcpy
import os

arcpy.env.overwriteOutput = True

def get_shapefiles_recursive(folder_path):
    """Recursively searches for shapefiles in a folder and its subfolders."""
    shapefiles = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.shp'):
                shapefiles.append(os.path.join(dirpath, filename)) or filename.endswith('.gpkg'):
    return shapefiles

def replace_spaces_with_underscores(file_path):
    """Replaces spaces in a file path with underscores."""
    return file_path.replace(' ', '_')

# Script arguments
input_folder = arcpy.GetParameterAsText(0)
#input_folder = fr'C:\Users\pedro.henrique\OneDrive - Caruso Jr\Documentos 1\Caruso\Bayer\Dados_Vetoriais\Shapefile'

arcpy.env.workspace = input_folder

area_interesse = arcpy.GetParameterAsText(1)
#area_interesse = fr'C:\Users\pedro.henrique\Downloads\BR_UF_2021\BR_UF_2021.shp'

definition_query = arcpy.GetParameterAsText(2)
#arcpy.addMessage(f'{definition_query}')

#input_sp = arcpy.GetParameterAsText(3)
#spatial_reference = arcpy.SpatialReference(text=input_sp)

#output = arcpy.GetParameterAsText(4)
#output = fr'C:\Users\pedro.henrique\OneDrive - Caruso Jr\Documentos 1\Teste'

#fgdb = arcpy.GetParameterAsText(4)
#fgdb = arcpy.management.CreateFileGDB(output, 'teste')
#dataset = arcpy.management.CreateFeatureDataset(fgdb, 'teste', spatial_reference)
dataset = arcpy.GetParameterAsText(3)

ai = arcpy.SelectLayerByAttribute_management(area_interesse, "NEW_SELECTION", definition_query)

featureclasses = get_shapefiles_recursive(input_folder)
#print(featureclasses)

for fc in featureclasses:
    print(fc)
    selected_fc = arcpy.SelectLayerByLocation_management(fc, "INTERSECT", ai, "", "NEW_SELECTION", "NOT_INVERT")
    if selected_fc is not None:
        name = replace_spaces_with_underscores(os.path.splitext(os.path.basename(fc))[0])
        new_fc = arcpy.conversion.FeatureClassToFeatureClass(selected_fc, dataset, name, "")
        # Renomeia a feature class com o nome da pasta onde o shapefile foi encontrado
        folder_name = os.path.basename(os.path.dirname(fc))
        new_name = f"{folder_name}_{name}"
        arcpy.management.Rename(new_fc, new_name)
        #arcpy.addMessage(f'{new_name}, - Concluido')
        #print(new_name)
        
#arcpy.addMessage('Processo finalizado')
