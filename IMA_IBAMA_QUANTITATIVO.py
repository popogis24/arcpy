import arcpy
import os.path
import pandas as pd
import numpy as np
import openpyxl as op


acesso = arcpy.GetParameterAsText(0)
tema = arcpy.GetParameterAsText(1)
fields_tema = arcpy.GetParameterAsText(2)
dataset_quantitativo = arcpy.GetParameterAsText(3)
pasta_excel = arcpy.GetParameterAsText(4)
junkspace = arcpy.GetParameterAsText(5)
field_nome = arcpy.GetParameterAsText(6)

list_acesso = acesso.split(';')
arcpy.management.RepairGeometry(tema)
#teste
def fxinteressexfeature(acesso, tema):

    filename_tema = os.path.basename(tema)
    arcpy.AddMessage(filename_tema)
    filename_acesso = os.path.basename(acesso).replace('.shp', '')
    filename_tema_acesso = fr'{filename_acesso}_x_{filename_tema}'
    fields = fields_tema.split(';')
    arcpy.env.workspace = junkspace
    expression_proj_len = '!shape.length@kilometers!'
    expression_proj_area = '!shape.area@hectares!'
    #dissolve pelos fields tema
    tema_dissolved = arcpy.analysis.PairwiseDissolve(tema, os.path.join(junkspace, fr'{filename_tema}_dissolved.shp'), fields)
    output = arcpy.analysis.PairwiseIntersect([acesso, tema_dissolved], os.path.join(junkspace, fr'Sobreposicao_x_{filename_tema_acesso}'))
    #feature class to feature class
    #dissolve pelo folderpath
    fields_dissolve = [field_nome]+fields
    output_dissolved = arcpy.analysis.PairwiseDissolve(output, os.path.join(junkspace, fr'Sobreposicao_x_{filename_tema_acesso}_dissolved'), fields_dissolve)
    output = arcpy.FeatureClassToFeatureClass_conversion(output_dissolved, dataset_quantitativo, fr'Sobreposicao_x_{filename_tema_acesso}')
    if arcpy.Describe(tema).shapeType == 'Polyline':
        arcpy.CalculateField_management(output, 'Extensao_km', expression_proj_len, 'PYTHON3')
    elif arcpy.Describe(tema).shapeType == 'Polygon':
        arcpy.CalculateField_management(output, 'Area_ha', expression_proj_area, 'PYTHON3')

    return output
    

def ltnearfeature(acesso,buffer,tema):
    filename_tema = os.path.basename(tema)
    arcpy.AddMessage(filename_tema)
    filename_acesso = os.path.basename(acesso).replace('.shp', '')
    filename_tema_acesso = fr'{filename_acesso}_x_{filename_tema}'
    fields = fields_tema.split(';')
    tema_dissolved = arcpy.analysis.PairwiseDissolve(tema, os.path.join(junkspace, fr'{filename_tema}_dissolved'), fields)
    arcpy.analysis.Near(in_features = tema_dissolved, near_features = acesso, search_radius = buffer)
    expression = "round(!NEAR_DIST! / 1000.0, 3)"
    arcpy.CalculateField_management(tema_dissolved, 'Distancia', expression, "PYTHON")
    arcpy.management.JoinField(in_data=tema_dissolved, in_field='NEAR_FID', join_table=acesso, join_field='FID')
    
    expression = "NEAR_DIST = {}".format(min(list))
    selectfc = arcpy.management.SelectLayerByAttribute(in_layer_or_view=os.path.join(junkspace, fr'{filename_tema}_dissolved'), selection_type="NEW_SELECTION", where_clause=expression)
    output1 = arcpy.CopyFeatures_management(selectfc, fr'{junkspace}\Proximidade_x_{filename_tema_acesso}')

    
    output = arcpy.FeatureClassToFeatureClass_conversion(output1, dataset_quantitativo, fr'Proximidade_x_{filename_tema_acesso}')
    arcpy.AddMessage(output)
    arcpy.AddField_management(output, 'OBS', 'TEXT')
    expression = """def neardist(x):
        if x == 0:
            return 'Tema Sobrepõe o acesso (Verificar planilha de sobreposição)'
        else:
            return ' '"""
    arcpy.management.CalculateField(in_table=output, field='OBS', expression='neardist(!NEAR_DIST!)', code_block=expression)




for acesso in list_acesso:
    ltnearfeature(acesso, '100000000 Meters', tema)
    if arcpy.Describe(tema).shapeType == 'Polyline' or arcpy.Describe(tema).shapeType == 'Polygon':
        fxinteressexfeature(acesso, tema)


def excel(fc):
# Extract the path from the feature class result object
    fc_path = arcpy.Describe(fc).catalogPath

    # Get the folder name from the feature class path
    folder_name = os.path.basename(fc_path).split('_x_')[1]    
    arcpy.AddMessage(folder_name)

    # Create the Excel file name using the feature class name
    filename = os.path.basename(fc_path) + '.xlsx'
    arcpy.AddMessage(filename)

    # Create a folder if it doesn't exist
    if not os.path.exists(os.path.join(pasta_excel, folder_name)):
        os.makedirs(os.path.join(pasta_excel, folder_name))

    # Convert the feature class to Excel and save it in the created folder
    arcpy.TableToExcel_conversion(fc_path, os.path.join(pasta_excel, folder_name, filename))



arcpy.env.workspace = dataset_quantitativo
fclist = arcpy.ListFeatureClasses()
#busca todas as feature classes na fclist que comecem com 'Proximidade' e terminem com o mesmo nome de tema 
prox = [fc for fc in fclist if fc.startswith('Proximidade') and fc.endswith(os.path.basename(tema))]
sobr = [fc for fc in fclist if fc.startswith('Sobreposicao') and fc.endswith(os.path.basename(tema))]


if arcpy.Describe(tema).shapeType == 'Point' or arcpy.Describe(tema).shapeType == 'Multipoint':

    todissolve = [field_nome]+fields_tema.split(';')+['Distancia', 'OBS']
    merge_prox = arcpy.Merge_management(prox, os.path.join(dataset_quantitativo, fr'Merge_Proximidade_x_{os.path.basename(tema)}_merged'))
    dissolve_prox = arcpy.analysis.PairwiseDissolve(merge_prox, os.path.join(dataset_quantitativo, fr'Merge_Proximidade_x_{os.path.basename(tema)}'), todissolve)
    excel(dissolve_prox)

else:
    if arcpy.Describe(tema).shapeType == 'Polyline':
        todissolve_sobr = [field_nome]+fields_tema.split(';')+['Extensao_km']
    elif arcpy.Describe(tema).shapeType == 'Polygon':
        todissolve_sobr = [field_nome]+fields_tema.split(';')+['Area_ha']

    todissolve_prox = [field_nome]+fields_tema.split(';')+['Distancia','OBS']  
    merge_prox = arcpy.Merge_management(prox, os.path.join(dataset_quantitativo, fr'Merge_Proximidade_x_{os.path.basename(tema)}_merged'))
    merge_sobr = arcpy.Merge_management(sobr, os.path.join(dataset_quantitativo, fr'Merge_Sobreposicao_x_{os.path.basename(tema)}_merged'))
    dissolve_prox = arcpy.analysis.PairwiseDissolve(merge_prox, os.path.join(dataset_quantitativo, fr'Merge_Proximidade_x_{os.path.basename(tema)}'), todissolve_prox)
    dissolve_sobr = arcpy.analysis.PairwiseDissolve(merge_sobr, os.path.join(dataset_quantitativo, fr'Merge_Sobreposicao_x_{os.path.basename(tema)}'), todissolve_sobr)

    excel(dissolve_prox)
    excel(dissolve_sobr)

