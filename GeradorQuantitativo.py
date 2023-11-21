import arcpy
import os.path
import pandas as pd
import numpy as np

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False


lt = #linha de transmissão previa
circuito_duplo: #insira a coluna que divide os circuitos
vert_inicial = #a linha começa no vertice 01 ou 02?
fx_interesse = #largura da faixa de interesse
bdgis = # insira o endereço do banco de dados GIS
temas_extra = #multiple values (separados por vírgula) de temas que não estão no banco de dados GIS
gdb_path = #caminho do geodatabase final, que terá os temas que estão no banco de dados GIS
pasta_quantitativo = #pasta onde serão salvos os arquivos excel
divisao_estadual = ''
arcpy.env.workspace = gdb_path
feature_datasets = arcpy.ListDatasets()
if 'Quantitativo' not in feature_datasets:
    arcpy.CreateFeatureDataset_management(gdb_path, 'Quantitativo', arcpy.Describe(lt).spatialReference)
else:
    pass
gdb_quantitativo = os.path.join(gdb_path, 'Quantitativo')

def project(gdb):
    arcpy.env.workspace = gdb
    feature_datasets = arcpy.ListDatasets()
    if 'Temas' not in feature_datasets:
        arcpy.CreateFeatureDataset_management(gdb, 'Temas', arcpy.Describe(lt).spatialReference)
    else:
        pass
    arcpy.env.workspace = bdgis
    feature_classes = arcpy.ListFeatureClasses()
    if temas_extra != '':
        feature_classes.append(temas_extra)
    for fc in feature_classes:
        #intersect entre a fc e a divisão estadual
        fc = arcpy.analysis.Intersect(in_features=[fc, divisao_estadual], out_feature_class=fr'div_estado_{fc}')
        arcpy.FeatureClassToFeatureClass_conversion(fc, os.path.join(gdb, 'Temas'), fc)


def determine_feature_type(fc):
    if arcpy.Describe(fc).shapeType == 'Point':
        return 'Ponto'
    elif arcpy.Describe(fc).shapeType == 'Polyline':
        return 'Linha'
    elif arcpy.Describe(fc).shapeType == 'Polygon':
        return 'Poligono'
    else:
        return 'Desconhecido'
    
def dissolve(fc):
    fields_interesse = []
    filename = os.path.basename(fc)
    if filename == 'Unidade_de_Conservação':
        fields_interesse.extend('NOME_UC','TIPO_UC')
    elif filename == 'Aerodromos':
        fields_interesse.extend('NOME_AERODROMO','TIPO_AERODROMO')
    output = arcpy.Dissolve_management(fc, "fcdissolved", fields_interesse) 
    return output

def fields(fc):
    filename = os.path.basename(fc)
    fields_to_keep = []
    if filename == 'Unidade_de_Conservação':
        fields_to_keep.extend('NOME_UC','TIPO_UC')
    return fields_to_keep

def gdb_to_dict(gdb):
    arcpy.env.workspace = gdb
    feature_classes = arcpy.ListFeatureClasses()
    feature_class_dict = {}
    for fc in feature_classes:
        desc = arcpy.Describe(fc)
        feature_class_dict[fc] = {"nome": desc.name, "tipo": determine_feature_type(desc)}
    return feature_class_dict

def ltxfeature(fc, lt):
    dissolved_fc = dissolve(fc)
    dissolved_fc = arcpy.CopyFeatures_management(fc, r'in_memory\fc')
    filename = os.path.basename(fc)
    if "Vertices" in fields(fc):
        if arcpy.Describe(fc).shapeType == 'Polyline':         
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='POINT')
            arcpy.AddField_management(output, 'Eixo_X', 'FLOAT')
            arcpy.CalculateField_management(output, 'Eixo_X', '!shape.firstPoint.X!', 'PYTHON')
            arcpy.CalculateField_management(output, 'Eixo_Y', '!shape.firstPoint.Y!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon':
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='LINE')
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')
    elif "Vertice" not in fields(fc):
        if arcpy.Describe(fc).shapeType == 'Polyline':
            if circuito_duplo != '':
                lt=arcpy.management.Dissolve(in_features=lt, out_feature_class='dissolved_lt',dissolve_field=circuito_duplo)
            else:
                lt=arcpy.management.Dissolve(in_features=lt, out_feature_class='dissolved_lt')
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='POINT')
            arcpy.AddField_management(output, 'Eixo_X', 'FLOAT')
            arcpy.CalculateField_management(output, 'Eixo_X', '!shape.firstPoint.X!', 'PYTHON')
            arcpy.CalculateField_management(output, 'Eixo_Y', '!shape.firstPoint.Y!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon':
            if circuito_duplo != '':
                lt=arcpy.management.Dissolve(in_features=lt, out_feature_class='dissolved_lt',dissolve_field=circuito_duplo)
            else:
                lt=arcpy.management.Dissolve(in_features=lt, out_feature_class='dissolved_lt')
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='LINE')
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')

def fxinteressexfeature(fc, fx_interesse):
    dissolved_fc = dissolve(fc)
    dissolved_fc = arcpy.CopyFeatures_management(fc, r'in_memory\fc')
    filename = os.path.basename(fc)
    if "Vertices" in fields(fc):
        if arcpy.Describe(fc).shapeType == 'Polyline':
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Extensao', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon':
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Area', '!shape.area@hectares!', 'PYTHON')
    elif "Vertice" not in fields(fc):
        if arcpy.Describe(fc).shapeType == 'Polyline':
            if circuito_duplo != '':
                fx_interesse=arcpy.management.Dissolve(in_features=fx_interesse, out_feature_class='dissolved_fx',dissolve_field=circuito_duplo)
            elif circuito_duplo == '':
                fx_interesse=arcpy.management.Dissolve(in_features=fx_interesse, out_feature_class='dissolved_fx')
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Extensao', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon':
            if circuito_duplo != '':
                fx_interesse=arcpy.management.Dissolve(in_features=fx_interesse, out_feature_class='dissolved_fx',dissolve_field=circuito_duplo)
            elif circuito_duplo == '':
                fx_interesse=arcpy.management.Dissolve(in_features=fx_interesse, out_feature_class='dissolved_fx')
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Area', '!shape.area@hectares!', 'PYTHON')

def ltnearfeature(fc,buffer):
    dissolved_fc = dissolve(fc)
    dissolved_fc = arcpy.CopyFeatures_management(fc, r'in_memory\fc')
    arcpy.analysis.Near(in_features=dissolved_fc, near_features=lt, search_radius=buffer)
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(dissolved_fc, 'Distancia', expression, "PYTHON")
    joinedfc = arcpy.management.JoinField(in_data=dissolved_fc, in_field='NEAR_FID', join_table=lt, join_field='OBJECTID')
    arcpy.CalculateField_management(joinedfc, 'OBS', expression, "PYTHON")
    selectfc = arcpy.management.SelectLayerByAttribute(in_layer_or_view=joinedfc, selection_type="NEW_SELECTION", where_clause="NEAR_FID <> -1")
    output = arcpy.CopyFeatures_management(selectfc, fr'{gdb_quantitativo}\LT_Near_{os.path.basename(fc)}')
    arcpy.AddField_management(output, 'OBS', 'TEXT')
    expression = """def neardist(x):
        if x == 0:
            return 'Tema Sobrepõe a LT (Verificar aba de sobreposição)'
        else:
            return ' '"""
    arcpy.management.CalculateField(in_table=output, field='OBS', expression='neardist(!NEAR_DIST!)', code_block=expression)

def toexcel(fc):
    #EXCEL
    campos_selecionados = fields(fc)
    # Obter os nomes originais dos campos
    desc = arcpy.Describe(fc)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]
    data = [row for row in arcpy.da.SearchCursor(fc, campos_originais)]
    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    df = pd.DataFrame(data, columns=campos_originais)
    #verificar se o data frame está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros para esse tema na área de estudo"]})
    else:
        pass
    # Salvar o dataframe em um arquivo Excel
    df.to_excel(os.path.join(pasta_quantitativo, os.path.basename(fr"{fc}.xlsx")), index=False)
   


project(gdb_path)




result_dict = gdb_to_dict(gdb_path)
for key, value in result_dict.items():
    print(f'Nome: {value["nome"]}, Tipo: {value["tipo"]}')
    if value["tipo"] == "Poligono":
        if value["nome"] == "Unidade de Conservação":
            nearpolygon(os.path.join(gdb_path, value["nome"]), '50000')
        else:
            nearpolygon(os.path.join(gdb_path, value["nome"]), '10000')
        ltxarea(os.path.join(gdb_path, value["nome"]))
        fxservicoxarea(os.path.join(gdb_path, value["nome"]))
        fxservidaoxarea(os.path.join(gdb_path, value["nome"]))
    elif value["tipo"] == "Linha":
        ltxlinha(os.path.join(gdb_path, value["nome"]))
        fxservidaoxlinha(os.path.join(gdb_path, value["nome"]))
    elif value["tipo"] == "Ponto":
        ltxponto(os.path.join(gdb_path, value["nome"])) 












