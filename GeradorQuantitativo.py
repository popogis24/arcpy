import arcpy
import os.path
import pandas as pd
import numpy as np

arcpy.env.overwriteOutput = True


lt = 'linha_de_transmissao'
fx_servico = 'fx_servico'
fx_servidao = 'fx_servidao'
gdb_path = r'C:\Users\anderson.souza\Documents\CGT_R3_CO.gdb\Dados_Caruso'
gdb_quantitativo = r'C:\Users\anderson.souza\Documents\CGT_R3_CO.gdb\Dados_Quantitativo'
workspace_final = r'C:\Users\anderson.souza\Documents...'

def determine_feature_type(desc):
    if desc.shapeType == 'Point':
        return 'Ponto'
    elif desc.shapeType == 'Polyline':
        return 'Linha'
    elif desc.shapeType == 'Polygon':
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

#FUNCOES GEOMETRICAS

#FUNCOES DE INTERSECCAO
def ltxarea(fc):
    #dissolve tema
    dissolved_fc = dissolve(fc)
    #intersecta o tema com o lt
    filename = os.path.basename(fc)
    output = arcpy.Intersect_analysis([lt, dissolved_fc], os.path.join(gdb_quantitativo,'LT_x_'+filename))
    #cria um field extensao
    arcpy.AddField_management(output, 'Extensao', 'FLOAT')
    #calcula a extensao da lt (linha)
    arcpy.CalculateField_management(output, 'Extensao', '!shape.length@meters!', 'PYTHON')
    #retorna o output em um shapefile
    #copia o output pra uma pasta
    arcpy.CopyFeatures_management(output, os.path.join(workspace_final, filename))

def fxservicoxarea(fc):
    #dissolve tema
    dissolved_fc = dissolve(fc)
    #intersecta a fx_servico com o lt
    filename = os.path.basename(fc)
    output = arcpy.Intersect_analysis([fx_servico, dissolved_fc], os.path.join(gdb_quantitativo,'FXservico_x_'+filename))
    #cria um field area
    arcpy.AddField_management(output, 'Area', 'FLOAT')
    #calcula a area da fx_servico (poligono) em hectares
    arcpy.CalculateField_management(output, 'Area', '!shape.area@hectares!', 'PYTHON')
    #retorna o output em um shapefile
    arcpy.CopyFeatures_management(output, os.path.join(workspace_final, filename))

def fxservidaoxarea(fc):
    #dissolve tema
    dissolved_fc = dissolve(fc)
    #intersecta a fx_servico com o lt
    filename = os.path.basename(fc)
    output = arcpy.Intersect_analysis([fx_servidao, dissolved_fc], os.path.join(gdb_quantitativo,'FXservidao_x_'+filename))
    #cria um field area
    arcpy.AddField_management(output, 'Area', 'FLOAT')
    #calcula a area da fx_servico (poligono) em hectares
    arcpy.CalculateField_management(output, 'Area', '!shape.area@hectares!', 'PYTHON')
    #retorna o output em um shapefile
    arcpy.CopyFeatures_management(output, os.path.join(workspace_final, filename))

def ltxlinha(fc):
    dissolved_fc = dissolve(fc)
    #faça um intersect que gere pontos
    filename = os.path.basename(fc)
    output = arcpy.Intersect_analysis([lt, dissolved_fc], os.path.join(gdb_quantitativo,'LT_x_'+filename),"","","POINT")
    #retorna o output em um shapefile
    arcpy.CopyFeatures_management(output, os.path.join(workspace_final, filename))

def fxservidaoxlinha(fc):
    dissolved_fc = dissolve(fc)
    #faça um intersect que gere pontos
    filename = os.path.basename(fc)
    output = arcpy.Intersect_analysis([fx_servidao, dissolved_fc], os.path.join(gdb_quantitativo,'FXservidao_x_'+filename),"","","POINT")
    #retorna o output em um shapefile
    arcpy.CopyFeatures_management(output, os.path.join(workspace_final, filename))

#FUNCOES DE NEAR
def ltxfeature(fc,buffer):
    dissolved_fc = fc
    
    arcpy.analysis.Near(in_features=fc, near_features=lt, search_radius=buffer)
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(fc, 'Distancia', expression, "PYTHON")
    #join !NEAR_FID! com lt
    joinedfc = arcpy.management.JoinField(in_data=dissolved_fc, in_field='NEAR_FID', join_table=lt, join_field='OBJECTID')
    arcpy.CalculateField_management(joinedfc, 'OBS', expression, "PYTHON")
    #seleciona todos que a coluna NEAR_FID é diferente de -1
    selectfc = arcpy.management.SelectLayerByAttribute(in_layer_or_view=joinedfc, selection_type="NEW_SELECTION", where_clause="NEAR_FID <> -1")
    #copia o select pra uma pasta
    output = arcpy.CopyFeatures_management(selectfc, fr'{workspace_final}\LT_Near_{os.path.basename(fc)}')
    #ADD FIELD de texto
    arcpy.AddField_management(output, 'OBS', 'TEXT')
    #CALCULATE FIELD de texto, se o NEAR_DIST for 0, escreva "Tema sobrepoe a LT", else, nao faça nada
    expression = "if !NEAR_DIST! == 0: 'Tema sobrepoe a LT'"
    arcpy.CalculateField_management(output, 'OBS', expression, "PYTHON")
    


'''
def fxservidaoxponto(fc):
    dissolved_fc = dissolve(fc)
    arcpy.Near_analysis(dissolved_fc, fx_servidao, '10000')
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(dissolved_fc, fr"fsd_10km", expression, "PYTHON")
    #join !NEAR_FID! com lt e pegar o nome da lt
    joinedfc = arcpy.management.AddJoin(in_layer_or_view=dissolved_fc, in_field='NEAR_FID', join_table=lt, join_field='FID')
    arcpy.CopyFeatures_management(joinedfc, os.path.join(workspace_final, os.path.basename(fr"Servidao_Near_{fc}")))

def fxservicoxponto(fc):
    dissolved_fc = dissolve(fc)
    arcpy.Near_analysis(dissolved_fc, fx_servico, '10000')
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(dissolved_fc, fr"fsd_10km", expression, "PYTHON")
    #join !NEAR_FID! com lt e pegar o nome da lt
    joinedfc = arcpy.management.AddJoin(in_layer_or_view=dissolved_fc, in_field='NEAR_FID', join_table=lt, join_field='FID')
    arcpy.CopyFeatures_management(joinedfc, os.path.join(workspace_final, os.path.basename(fr"Servico_Near_{fc}")))

def nearpolygon (fc,buffer):
    dissolved_fc = dissolve(fc)
    arcpy.Near_analysis(dissolved_fc, lt, buffer)
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(dissolved_fc, fr"lt{buffer[:2]}km", expression, "PYTHON")
    #join !NEAR_FID! com lt e pegar o nome da lt
    joinedfc = arcpy.management.AddJoin(in_layer_or_view=dissolved_fc, in_field='NEAR_FID', join_table=lt, join_field='FID')
    arcpy.CopyFeatures_management(joinedfc, os.path.join(workspace_final, os.path.basename(fr"Polygon_Near_{fc}")))
'''

#FIM DAS FUNÇÕES GEOMETRICAS

#FUNCOES DE ATRIBUTOS  #####NOTA, ADICIONAR A FIELD DO NEAR_DIST na lista de fields to keep
def toexcel(fc):
    #EXCEL
    campos_selecionados = fields(fc)
    # Obter os nomes originais dos campos
    desc = arcpy.Describe(fc)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]
    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(fc, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    #verificar se o data frame está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros para esse tema na área de estudo"]})
    else:
        

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

