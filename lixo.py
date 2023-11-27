import arcpy
import os.path
import pandas as pd
import numpy as np

arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False


lt_inteira = arcpy.GetParameterAsText(0)#linha de transmissão previa
circuito_duplo = arcpy.GetParameterAsText(1)#insira a coluna que divide os circuitos
vert_inicial = arcpy.GetParameterAsText(2)#a linha começa no vertice 01 ou 02?
fx_interesse = arcpy.GetParameterAsText(3)#largura da faixa de interesse
bdgis = arcpy.GetParameterAsText(4)#insira o endereço do banco de dados GIS
temas_extra = arcpy.GetParameterAsText(5)#multiple values (separados por vírgula) de temas que não estão no banco de dados GIS
fields_extras = arcpy.GetParameterAsText(6)#multiple values (separados por vírgula) de campos extras que não estão no banco de dados GIS
gdb_path = arcpy.GetParameterAsText(7)#caminho do geodatabase final, que terá os temas que estão no banco de dados GIS
pasta_quantitativo = arcpy.GetParameterAsText(8)#pasta onde serão salvos os arquivos excel
atualizar = arcpy.GetParameterAsText(9)
atualizar_vao = arcpy.GetParameterAsText(10)
junkspace = arcpy.GetParameterAsText(11)
divisao_estadual = r'C:\Users\anderson.souza\Downloads\BR_UF_2022\BR_UF_2022.shp'
arcpy.env.workspace = gdb_path
feature_datasets = arcpy.ListDatasets()

if 'Quantitativo' not in feature_datasets:
    arcpy.CreateFeatureDataset_management(gdb_path, 'Quantitativo', arcpy.Describe(lt_inteira).spatialReference)
else:
    pass
gdb_quantitativo = os.path.join(gdb_path, 'Quantitativo')
#verifica se a pasta junkspace esta vazia, se não estiver, deleta tudo
if os.listdir(junkspace) != []:
    for file in os.listdir(junkspace):
        os.remove(os.path.join(junkspace, file))


def criavao(shape_lt, fx_interesse,vert_inicial):
    # Split at Vertices
    output_split = r'in_memory\"SplitVertices"'
    arcpy.SplitLine_management(shape_lt, output_split)

    # Criar novo campo "Sequencial"
    campo_sequencial = 'Sequencial'
    arcpy.management.AddField(output_split, campo_sequencial, 'LONG')
    if vert_inicial == 'Inicia no Vértice 0':
        vert_inicial = 0
    elif vert_inicial == 'Inicia no Vértice 1':
        vert_inicial = 1
    # Enumerar os registros sequencialmente
    with arcpy.da.UpdateCursor(output_split, campo_sequencial) as cursor:
        for i, row in enumerate(cursor,start=vert_inicial):
            row[0] = i
            cursor.updateRow(row)

    # Criar novo campo "Vertices" e preenchê-lo com a enumeração
    campo_vertices = 'Vertices'
    arcpy.management.AddField(output_split, campo_vertices, 'TEXT', field_length=20)

    with arcpy.da.UpdateCursor(output_split, [campo_sequencial, campo_vertices]) as update_cursor:
        for row in update_cursor:
            sequencia = row[0]
            if sequencia > 0:
                valor_anterior = f"V{sequencia:02d}"
                valor_atual = f"V{sequencia + 1:02d}"
                row[1] = f"{valor_anterior}-{valor_atual}"
            else:
                row[1] = f"V{sequencia:02d}-V{sequencia + 1:02d}"
            update_cursor.updateRow(row)

    # Salvar a feature class no geodatabase de saída com o nome "Diretriz_Gerada"
    try:
        output_diretriz_gerada = arcpy.CopyFeatures_management(output_split, os.path.join(gdb_path,'Dados_Caruso','Vao_LT'))
    except:
        #delete feature class
        arcpy.management.Delete(os.path.join(gdb_path,'Dados_Caruso','Vao_LT'))
        output_diretriz_gerada = arcpy.CopyFeatures_management(output_split, os.path.join(gdb_path,'Dados_Caruso','Vao_LT'))

    #largura da faixa de servidao em metros
    fs_distancia = str(float(fx_interesse)/2)

    # Caminho completo para o arquivo shapefile do buffer
    output_buffer_saida = r'in_memory\"faixa_servidao_buffer"'

    # Salvar o buffer como shapefile
    arcpy.Buffer_analysis(output_diretriz_gerada, output_buffer_saida, fs_distancia)

    # Criar a feature class em memória
    no_over = arcpy.management.CreateFeatureclass(
        "in_memory",  # Caminho "in_memory" indica que a feature class será criada em memória
        "Faixa_Servidao",  # Nome da feature class
        "POLYGON",  # Tipo de geometria (neste caso, polígono)
        None,  # Template - pode ser None para não usar um template
        "DISABLED",  # Habilitar M (Medidas) - neste caso, está desabilitado
        "DISABLED",  # Habilitar Z (Elevação) - neste caso, está desabilitado
        'PROJCS["SIRGAS_2000_UTM_Zone_22S",GEOGCS["GCS_SIRGAS_2000",DATUM["D_SIRGAS_2000",SPHEROID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",10000000.0],PARAMETER["Central_Meridian",-51.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]];-5120900 1900 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision',
        '',  # Configurações do cluster - vazio neste caso
        0,  # Recursos do tamanho do arquivo - 0 neste caso para uso padrão
        0,  # Armazenamento do limite do arquivo - 0 neste caso para uso padrão
        0,  # Armazenamento do limite de espaço único - 0 neste caso para uso padrão
    )

    # Criar os campos "Sequencial" e "Vertices" na feature class "no_over"
    campo_sequencial = 'Sequencial'
    campo_vertices = 'Vertices'
    arcpy.management.AddField(no_over, campo_sequencial, 'LONG')
    arcpy.management.AddField(no_over, campo_vertices, 'TEXT', field_length=20)

    # Copiar os valores dos campos "Sequencial" e "Vertices" da feature class "Diretriz_Gerada" para a feature class "no_over"
    campos_copiar = [campo_sequencial, campo_vertices]
    with arcpy.da.UpdateCursor(no_over, campos_copiar) as update_cursor:
        for row in update_cursor:
            seq_valor = row[0]  # Valor do campo Sequencial na feature class "Diretriz_Gerada"
            vert_valor = row[1]  # Valor do campo Vertices na feature class "Diretriz_Gerada"
            # Copiar os valores para a feature class "no_over"
            row[0] = seq_valor
            row[1] = vert_valor
            update_cursor.updateRow(row)

    sl_fx_serv = arcpy.management.SelectLayerByAttribute(in_layer_or_view=output_buffer_saida, selection_type='NEW_SELECTION', where_clause='Sequencial=0')
    feature_copiada = os.path.join(gdb_path,'Dados_Caruso','feature_copiada')
    copyfzero = arcpy.management.CopyFeatures(sl_fx_serv, feature_copiada, '', None, None, None)
    no_over_final = arcpy.management.Append(inputs=copyfzero, target=no_over, schema_type='NO_TEST')
    #deleta a feature class copiada
    arcpy.management.Delete(feature_copiada)

    cursor = arcpy.SearchCursor(output_buffer_saida)

    for row in cursor:
        vao_row = row.getValue('Sequencial')
        sl_getcount = arcpy.management.SelectLayerByAttribute(in_layer_or_view=output_buffer_saida, selection_type='NEW_SELECTION', where_clause=f'"Sequencial"={vao_row}')
        copy_getcount = arcpy.management.CopyFeatures(sl_getcount, "teste2.shp", '', None, None, None) 
        erase_getcount = arcpy.analysis.Erase(in_features=copy_getcount, erase_features=no_over_final, out_feature_class=f'in_memory\\erase_copy_{vao_row}')

        # Create a FieldMappings object and add the necessary field mappings
        field_mappings = arcpy.FieldMappings()
        field_mappings.addTable(no_over_final)
        field_mappings.addTable(erase_getcount)

        # Append the features from erase_getcount to no_over_final using the defined field mappings
        arcpy.management.Append(inputs=erase_getcount, target=no_over_final, schema_type='NO_TEST', field_mapping=field_mappings)



    # Salvar a feature class no geodatabase de saída com nome "Faixa_Servidao"
    try: 
        output_faixa_servidao = arcpy.CopyFeatures_management(no_over, os.path.join(gdb_path,'Dados_Caruso','Vao_FxInteresse'))
    except:
        #delete feature class
        arcpy.management.Delete(os.path.join(gdb_path,'Dados_Caruso','Vao_FxInteresse'))
        output_faixa_servidao = arcpy.CopyFeatures_management(no_over, os.path.join(gdb_path,'Dados_Caruso','Vao_FxInteresse'))
    arcpy.AddMessage('LT e Faixa de Interesse segmentadas geradas com sucesso')
    return output_diretriz_gerada, output_faixa_servidao

def project(gdb,temas_extra):
    arcpy.env.workspace = gdb
    feature_datasets = arcpy.ListDatasets()
    if 'Temas' not in feature_datasets:
        arcpy.CreateFeatureDataset_management(gdb, 'Temas', arcpy.Describe(lt_inteira).spatialReference)
    arcpy.env.workspace = bdgis
    feature_classes = arcpy.ListFeatureClasses()
    if temas_extra == '':
        for fc in feature_classes:
            #intersect entre a fc e a divisão estadual
            if 'UF' in fields(fc):
                fc_intersect = arcpy.analysis.Intersect(in_features=[fc, divisao_estadual], out_feature_class=os.path.join(junkspace,fr'div_{fc}'))
                arcpy.conversion.FeatureClassToFeatureClass(fc_intersect, os.path.join(gdb, 'Temas'),fc)
            elif 'UF' not in fields(fc):
                arcpy.conversion.FeatureClassToFeatureClass(fc, os.path.join(gdb, 'Temas'),fc)
        arcpy.AddMessage('Temas adicionados ao geodatabase local')
    else:
        temas_extra_name = os.path.basename(temas_extra)
        if 'UF' in fields_extras:
            fc_intersect = arcpy.analysis.Intersect(in_features=[temas_extra, divisao_estadual], out_feature_class=os.path.join(junkspace,fr'div_{temas_extra}'))
            arcpy.conversion.FeatureClassToFeatureClass(fc_intersect, os.path.join(gdb, 'Temas'),temas_extra_name)
        elif 'UF' not in fields_extras:
            arcpy.conversion.FeatureClassToFeatureClass(temas_extra, os.path.join(gdb, 'Temas'),temas_extra_name)

def dissolve(fc):
    arcpy.env.overwriteOutput = True
    filename = os.path.basename(fc)
    if '.shp' in filename:
        filename_tema_extra=filename.split('.shp')[0]
    else:
        filename_tema_extra=filename
    fields_interesse = []
    if filename == 'Aerodromos_ANAC_2022':
        fields_interesse.extend(['Codigo_OAC','Tipo','CIAD'])
    elif filename == 'Aerogeradores_ANEEL_2023':
        fields_interesse.extend(['NOME_EOL','EOL_VERSAO'])
    elif filename == 'Aglomerado_Rural_IBGE_2021':
        fields_interesse.extend(['nome'])
    elif filename == 'AI_Riqueza_CEMAVE_2019':
        fields_interesse = []
    elif filename == 'Aldeias_Indigenas_FUNAI_2023':
        fields_interesse.extend(['nomuf','nome_aldei'])
    if filename == filename_tema_extra:
        fields_interesse = [field.name for field in arcpy.ListFields(fc)]
    

    output_path = os.path.join(junkspace, f"{filename}_dissolved")
    output_path = arcpy.CreateUniqueName(output_path)
    if 'UF' in [field.name for field in arcpy.ListFields(fc)]:
        fields_interesse = fields_interesse + ['UF']
        output = arcpy.Dissolve_management(fc, output_path, fields_interesse)
    else:
        output = arcpy.Dissolve_management(fc, output_path, fields_interesse)
    return output, fields_interesse

def fields(fc):
    filename = os.path.basename(fc)
    if '.shp' in filename:
        filename_tema_extra = filename.split('.shp')[0]
    else:
        filename_tema_extra = filename

        fields_to_keep = []
        # caso o tema esteja nessa lista, ele
        if filename == 'Aerodromos_ANAC_2022':
            fields_to_keep = dissolve(fc)[1] + ['UF', 'Distancia', 'Vertices']
        elif filename == 'Aerogeradores_ANEEL_2023':
            fields_to_keep = dissolve(fc)[1] + ['UF', 'Distancia', 'Vertices']
        elif filename == 'Aglomerado_Rural_IBGE_2021':
            fields_to_keep = dissolve(fc)[1] + ['Distancia', 'Vertices']
        elif filename == 'AI_Riqueza_CEMAVE_2019':
            fields_to_keep = dissolve(fc)[1] + ['Distancia', 'Vertices', 'Extensao', 'Area']
        elif filename == 'Aldeias_Indigenas_FUNAI_2023':
            fields_to_keep = dissolve(fc)[1] + ['Distancia', 'Vertices']
        if filename == filename_tema_extra:
            fc = os.path.join(gdb_path, 'Temas', filename)
            field_extras_split = fields_extras.split(';')
            fields_to_keep = dissolve(fc)[1] + field_extras_split

        return fields_to_keep


def ltxfeature(fc, lt):
    dissolved_fc = dissolve(fc)[0]
    filename = os.path.basename(fc)
    if "Vertices" in fields(fc):
        if arcpy.Describe(fc).shapeType == 'Polyline' or arcpy.Describe(fc).shapeType == 'PolylineM' or arcpy.Describe(fc).shapeType == 'PolylineZ':         
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='POINT')
            arcpy.AddField_management(output, 'Eixo_X', 'FLOAT')
            arcpy.CalculateField_management(output, 'Eixo_X', '!shape.firstPoint.X!', 'PYTHON')
            arcpy.CalculateField_management(output, 'Eixo_Y', '!shape.firstPoint.Y!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon' or arcpy.Describe(fc).shapeType == 'PolygonM' or arcpy.Describe(fc).shapeType == 'PolygonZ':
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='LINE')
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')
    elif "Vertices" not in fields(fc):
        arcpy.env.workspace = junkspace
        if arcpy.Describe(fc).shapeType == 'Polyline' or arcpy.Describe(fc).shapeType == 'PolylineM' or arcpy.Describe(fc).shapeType == 'PolylineZ':
            lt=arcpy.management.Dissolve(in_features=lt, out_feature_class='dissolved_lt')
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='POINT')
            arcpy.AddField_management(output, 'Eixo_X', 'FLOAT')
            arcpy.CalculateField_management(output, 'Eixo_X', '!shape.firstPoint.X!', 'PYTHON')
            arcpy.CalculateField_management(output, 'Eixo_Y', '!shape.firstPoint.Y!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon'or arcpy.Describe(fc).shapeType == 'PolygonM' or arcpy.Describe(fc).shapeType == 'PolygonZ':
            lt=arcpy.management.Dissolve(in_features=lt, out_feature_class='dissolved_lt')
            output = arcpy.analysis.Intersect(in_features=[lt, dissolved_fc], out_feature_class=os.path.join(gdb_quantitativo,'LT_x_'+filename), output_type='LINE')
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')

def fxinteressexfeature(fc, fx_interesse):
    dissolved_fc = dissolve(fc)[0]
    filename = os.path.basename(fc)
    if "Vertices" in fields(fc):
        if arcpy.Describe(fc).shapeType == 'Polyline' or arcpy.Describe(fc).shapeType == 'PolylineM' or arcpy.Describe(fc).shapeType == 'PolylineZ':
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Extensao', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon' or arcpy.Describe(fc).shapeType == 'PolygonM' or arcpy.Describe(fc).shapeType == 'PolygonZ':
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Area', '!shape.area@hectares!', 'PYTHON')
    elif "Vertices" not in fields(fc):
        arcpy.env.workspace = junkspace
        if arcpy.Describe(fc).shapeType == 'Polyline' or arcpy.Describe(fc).shapeType == 'PolylineM' or arcpy.Describe(fc).shapeType == 'PolylineZ':
            fx_interesse=arcpy.management.Dissolve(in_features=fx_interesse, out_feature_class='dissolved_fx')
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Extensao', 'FLOAT')
            arcpy.CalculateField_management(output, 'Extensao', '!shape.length@kilometers!', 'PYTHON')
        elif arcpy.Describe(fc).shapeType == 'Polygon' or arcpy.Describe(fc).shapeType == 'PolygonM' or arcpy.Describe(fc).shapeType == 'PolygonZ':
            fx_interesse=arcpy.management.Dissolve(in_features=fx_interesse, out_feature_class='dissolved_fx')
            output = arcpy.Intersect_analysis([fx_interesse, dissolved_fc], os.path.join(gdb_quantitativo,'FxInteresse_x_'+filename))
            arcpy.AddField_management(output, 'Area', 'FLOAT')
            arcpy.CalculateField_management(output, 'Area', '!shape.area@hectares!', 'PYTHON')

def ltnearfeature(fc,buffer,lt):
    dissolved_fc = dissolve(fc)[0]
    arcpy.analysis.Near(in_features=dissolved_fc, near_features=lt, search_radius=buffer)
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(dissolved_fc, 'Distancia', expression, "PYTHON")
    joinedfc = arcpy.management.JoinField(in_data=dissolved_fc, in_field='NEAR_FID', join_table=lt, join_field='OBJECTID')
    arcpy.CalculateField_management(joinedfc, 'OBS', expression, "PYTHON")
    selectfc = arcpy.management.SelectLayerByAttribute(in_layer_or_view=joinedfc, selection_type="NEW_SELECTION", where_clause="NEAR_FID <> -1")
    output = arcpy.CopyFeatures_management(selectfc, fr'{gdb_quantitativo}\LT_Near_x_{os.path.basename(fc)}')
    arcpy.AddField_management(output, 'OBS', 'TEXT')
    expression = """def neardist(x):
        if x == 0:
            return 'Tema Sobrepõe a LT (Verificar aba de sobreposição)'
        else:
            return ' '"""
    arcpy.management.CalculateField(in_table=output, field='OBS', expression='neardist(!NEAR_DIST!)', code_block=expression)

def toexcel(fc, related_field):
    campos_fc = [campo.name for campo in arcpy.ListFields(fc)]
    campos_related_field = fields(os.path.join(gdb_path, 'Temas', related_field))

    # Encontrar a interseção entre as colunas do fc e do related_field
    colunas_comuns = [campo for campo in campos_fc if campo in campos_related_field]
    if 'UF' in campos_related_field:
        colunas_comuns.append('UF')
    if 'OBS' in campos_fc:
        colunas_comuns.append('OBS')

    if not colunas_comuns:
        arcpy.AddWarning(f"Não há colunas comuns entre {os.path.basename(fc)} e {related_field}")
        return

    # Remove duplicate fields
    colunas_comuns = list(set(colunas_comuns))

    # Obter os dados apenas das colunas comuns
    table = arcpy.da.TableToNumPyArray(fc, colunas_comuns, skip_nulls=False)
    df = pd.DataFrame(table)  # Inicializa a variável df com os dados da tabela

    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros para esse tema na área de estudo"]})

    excel_saida = os.path.join(pasta_quantitativo, f'{os.path.basename(fc)}.xlsx')
    df.dropna(axis=1, how='all', inplace=True)
    
    df.to_excel(excel_saida, index=False)
    #apaga todas as colunas que não tem informação
    


if atualizar_vao == 'true':
    vao = criavao(lt_inteira, fx_interesse, vert_inicial)
    lt = vao[0]
    fx_interesse = vao[1]
else: 
    lt = os.path.join(gdb_path, 'Dados_Caruso','Vao_LT')
    fx_interesse = os.path.join(gdb_path, 'Dados_Caruso','Vao_FxInteresse')

if atualizar == 'true':
    project(gdb_path, temas_extra)
else:
    pass

arcpy.env.workspace = os.path.join(gdb_path, 'Temas')

temas = arcpy.ListFeatureClasses()
for tema in temas:
    #conta quantos temas tem na pasta Temas
    count = len(temas)
    #faz um add mensage com o andamento do processo
    arcpy.AddMessage(f'Processando {tema} ({temas.index(tema)+1} de {count})')
    # Check if the feature class is "Unidade de Conservação"
    if tema == "Unidade de Conservação":
        ltnearfeature(os.path.join(gdb_path, 'Temas', tema), '50000', lt)
    elif 'Distancia' in fields(tema):
        ltnearfeature(os.path.join(gdb_path, 'Temas', tema), '10000', lt)
    
    # Call ltxfeature and fxinteressexfeature functions
    ltxfeature(os.path.join(gdb_path, 'Temas', tema), lt)
    fxinteressexfeature(os.path.join(gdb_path, 'Temas', tema), fx_interesse)

arcpy.env.workspace = os.path.join(gdb_path, 'Quantitativo')
temas = arcpy.ListFeatureClasses()

for tema in temas:
    lastname = tema.split('_x_')[-1]
    toexcel(os.path.join(gdb_path, 'Quantitativo', tema),lastname)
    arcpy.AddMessage(f'Planilha de quantitativo do tema {tema} gerado com sucesso!')
