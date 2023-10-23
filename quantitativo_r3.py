import arcpy
import os
import pandas as pd
import numpy as np

arcpy.env.overwriteOutput = True

# Caminho para o geodatabase de entrada
gdb_base = fr'C:\Users\anderson.souza\Documents\CHESF\GDB_Dados_Referenciais\PL_LOTE_02_03_Clipped.gdb\Dados_Referenciais_F22'
arcpy.env.workspace = fr'C:\Users\anderson.souza\Documents\CHESF\Piloto_quantitativo\workspace'# Defina o caminho correto para sua pasta de trabalho
gdb_saida = fr'C:\Users\anderson.souza\Documents\CHESF\Piloto_quantitativo\gdb_saida\quantitativo_fuso22.gdb'# Caminho para o geodatabase de saída
excelfiles = fr'C:\Users\anderson.souza\Documents\CHESF\Piloto_quantitativo\excel'


input_diretriz = os.path.join(gdb_base, 'Diretriz_Lote02_F22_18092023')
input_municipios = os.path.join(gdb_base, 'Divisao_Municipal_IBGE_2022_1_clip')
input_localidades = os.path.join(gdb_base, 'Localidades_IBGE_2010_1_clip')
input_Linhas_Transmissao = os.path.join(gdb_base, "Linhas_de_Transmissão__Base_Existente_EPE_1_clip")
input_rodovias = os.path.join(gdb_base, "Rodovias_DNIT") ###NAO SEI AINDA
input_ferrovias = os.path.join(gdb_base, "Ferrovias_DNIT_2020_1_clip")
input_Gas_Trans = os.path.join(gdb_base, "Gasodutos_de_transporte_EPE_1_clip")
input_Gas_Dis = os.path.join(gdb_base, "Gasodutos_de_distribuição_EPE_1_clip")
input_Dutovias = os.path.join(gdb_base, "Dutovias_Gas_Oleo_Minerio_ANP") # NAO SEI AINDA
input_Adutoras = os.path.join(gdb_base, "Adutoras_SNIRH_ANA_Atlas_2021") # FALTA NO GDB
input_hidro = os.path.join(gdb_base, "Hidrografia_Adaptada_Lote02_F22")
input_aerodromos = os.path.join(gdb_base, "Area_Aerodromos_DECEA_2023_1_clip")
input_Quilombolas = os.path.join(gdb_base, "Quilombolas_INCRA_2023_1_clip")
input_Cavidades = os.path.join(gdb_base, "Cavernas_CANIE_2022_1_clip")
input_sitios = os.path.join(gdb_base, "Sitios_arqueologicos_IPHAN_2023_1_clip")
input_ocorrencias = os.path.join(gdb_base, "Ocorrencias_Fossiliferas_CPRM_2023_1_clip")
input_TIs = os.path.join(gdb_base, "Terras_Indigenas_Homologadas_FUNAI_2023_1_clip")
input_UCs = os.path.join(gdb_base, "Unidades_Conservacao_MMA_2023_1_clip")
input_ZAs = os.path.join(gdb_base, "ZAs_GO_2023_1_clip")
input_APCBs_MA = os.path.join(gdb_base, "APCB_Cerrado_Pantanal_MMA_2018_1_clip")
input_APCBs_CEPA = os.path.join(gdb_base, "APCB_Cerrado_Pantanal_MMA_2018_1_clip")
input_assentamentos = os.path.join(gdb_base, "Assentamento_INCRA_2023_1_clip")
input_processos_minerarios = os.path.join(gdb_base, "Recursos_Minerários_ANM_2023_1_clip")
input_vegetacao = os.path.join(gdb_base, "Vegetacao_IBGE_1250000_2021_1_clip")
input_relevo = os.path.join(gdb_base, "Declividade_Caruso")
input_uso = os.path.join(gdb_base, "Uso_Solo_Caruso")
input_edificacoes = os.path.join(gdb_base, "Edificacoes_Caruso")
input_vertices = os.path.join(gdb_base, "Vertices_Caruso")
input_Erodibilidade = os.path.join(gdb_base, "Erodibilidade_Caruso")

input_list = [input_diretriz, input_municipios, input_localidades, input_Linhas_Transmissao, input_rodovias, input_ferrovias, input_Gas_Trans, input_Gas_Dis, input_Dutovias, 
              input_Adutoras, input_hidro, input_aerodromos, input_Quilombolas, input_Cavidades, input_sitios, input_ocorrencias, input_TIs, input_UCs, input_ZAs, input_APCBs_MA, 
              input_assentamentos, input_processos_minerarios, input_vegetacao, input_relevo, input_uso, input_edificacoes, input_vertices, input_Erodibilidade]

feature_classes = arcpy.ListFeatureClasses("*", "ALL", gdb_base)

def diretriz():
    # Split at Vertices
    output_split = "SplitVertices"
    arcpy.SplitLine_management(input_diretriz, output_split)

    # Criar novo campo "Sequencial"
    campo_sequencial = 'Sequencial'
    arcpy.management.AddField(output_split, campo_sequencial, 'LONG')

    # Enumerar os registros sequencialmente
    with arcpy.da.UpdateCursor(output_split, campo_sequencial) as cursor:
        for i, row in enumerate(cursor):
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
    output_diretriz_gerada = os.path.join(gdb_saida, 'Diretriz_Gerada')
    arcpy.CopyFeatures_management(output_split, output_diretriz_gerada)

    #largura da faixa de servidao em metros
    fs_distancia = arcpy.GetParameterAsText(0)

    # Nome do arquivo shapefile (sem extensão) para o buffer
    nome_shapefile_buffer = 'faixa_servidao_buffer'

    # Caminho completo para o arquivo shapefile do buffer
    output_buffer_saida = os.path.join(arcpy.env.workspace, f"{nome_shapefile_buffer}.shp")

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
    copyfzero = arcpy.management.CopyFeatures(sl_fx_serv, 'feature_copiada', '', None, None, None)
    no_over_final = arcpy.management.Append(inputs=copyfzero, target=no_over, schema_type='NO_TEST')

    cursor = arcpy.SearchCursor(output_buffer_saida)

    for row in cursor:
        vao_row = row.getValue('Sequencial')
        sl_getcount = arcpy.management.SelectLayerByAttribute(in_layer_or_view=output_buffer_saida, selection_type='NEW_SELECTION', where_clause=f'"Sequencial"={vao_row}')
        copy_getcount = arcpy.management.CopyFeatures(sl_getcount, fr"C:\Users\anderson.souza\Documents\CHESF\Piloto_quantitativo\workspace\teste2.shp", '', None, None, None) 
        erase_getcount = arcpy.analysis.Erase(in_features=copy_getcount, erase_features=no_over_final, out_feature_class='erase_copy')

        # Create a FieldMappings object and add the necessary field mappings
        field_mappings = arcpy.FieldMappings()
        field_mappings.addTable(no_over_final)
        field_mappings.addTable(erase_getcount)

        # Append the features from erase_getcount to no_over_final using the defined field mappings
        arcpy.management.Append(inputs=erase_getcount, target=no_over_final, schema_type='NO_TEST', field_mapping=field_mappings)

    # Salvar a feature class no geodatabase de saída com nome "Faixa_Servidao"
    output_faixa_servidao = os.path.join(gdb_saida, 'Faixa_Servidao')
    arcpy.CopyFeatures_management(no_over, output_faixa_servidao)
    return output_diretriz_gerada, output_faixa_servidao

###variáveis globais
output_diretriz_gerada = diretriz()[0]
output_faixa_servidao = diretriz()[1]

def municipios():
    # Realizar o intersect entre os shapefiles
    output_intersect = arcpy.Intersect_analysis([input_municipios, output_diretriz_gerada], "in_memory\\municipios_intersect")

    # Realizar o dissolve por NM_MUN e SIGLA_UF
    output_dissolve = os.path.join(gdb_saida, 'Municipios')
    arcpy.Dissolve_management(output_intersect, output_dissolve, ['CD_MUN', 'NM_MUN', 'SIGLA_UF', 'AREA_KM2'])

    # Criar um novo campo chamado extensao
    extensao_field = 'Ext_km'
    arcpy.AddField_management(output_dissolve, extensao_field, 'FLOAT')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.geodesicLength@KILOMETERS!'
    arcpy.CalculateField_management(output_dissolve, extensao_field, expression, 'PYTHON')

    #Exportar para Excel

    # Caminho completo para a tabela de atributos da feição "Municipios"
    municipios_table = os.path.join(gdb_saida, 'Municipios')

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['CD_MUN', 'NM_MUN', 'SIGLA_UF', 'Ext_km']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(municipios_table)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(municipios_table, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "CD_MUN": "Código Município",
        "NM_MUN": "Nome Município",
        "SIGLA_UF": "Unidade Federação",
        "Ext_km": "Extensão em Km"
    }

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Municipios.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def localidades():
    #distancia do buffer em metros
    loc_buffer = 10000

    # realizar o buffer e salvar em memória
    output_buffer10km = "in_memory/buffer10km"
    arcpy.Buffer_analysis(output_diretriz_gerada, output_buffer10km, loc_buffer)

    # selecionar os pontos dentro do buffer
    arcpy.MakeFeatureLayer_management(input_localidades, 'localidades_lyr')
    arcpy.SelectLayerByLocation_management('localidades_lyr', 'COMPLETELY_WITHIN', output_buffer10km)

    # Salvar a camada 'localidades_lyr' em memória
    output_localidades_mem = "in_memory/localidades"

    # Copiar a camada 'localidades_lyr' para a camada em memória
    arcpy.CopyFeatures_management('localidades_lyr', output_localidades_mem)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_localidades_mem, output_diretriz_gerada)

    # Recalcular o campo "NEAR_FID"
    with arcpy.da.UpdateCursor(output_localidades_mem, ["NEAR_FID"]) as cursor:
        for row in cursor:
            near_fid = row[0]
            row[0] = near_fid + 1
            cursor.updateRow(row)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_localidades_mem, "NEAR_DIST", expression, "PYTHON")

    # Nome do campo "Vertices" no shapefile "Diretriz_Gerada"
    campo_vertices_diretriz = "Vertices"

    # Realizar o relacionamento entre os dados com base no campo "NEAR_FID" e "Sequencial"
    arcpy.JoinField_management(output_localidades_mem, "NEAR_FID", output_diretriz_gerada, "Sequencial", [campo_vertices_diretriz])

    # Salvar a feature class no geodatabase de saída
    output_localidades = os.path.join(gdb_saida, 'Localidades')

    # Realizar o Dissolve na camada em memória
    arcpy.Dissolve_management(output_localidades_mem, output_localidades, dissolve_field="tipolocali;identifica;NEAR_DIST;Vertices")

    #Exportar para Excel

    # Caminho completo para a tabela de atributos da feição Localidades
    localidades_table = os.path.join(gdb_saida, 'Localidades')

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['tipolocali', 'identifica', 'NEAR_DIST', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(localidades_table)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "tipolocali": "Tipo de Localidade",
        "identifica": "Identificação",
        "NEAR_DIST": "Menor Distância (km)",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(localidades_table, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Localizades.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def linhas_transmissao():

    # Criar camada em memória a partir do shapefile de Faixa Servidao
    arcpy.MakeFeatureLayer_management(output_faixa_servidao, "faixa_servidao_lyr")

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("faixa_servidao_lyr", "INTERSECT", input_Linhas_Transmissao)

    # Nome da feature class resultante do Select By Location
    output_selected_Lts = "in_memory/SelectedLts"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("faixa_servidao_lyr", output_selected_Lts)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_Lts = "in_memory/SpatialJoinResult"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_Lts, input_Linhas_Transmissao, output_spatial_join_Lts, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Dissolve pelos campos "Vertices" e "Nome"
    output_dissolve_Lts = "in_memory/DissolveResult"
    arcpy.Dissolve_management(output_spatial_join_Lts, output_dissolve_Lts, ["Vertices", "Nome"])

    # Nome da feature class de linhas de transmissão com vértices
    output_linhas_transmissao = os.path.join(gdb_saida, 'Linhas_Transmissao')

    # Exportar a feature class resultante do Dissolve para o geodatabase de saída
    arcpy.CopyFeatures_management(output_dissolve_Lts, output_linhas_transmissao)

    #Exportar para Excel

    # Caminho completo para a tabela de atributos da feição Localidades
    LTs_table = os.path.join(gdb_saida, 'Linhas_Transmissao')

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Nome', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(LTs_table)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(LTs_table, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Linhas_Transmissao.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def rodovias ():
    # Criar camada em memória a partir do shapefile de Faixa Servidao
    arcpy.MakeFeatureLayer_management(output_faixa_servidao, "rod_lyr")

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("rod_lyr", "INTERSECT", input_rodovias)

    # Nome da feature class resultante do Select By Location
    output_selected_rod = "in_memory/Selectedrod"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("rod_lyr", output_selected_rod)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_rod = "in_memory/SpatialJoinResultRodo"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_rod, input_rodovias, output_spatial_join_rod, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Adicionar novo campo "Sigla_Rodovia" do tipo string
    campo_sigla_rodovia = "Sigla_Rodovia"
    arcpy.AddField_management(output_spatial_join_rod, campo_sigla_rodovia, "TEXT", field_length=50)

    # Atualizar o campo "Sigla_Rodovia" com os valores desejados
    with arcpy.da.UpdateCursor(output_spatial_join_rod, ["ds_jurisdi", "vl_br", "sg_uf", campo_sigla_rodovia]) as cursor:
        for row in cursor:
            if row[0] == "Federal":
                row[3] = "Rodovia BR-" + row[1]
            else:
                row[3] = "Rodovia " + row[2] + "-" + row[1]
            cursor.updateRow(row)

    #Criar camada em memória para o intersect
    output_intersect_rod_man = arcpy.Intersect_analysis([output_spatial_join_rod, input_municipios], "in_memory\\rod_intersect")

    # Verificar se a feature class já existe e excluí-la
    if arcpy.Exists(output_spatial_join_rod):
        arcpy.Delete_management(output_spatial_join_rod)

    # Realizar o dissolve 
    output_dissolve_rod = os.path.join(gdb_saida, 'Rodovias')
    arcpy.Dissolve_management(output_intersect_rod_man, output_spatial_join_rod, ['Sequencial', 'Vertices', 'vl_br', 'nm_tipo_tr', 'vl_codigo', 'ds_jurisdi', 'Sigla_Rodovia','NM_MUN', 'SIGLA_UF'])

    # Nome da feature class de linhas de transmissão com vértices
    output_Rodovias = os.path.join(gdb_saida, 'Rodovias')

    # Exportar a feature class resultante para o geodatabase de saída
    arcpy.CopyFeatures_management(output_spatial_join_rod, output_Rodovias)

    #Exportar para Excel

    # Caminho completo para a tabela de atributos da feição Localidades
    rod_table = os.path.join(gdb_saida, 'Rodovias')

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Sigla_Rodovia', 'ds_jurisdi', 'NM_MUN', 'SIGLA_UF', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(rod_table)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Sigla_Rodovia": "Benfeitoria",
        "ds_jurisdi": "Jurisdição",
        "NM_MUN": "Município",
        "Vertices": "Vértices",
        }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(rod_table, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Preencher o campo 'Município' com NM_MUN + "-" + SIGLA_UF
    df['Município'] = df['Município'] + '-' + df['SIGLA_UF']

    # Remover a coluna 'SIGLA_UF' do dataframe
    df.drop('SIGLA_UF', axis=1, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Benfeitoria', 'Jurisdição', 'Município', 'Vértices']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Rodovias.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def ferrovias():

    # Criar camada em memória a partir do shapefile de Faixa Servidao
    arcpy.MakeFeatureLayer_management(output_faixa_servidao, "fer_lyr")

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("fer_lyr", "INTERSECT", input_ferrovias)

    # Nome da feature class resultante do Select By Location
    output_selected_fer = "in_memory/Selectedfer"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("fer_lyr", output_selected_fer)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_fer = "in_memory/SpatialJoinResultfer"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_fer, input_ferrovias, output_spatial_join_fer, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Nome da feature class de linhas de transmissão com vértices
    output_ferrovias = os.path.join(gdb_saida, 'Ferrovias')

    # Exportar a feature class resultante do Dissolve para o geodatabase de saída
    arcpy.CopyFeatures_management(output_spatial_join_fer, output_ferrovias)

    #Exportar para Excel

    # Caminho completo para a tabela de atributos da feição Localidades
    fer_table = os.path.join(gdb_saida, 'Ferrovias')

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['sigla', 'tip_situac', 'municipio', 'uf', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(fer_table)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "sigla": "Benfeitoria",
        "tip_situac": "Situação",
        "municipio": "Município",
        "uf": "UF",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(fer_table, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Ferrovias.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def gasoduto_transporte():
        
    # GASODUTOS TRANSPORTE (Executa o código selecionando apenas as feições existêntes, deixando as planejadas e em estudo de fora)

    # Criar camada em memória a partir da feature
    arcpy.MakeFeatureLayer_management(input_Gas_Trans, "gas_trans_lyr")

    # Selecionar apenas os registros com Categoria = 'Existente'
    expressao = "Categoria = 'Existente'"
    arcpy.SelectLayerByAttribute_management("gas_trans_lyr", "NEW_SELECTION", expressao)

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("gas_trans_lyr", "INTERSECT", output_faixa_servidao)

    # Nome da feature class resultante do Select By Location
    output_selected_gas_trans = "in_memory/Selected_gas_trans"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("gas_trans_lyr", output_selected_gas_trans)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_gas_trans = "in_memory/SpatialJoinResult_gasTrans"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_gas_trans, output_faixa_servidao, output_spatial_join_gas_trans, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Nome da feature class de linhas de transmissão com vértices
    output_gas = os.path.join(gdb_saida, 'Gasodutos_Transporte')

    # Exportar a feature class resultante do Spatial Join para o geodatabase de saída
    arcpy.CopyFeatures_management(output_spatial_join_gas_trans, output_gas)

    #Exportar para Excel

    # Caminho completo para a tabela de atributos da feição Localidades
    gas_table = os.path.join(gdb_saida, 'Gasodutos_Transporte')

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Nome_Dut_1', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(gas_table)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Nome_Dut_1": "Nome",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(gas_table, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Gasodutos de Transporte que são interceptados pela faixa de serviço."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Gasodutos_Transporte.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def gasoduto_distribuicao():
    # GASODUTOS DISTRIBUIÇÃO

    # Criar camada em memória a partir da feature
    arcpy.MakeFeatureLayer_management(input_Gas_Dis, "gas_dis_lyr")

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("gas_dis_lyr", "INTERSECT", output_faixa_servidao)

    # Nome da feature class resultante do Select By Location
    output_selected_gas_dis = "in_memory/Selected_gas_dis"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("gas_dis_lyr", output_selected_gas_dis)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_gas_dis = "in_memory/SpatialJoinResult_gasdist"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_gas_dis, output_faixa_servidao, output_spatial_join_gas_dis, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Nome da feature class de linhas de transmissão com vértices
    output_gas_dis = os.path.join(gdb_saida, 'Gasodutos_Distribuicao')

    # Exportar a feature class resultante do Spatial Join para o geodatabase de saída
    arcpy.CopyFeatures_management(output_spatial_join_gas_dis, output_gas_dis)

    #Exportar para Excel

    # Caminho completo para a tabela de atributos da feição Localidades
    gas_table = os.path.join(gdb_saida, 'Gasodutos_Distribuicao')

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Distrib', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(gas_table)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Distrib": "Nome da Distribuidora",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(gas_table, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Gasodutos de Distribuição que são interceptados pela faixa de serviço."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Gasodutos_Distribuicao.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def dutovias():
    # DUTOVIAS

    # Criar camada em memória a partir da feature
    arcpy.MakeFeatureLayer_management(input_Dutovias, "duto_lyr")

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("duto_lyr", "INTERSECT", output_faixa_servidao)

    # Nome da feature class resultante do Select By Location
    output_selected_duto = "in_memory/Selected_duto"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("duto_lyr", output_selected_duto)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_duto = "in_memory/SpatialJoinResult_duto"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_duto, output_faixa_servidao, output_spatial_join_duto, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Nome da feature class de linhas de transmissão com vértices
    output_dutovias = os.path.join(gdb_saida, 'Dutovias')

    # Exportar a feature class resultante do Spatial Join para o geodatabase de saída
    arcpy.CopyFeatures_management(output_spatial_join_duto, output_dutovias)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Name', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_dutovias)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Name": "Duto",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_dutovias, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Dutovias que são interceptadas pela faixa de serviço."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Dutovias.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def adutoras():
    # ADUTORAS
    # Criar camada em memória a partir da feature
    arcpy.MakeFeatureLayer_management(input_Adutoras, "adut_lyr")

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("adut_lyr", "INTERSECT", output_faixa_servidao)

    # Nome da feature class resultante do Select By Location
    output_selected_adut = "in_memory/Selected_adut"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("adut_lyr", output_selected_adut)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_adut = "in_memory/SpatialJoinResult_adut"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_adut, output_faixa_servidao, output_spatial_join_adut, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Nome da feature class de linhas de transmissão com vértices
    output_adutoras = os.path.join(gdb_saida, 'Adutoras')

    # Exportar a feature class resultante do Spatial Join para o geodatabase de saída
    arcpy.CopyFeatures_management(output_spatial_join_adut, output_adutoras)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['ADUTORA', 'SITUAÇÃO', 'ESTADO', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_adutoras)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "ADUTORA": "Adutora",
        "SITUAÇÃO": "Situação",
        "ESTADO": "UF",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_adutoras, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Adutoras que são interceptadas pela faixa de serviço."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Adutoras.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def hidrografia():
    # HIDROGRAFIA

    # Criar camada em memória a partir da feature
    arcpy.MakeFeatureLayer_management(input_hidro, "hidro_lyr")

    # Realizar Select By Location para selecionar os segmentos de retas interceptados
    arcpy.SelectLayerByLocation_management("hidro_lyr", "INTERSECT", output_faixa_servidao)

    # Nome da feature class resultante do Select By Location
    output_selected_hidro = "in_memory/Selected_hidro"

    # Exportar o resultado do Select By Location para uma nova feature class
    arcpy.CopyFeatures_management("hidro_lyr", output_selected_hidro)

    # Nome da feature class resultante do Spatial Join
    output_spatial_join_hidro = "in_memory/SpatialJoinResult_hidro"

    # Realizar o Spatial Join entre a faixa de servidão selecionada e as linhas de transmissão selecionadas
    arcpy.SpatialJoin_analysis(output_selected_hidro, output_faixa_servidao, output_spatial_join_hidro, "JOIN_ONE_TO_ONE", "KEEP_ALL")

    # Nome da feature class de linhas de transmissão com vértices
    output_hidro = os.path.join(gdb_saida, 'Hidrografia')

    # Exportar a feature class resultante do Spatial Join para o geodatabase de saída
    arcpy.CopyFeatures_management(output_spatial_join_hidro, output_hidro)

    # Calculando a extensão em metros para cada elemento da hidrografia
    with arcpy.da.UpdateCursor(output_hidro, ['Shape@', 'Exten_m']) as cursor:
        for row in cursor:
            # Para linhas (por exemplo, rios ou córregos)
            if row[0].type == "Polyline":
                exten_metros = row[0].length
                row[1] = exten_metros
            # Para polígonos (por exemplo, lagos ou lagoas)
            elif row[0].type == "Polygon":
                exten_metros = row[0].area
                row[1] = exten_metros
            # Para outros tipos de geometria, defina o valor de exten_metros conforme necessário
            else:
                exten_metros = 0
                row[1] = exten_metros
            cursor.updateRow(row)


    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Vertices', 'tipotrecho', 'nome','Exten_m']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_hidro)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Vertices": "Vértices",
        "tipotrecho": "Tipo",
        "nome": "Nome",
        "Exten_m": "Extensão (m)"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_hidro, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Hidrografia que são interceptados pela faixa de servidão."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Vértices', 'Tipo', 'Nome', 'Extensão (m)']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Hidrografia.xlsx')
    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def aerodromos():
    # AERÓDROMOS

    # Realizar o intersect entre os shapefiles
    output_intersect = "in_memory/aerodromos_intersect"
    arcpy.Intersect_analysis([input_aerodromos, output_faixa_servidao], output_intersect, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    loc_buffer = 10000

    # realizar o buffer e salvar em memória
    output_buffer10km = "in_memory/buffer10kms"
    arcpy.Buffer_analysis(output_faixa_servidao, output_buffer10km, loc_buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_aerodromos, 'aerodromos_lyr')
    arcpy.SelectLayerByLocation_management('aerodromos_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{loc_buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('aerodromos_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'aerodromos_lyr' em memória com um nome diferente
    output_aerodromos_mem = "in_memory/aerodromos_temp"
    arcpy.CopyFeatures_management('aerodromos_lyr', output_aerodromos_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined = "in_memory/aerodromos_combined"
    arcpy.Merge_management([output_intersect, output_aerodromos_mem], output_combined)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_aerodromos = os.path.join(gdb_saida, 'Aerodromos')
    arcpy.CopyFeatures_management(output_combined, output_aerodromos)

    #Exportar para Excel

    campos_selecionados = ['Vertices', 'nom', 'mun', 'uf', 'Zona', 'Area_ha', 'NEAR_DIST']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_aerodromos)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_aerodromos, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Aeródromos e suas Zonas de Proteção em um raio de 10 km da Faixa de Servidão."]})
    else:
        # Lista dos campos selecionados para exportação
        #campos_selecionados = ['Vertices', 'nom', 'mun', 'uf', 'Zona', 'Area_ha', 'NEAR_DIST']

        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_aerodromos)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_aerodromos, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "Vertices": "Vértices",
            "nom": "Nome",
            "mun": "Município",
            "uf": "UF",
            "Zona": "Zona",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Vértices', 'Nome', 'Município', 'UF', 'Zona', 'Área (ha)', 'Menor Distância (km)']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Aerodromos.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def quilombolas():
    #  QUILOMBOLAS
    #Distancia Buffer Territórios Quilombolas
    qui_buffer = 5000

    # realizar o buffer e salvar em memória
    input_Quilombolas_Area = "in_memory/quilombolabuffer5km"
    arcpy.Buffer_analysis(input_Quilombolas, input_Quilombolas_Area, qui_buffer)

    # Realizar o intersect entre os shapefiles
    output_intersect_quilombola5km = "in_memory/quilombola"
    arcpy.Intersect_analysis([input_Quilombolas_Area, output_faixa_servidao], output_intersect_quilombola5km, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_quilombola5km)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_quilombola5km, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_quilombola5km, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_quilombola5km, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    loc_buffer = 10000

    # realizar o buffer e salvar em memória
    output_buffer10kms = "in_memory/buffer10kmss"
    arcpy.Buffer_analysis(output_faixa_servidao, output_buffer10kms, loc_buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_Quilombolas_Area, 'quilombolas_lyr')
    arcpy.SelectLayerByLocation_management('quilombolas_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{loc_buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('quilombolas_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'aerodromos_lyr' em memória com um nome diferente
    output_quilombolas_mem = "in_memory/quilombolas_temp"
    arcpy.CopyFeatures_management('quilombolas_lyr', output_quilombolas_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined = "in_memory/quilombolas_combined"
    arcpy.Merge_management([output_intersect_quilombola5km, output_quilombolas_mem], output_combined)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_quilombolas = os.path.join(gdb_saida, 'Quilombolas')
    arcpy.CopyFeatures_management(output_combined, output_quilombolas)

    #EXPORTAR PARA EXCEL

    campos_selecionados = ['nr_process', 'nm_comunid', 'nm_municip', 'cd_uf', 'Area_ha', 'NEAR_DIST', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_quilombolas)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_quilombolas, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Territórios Quilombolas em um raio de 10 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_quilombolas)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_quilombolas, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "nr_process": "Processo",
            "nm_comunid": "Nome",
            "nm_municip": "Município",
            "cd_uf": "UF",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Processo', 'Nome', 'Município', 'UF', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Quilombolas.xlsx')
    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def cavidades():
    # CAVIDADES

    #Distancia Buffer Cavidades
    cavi_buffer = 250

    # realizar o buffer e salvar em memória
    input_cavi = "in_memory/cavi250m"
    arcpy.Buffer_analysis(input_Cavidades, input_cavi, cavi_buffer)

    # Realizar o intersect entre os shapefiles
    output_intersect_cavi = "in_memory/cavi"
    arcpy.Intersect_analysis([input_cavi, output_faixa_servidao], output_intersect_cavi, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_cavi)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_cavi, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_cavi, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_cavi, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    loc_buffer = 2000

    # realizar o buffer e salvar em memória
    output_buffer2km = "in_memory/buffer2K"
    arcpy.Buffer_analysis(output_faixa_servidao, output_buffer2km, loc_buffer)

    # Selecionar os polígonos que estão a menos de 2 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(output_intersect_cavi, 'cavi_lyr')
    arcpy.SelectLayerByLocation_management('cavi_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{loc_buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('cavi_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'cavi' em memória com um nome diferente
    output_cavi_mem = "in_memory/cavi_temp"
    arcpy.CopyFeatures_management('cavi_lyr', output_cavi_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined_cavi = "in_memory/cavi_combined"
    arcpy.Merge_management([output_intersect_cavi, output_cavi_mem], output_combined_cavi)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined_cavi, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined_cavi, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_cavi, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined_cavi, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_cavi, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined_cavi, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined_cavi, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined_cavi, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined_cavi, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_cavidades = os.path.join(gdb_saida, 'Cavidades')
    arcpy.CopyFeatures_management(output_combined_cavi, output_cavidades)

    #Exportar para Excel

    campos_selecionados = ['Registro_N', 'Caverna', 'Municipio', 'UF', 'Area_ha', 'NEAR_DIST',"Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_cavidades)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_cavidades, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Cavidades Naturais em um raio de 2 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_cavidades)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_cavidades, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "Registro_N": "Registro",
            "Caverna": "Denominação",
            "Municipio": "Município",
            "UF": "UF",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Registro', 'Denominação', 'Município', 'UF', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Cavidades.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def sitios_arqueologicos():
# SÍTIOS ARQUEOLOGICOS


    #Distancia Buffer Cavidades
    sitios_buffer = 250

    # realizar o buffer e salvar em memória
    input_buffer250 = "in_memory/sitios250m"
    arcpy.Buffer_analysis(input_sitios, input_buffer250, sitios_buffer)

    # Realizar o intersect entre os shapefiles
    output_intersect_sitios = "in_memory/sitios" #aqui vem um registro que intercepta
    arcpy.Intersect_analysis([input_buffer250, output_faixa_servidao], output_intersect_sitios, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_sitios)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_sitios, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_sitios, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_sitios, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    sit_buffer = 2000

    # realizar o buffer e salvar em memória
    output_buffer2km = "in_memory/buffer2Ksitios"
    arcpy.Buffer_analysis(output_faixa_servidao, output_buffer2km, sit_buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_buffer250, 'sitiosarqueologicos_lyr')
    arcpy.SelectLayerByLocation_management('sitiosarqueologicos_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{sit_buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('sitiosarqueologicos_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'sitios' em memória com um nome diferente
    output_sitios_mem = "in_memory/sitiosarqueologicos_temp"
    arcpy.CopyFeatures_management('sitiosarqueologicos_lyr', output_sitios_mem)

    # Converter feições de linha para polígono
    #output_sitios_mem_poly = "in_memory/sitios_mem_poly"
    #arcpy.FeatureToPolygon_management(output_sitios_mem, output_sitios_mem_poly)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined_sitios = "in_memory/sitios_combined"
    arcpy.Merge_management([output_intersect_sitios, output_sitios_mem], output_combined_sitios)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined_sitios, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined_sitios, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_sitios, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined_sitios, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_sitios, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined_sitios, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined_sitios, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined_sitios, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined_sitios, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_sitiosarc = os.path.join(gdb_saida, 'Sitios_Arqueologicos')
    arcpy.CopyFeatures_management(output_combined_sitios, output_sitiosarc)


    #Exportar para Excel


    campos_selecionados = ['co_iphan', 'identifica', 'Area_ha', 'NEAR_DIST',"Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_sitiosarc)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_sitiosarc, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Sítios Arqueológicos em um raio de 2 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_sitiosarc)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_sitiosarc, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "co_iphan": "Código",
            "identifica": "Idenditicação",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Código', 'Idenditicação', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Sitios_Arqueologicos.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def ocorrencias_fossiliferas():
    # OCORRENCIAS FOSSILIFERAS


    #Distancia Buffer Ocorrencias
    ocorrencias_buffer = 250

    # realizar o buffer e salvar em memória
    input_buffer250_ = "in_memory/ocorrencias250m"
    arcpy.Buffer_analysis(input_ocorrencias, input_buffer250_, ocorrencias_buffer)

    # Realizar o intersect entre os shapefiles
    output_intersect_ocorrencias = "in_memory/ocorrencias" 
    arcpy.Intersect_analysis([input_buffer250_, output_faixa_servidao], output_intersect_ocorrencias, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_ocorrencias)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_ocorrencias, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_ocorrencias, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_ocorrencias, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    oco_buffer = 2000

    # realizar o buffer e salvar em memória
    output_buffer2kms = "in_memory/buffer2Koco"
    arcpy.Buffer_analysis(output_faixa_servidao, output_buffer2kms, oco_buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_buffer250_, 'ocorrencias_lyr')
    arcpy.SelectLayerByLocation_management('ocorrencias_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{oco_buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('ocorrencias_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'sitios' em memória com um nome diferente
    output_oco_mem = "in_memory/oco_temp"
    arcpy.CopyFeatures_management('ocorrencias_lyr', output_oco_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined_oco = "in_memory/oco_combined"
    arcpy.Merge_management([output_intersect_ocorrencias, output_oco_mem], output_combined_oco)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined_oco, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined_oco, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_oco, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined_oco, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_oco, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined_oco, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined_oco, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined_oco, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined_oco, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_ocorrencias = os.path.join(gdb_saida, 'Ocorrencias_Fossiliferas')
    arcpy.CopyFeatures_management(output_combined_oco, output_ocorrencias)


    #Exportar para Excel


    campos_selecionados = ['ID', 'DATA_ATUAL', 'FONTE', 'TAXON', 'Area_ha', 'NEAR_DIST',"Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_ocorrencias)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_ocorrencias, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Ocorrências Fossilíferas em um raio de 2 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_ocorrencias)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_ocorrencias, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "ID": "Código",
            "DATA_ATUAL": "Data",
            "FONTE": "Descrição",
            "TAXON": "Taxon",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Código', 'Data', 'Descrição', 'Taxon', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Ocorrencias_Fossiliferas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def indigenas():
    # TERRITÓRIOS INDÍGENAS


    #Distancia Buffer Ocorrencias
    buffer_TIs = 5000

    # realizar o buffer e salvar em memória
    input_buffer_5000TIs = "in_memory/bufferTIs"
    arcpy.Buffer_analysis(input_TIs, input_buffer_5000TIs, buffer_TIs)

    # Realizar o intersect entre os shapefiles
    output_intersect_TIs = "in_memory/TIs" 
    arcpy.Intersect_analysis([input_buffer_5000TIs, output_faixa_servidao], output_intersect_TIs, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_TIs)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_TIs, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_TIs, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_TIs, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    TIs_Buffer = 10000

    # realizar o buffer e salvar em memória
    output_TIs_Buffer = "in_memory/outputtisbuffer"
    arcpy.Buffer_analysis(output_faixa_servidao, output_TIs_Buffer, TIs_Buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_buffer_5000TIs, 'TIs_lyr')
    arcpy.SelectLayerByLocation_management('TIs_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{TIs_Buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('TIs_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'sitios' em memória com um nome diferente
    output_TIs_mem = "in_memory/TIs_temp"
    arcpy.CopyFeatures_management('TIs_lyr', output_TIs_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined_TIs = "in_memory/TIs_combined"
    arcpy.Merge_management([output_intersect_TIs, output_TIs_mem], output_combined_TIs)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined_TIs, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined_TIs, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_TIs, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined_TIs, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_TIs, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined_TIs, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined_TIs, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined_TIs, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined_TIs, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_TIs = os.path.join(gdb_saida, 'TIs')
    arcpy.CopyFeatures_management(output_combined_TIs, output_TIs)


    #Exportar para Excel


    campos_selecionados = ['terrai_cod', 'terrai_nom', 'etnia_nome', 'municipio_', 'uf_sigla', 'fase_ti', 'Area_ha', 'NEAR_DIST',"Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_TIs)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_TIs, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Territórios Indígenas em um raio de 10 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_TIs)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_TIs, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "terrai_cod": "Código",
            "terrai_nom": "Nome",
            "etnia_nome": "Etnia",
            "municipio_": "Município",
            "uf_sigla": "UF",
            "fase_ti": "Fase",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Código', 'Nome', 'Etnia', 'Município', 'UF', 'Fase', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Territorios_Indigenas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def ucs():

    # UNIDADES DE CONSERVAÇÃO



    # Realizar o intersect entre os shapefiles
    output_intersect_UCs = "in_memory/UCs" 
    arcpy.Intersect_analysis([input_UCs, output_faixa_servidao], output_intersect_UCs, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_UCs)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_UCs, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_UCs, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_UCs, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    UCs_buffer = 10000

    # realizar o buffer e salvar em memória
    output_UCs_Buffer = "in_memory/outputUCsbuffer"
    arcpy.Buffer_analysis(output_faixa_servidao, output_UCs_Buffer, UCs_buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_UCs, 'UCs_lyr')
    arcpy.SelectLayerByLocation_management('UCs_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{UCs_buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('UCs_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'sitios' em memória com um nome diferente
    output_UCs_mem = "in_memory/mem_temp"
    arcpy.CopyFeatures_management('UCs_lyr', output_UCs_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined_UCs = "in_memory/UCs_combined"
    arcpy.Merge_management([output_intersect_UCs, output_UCs_mem], output_combined_UCs)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined_UCs, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined_UCs, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_UCs, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined_UCs, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_UCs, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined_UCs, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined_UCs, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined_UCs, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined_UCs, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_UCS = os.path.join(gdb_saida, 'UCs')
    arcpy.CopyFeatures_management(output_combined_UCs, output_UCS)


    #Exportar para Excel


    campos_selecionados = ['CODIGO_U11', 'NOME_UC1', 'CATEGORI3', 'GRUPO4', 'ESFERA5', 'ATO_LEGA9', 'Area_ha', 'NEAR_DIST',"Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_UCS)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_UCS, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Unidades de Conservação em um raio de 10 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_UCS)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_UCS, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "CODIGO_U11": "Código",
            "NOME_UC1": "Nome",
            "CATEGORI3": "Categoria",
            "GRUPO4": "Grupo",
            "ESFERA5": "Esfera",
            "ATO_LEGA9": "Ato Legal",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Código', 'Nome', 'Categoria', 'Grupo', 'Esfera', 'Ato Legal', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Unidades_de_Conservacao.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def zona_amortecimento():
    # ZONAS DE AMORTECIMENTO



    # Realizar o intersect entre os shapefiles
    output_intersect_ZAs = "in_memory/ZAs" 
    arcpy.Intersect_analysis([input_ZAs, output_faixa_servidao], output_intersect_ZAs, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_ZAs)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_ZAs, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_ZAs, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_ZAs, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    ZAs_Buffer = 10000

    # realizar o buffer e salvar em memória
    output_ZAs_Buffer = "in_memory/outputZAsbuffer"
    arcpy.Buffer_analysis(output_faixa_servidao, output_ZAs_Buffer, ZAs_Buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_ZAs, 'ZAs_lyr')
    arcpy.SelectLayerByLocation_management('ZAs_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{ZAs_Buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('ZAs_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'sitios' em memória com um nome diferente
    output_ZAs_mem = "in_memory/memZas_temp"
    arcpy.CopyFeatures_management('ZAs_lyr', output_ZAs_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined_ZAs = "in_memory/ZAs_combined"
    arcpy.Merge_management([output_intersect_ZAs, output_ZAs_mem], output_combined_ZAs)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined_ZAs, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined_ZAs, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_ZAs, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined_ZAs, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_ZAs, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined_ZAs, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined_ZAs, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined_ZAs, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined_ZAs, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_ZAs = os.path.join(gdb_saida, 'ZAs')
    arcpy.CopyFeatures_management(output_combined_ZAs, output_ZAs)


    #Exportar para Excel


    campos_selecionados = ['zam_uco_cd', 'zam_nm_mic', 'Area_ha', 'NEAR_DIST',"Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_ZAs)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_ZAs, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Zonas de Amortecimento de Unidades de Conservação em um raio de 10 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_ZAs)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_ZAs, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "zam_uco_cd": "Código",
            "zam_nm_mic": "Nome",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Código', 'Nome', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Zonas_de_Amortecimento.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def apcb():
    # APCBs


    # Realizar o intersect entre os shapefiles
    output_intersect_APCBs = "in_memory/APCBs" 
    arcpy.Intersect_analysis([input_APCBs_MA, output_faixa_servidao], output_intersect_APCBs, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_APCBs)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_APCBs, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_APCBs, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_APCBs, area_intersecao_field, expression, 'PYTHON')

    # Salvar a feature class combinada no geodatabase de saída
    output_APCBs = os.path.join(gdb_saida, 'APCBs')
    arcpy.CopyFeatures_management(output_intersect_APCBs, output_APCBs)

    #Exportar para Excel

    campos_selecionados = ['COD_area', 'AcaoPriori', 'ImportBio_', 'Prioridade', 'Area_ha', "Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_APCBs)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_APCBs, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não foram encontradas APCBs que interceptam a Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_APCBs)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_APCBs, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "COD_area": "Código",
            "AcaoPriori": "Ação Prioritária",
            "ImportBio_": "Importância",
            "Prioridade": "Prioridade",
            "Area_ha": "Área (ha)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Código', 'Ação Prioritária', 'Importância', 'Prioridade', 'Área (ha)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'APCBs.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def assentamento():
    # ASSENTAMENTOS RURAIS


    # Realizar o intersect entre os shapefiles
    output_intersect_assentamentos = "in_memory/assentamentos" 
    arcpy.Intersect_analysis([input_assentamentos, output_faixa_servidao], output_intersect_assentamentos, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_assentamentos)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_assentamentos, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_assentamentos, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_assentamentos, area_intersecao_field, expression, 'PYTHON')

    #distancia do buffer em metros
    assentamento_buffer = 10000

    # realizar o buffer e salvar em memória
    output_assentamentos_buffer = "in_memory/outputassentbuffer"
    arcpy.Buffer_analysis(output_faixa_servidao, output_assentamentos_buffer, assentamento_buffer)

    # Selecionar os polígonos que estão a menos de 10 km da faixa de servidão
    arcpy.MakeFeatureLayer_management(input_assentamentos, 'assent_lyr')
    arcpy.SelectLayerByLocation_management('assent_lyr', 'WITHIN_A_DISTANCE', output_faixa_servidao, f"{assentamento_buffer} Meters", 'NEW_SELECTION')

    # Selecionar os polígonos que intersectam a faixa de servidão
    arcpy.SelectLayerByLocation_management('assent_lyr', 'INTERSECT', output_faixa_servidao, None, 'REMOVE_FROM_SELECTION')

    # Salvar a camada 'sitios' em memória com um nome diferente
    output_assentamentos_mem = "in_memory/memassent_temp"
    arcpy.CopyFeatures_management('assent_lyr', output_assentamentos_mem)

    # Combinar o resultado do intersect com os demais polígonos
    output_combined_assentamentos = "in_memory/outputassent_combined"
    arcpy.Merge_management([output_intersect_assentamentos, output_assentamentos_mem], output_combined_assentamentos)

    # Calcular a menor distância dos pontos selecionados em relação à diretriz gerada
    arcpy.Near_analysis(output_combined_assentamentos, output_faixa_servidao)

    # Calcular os valores do novo campo "Menor_Distancia_km" em quilômetros com duas casas decimais
    expression = "round(!NEAR_DIST! / 1000.0, 2)"
    arcpy.CalculateField_management(output_combined_assentamentos, "NEAR_DIST", expression, "PYTHON")

    # Atualizar o campo "Sequencial" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_assentamentos, ["Sequencial", "NEAR_FID"]) as cursor:
        for row in cursor:
            sequencial = row[0]
            near_fid = row[1]
            if sequencial is None:
                row[0] = near_fid - 1
                cursor.updateRow(row)

    # Relacionar o campo "Sequencial" com o campo "Sequencial" da faixa de servidão
    arcpy.JoinField_management(output_combined_assentamentos, "Sequencial", output_faixa_servidao, "Sequencial", ["Vertices"])

    # Preencher o campo "Vertices" se estiver nulo
    with arcpy.da.UpdateCursor(output_combined_assentamentos, ["Vertices"]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices is None:
                # Obter o valor do campo "Vertices" da faixa de servidão
                with arcpy.da.SearchCursor(output_faixa_servidao, "Vertices") as search_cursor:
                    for search_row in search_cursor:
                        vertices = search_row[0]
                        break  # Parar após a primeira iteração, pois só precisamos da primeira linha
                row[0] = vertices
                cursor.updateRow(row)

    # Renomear a coluna "Vertices" para "Vert_Result"
    arcpy.AlterField_management(output_combined_assentamentos, "Vertices_1", "Vert_Result", "Vert_Result")

    # Excluir a coluna "Vertices" do arquivo finalj
    arcpy.DeleteField_management(output_combined_assentamentos, "Vertices")

    # Renomear a coluna "Vert_Result" para "Vertices"
    arcpy.AlterField_management(output_combined_assentamentos, "Vert_Result", "Vertices", "Vertices")

    # Nome do campo 'Area_ha'
    campo_area_ha = 'Area_ha'

    # Atualizar registros com valor nulo para 0
    with arcpy.da.UpdateCursor(output_combined_assentamentos, [campo_area_ha]) as cursor:
        for row in cursor:
            if row[0] is None:
                row[0] = 0
                cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_assentamentos = os.path.join(gdb_saida, 'Assentamentos')
    arcpy.CopyFeatures_management(output_combined_assentamentos, output_assentamentos)


    #Exportar para Excel


    campos_selecionados = ['cd_sipra', 'nome_proje', 'municipio', 'uf', 'Area_ha', 'NEAR_DIST',"Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_assentamentos)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_assentamentos, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Assentamentos Rurais em um raio de 10 km da Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_assentamentos)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_assentamentos, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "cd_sipra": "Código",
            "nome_proje": "Nome do Projeto",
            "municipio": "Município",
            "uf": "UF",
            "Area_ha": "Área (ha)",
            "NEAR_DIST": "Menor Distância (km)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Código', 'Nome do Projeto', 'Município', 'UF', 'Área (ha)', 'Menor Distância (km)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Assentamentos_Rurais.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def processos_minerarios():
    # PROCESSOS MINERÁRIOS


    # Realizar o intersect entre os shapefiles
    output_intersect_faixa_muni = "in_memory/intersectfaixamuni" 
    arcpy.Intersect_analysis([input_municipios, output_faixa_servidao], output_intersect_faixa_muni, "ALL", "", "INPUT")

    # Definir os parâmetros do Dissolve
    input_features = output_intersect_faixa_muni
    output_faixa_Mun_dissolve = "in_memory/dissolve"
    dissolve_field = "Sequencial; Vertices; NM_MUN; SIGLA_UF"
    statistics_fields = []  # Lista vazia para dissolver todos os atributos

    # Realizar o Dissolve
    arcpy.Dissolve_management(input_features, output_faixa_Mun_dissolve, dissolve_field, statistics_fields)

    # Realizar o intersect entre os shapefiles
    output_intersect_processos = "in_memory/processosminerarios_" 
    arcpy.Intersect_analysis([input_processos_minerarios, output_faixa_Mun_dissolve], output_intersect_processos, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_processos)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_processos, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_processos, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_processos, area_intersecao_field, expression, 'PYTHON')

    # Realizar o intersect entre os shapefiles
    output_intersect_processos2 = "in_memory/processosminerarios2" 
    arcpy.Intersect_analysis([input_processos_minerarios, output_faixa_Mun_dissolve], output_intersect_processos2, "ALL", "", "INPUT")

    # Verificar se o campo 'Area_ha' já existe
    field_names = [field.name for field in arcpy.ListFields(output_intersect_processos2)]
    area_intersecao_field = 'Area_ha'

    if area_intersecao_field in field_names:
        # Se o campo já existir, recalcular a área apenas para a interseção
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_processos2, area_intersecao_field, expression, 'PYTHON')
    else:
        # Se o campo não existir, criar o campo 'Area_ha' e calcular a área apenas para a interseção
        arcpy.AddField_management(output_intersect_processos2, area_intersecao_field, 'DOUBLE')
        expression = '!SHAPE.area@HECTARES!'
        arcpy.CalculateField_management(output_intersect_processos2, area_intersecao_field, expression, 'PYTHON')

    # Salvar a feature class combinada no geodatabase de saída
    output_processos_minerarios3 = os.path.join(gdb_saida, 'Processos_Minerarios')
    arcpy.CopyFeatures_management(output_intersect_processos2, output_processos_minerarios3)

    #Exportar para Excel

    campos_selecionados = ['PROCESSO', 'FASE', 'NOME', 'SUBS', 'USO', 'NM_MUN', 'UF','AREA_HA', "Vertices"]

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_processos_minerarios3)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_processos_minerarios3, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não foram encontradas Processos Minerários que interceptam a Faixa de Servidão."]})
    else:
        
        # Obter os nomes originais dos campos
        desc = arcpy.Describe(output_processos_minerarios3)
        campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

        # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
        table = arcpy.da.TableToNumPyArray(output_processos_minerarios3, campos_originais, skip_nulls=False)
        df = pd.DataFrame(table)

        # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
        nome_cabecalhos = {
            "PROCESSO": "Nº Processo",
            "NOME": "Nome",
            "FASE": "Fase",
            "NM_MUN": "Município",
            "UF": "UF",
            "SUBS": "Substância",
            "USO": "Uso",
            "AREA_HA": "Área (ha)",
            "Vertices": "Vértices"
        }

        # Renomear os cabeçalhos no dataframe
        df.rename(columns=nome_cabecalhos, inplace=True)

        # Definir a ordem desejada das colunas
        ordem_colunas = ['Nº Processo', 'Nome', 'Fase', 'Município', 'UF', 'Substância', 'Uso', 'Área (ha)', 'Vértices']

        # Reordenar as colunas do DataFrame
        df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Processos_Minerarios.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def vegetacao():
    # VEGETAÇÃO


    # Realizar o intersect entre os shapefiles
    output_intersect_veg = "in_memory/vegetacao" 
    arcpy.Intersect_analysis([input_vegetacao, output_diretriz_gerada], output_intersect_veg, "ALL", "", "INPUT")

    # Definir os parâmetros do Dissolve
    input_features = output_intersect_veg
    output_Diretriz_dissolve = "in_memory/dissolve2"
    dissolve_field = "Fito; Vertices"
    statistics_fields = []  # Lista vazia para dissolver todos os atributos

    # Realizar o Dissolve
    arcpy.Dissolve_management(input_features, output_Diretriz_dissolve, dissolve_field, statistics_fields)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_km'
    arcpy.AddField_management(output_Diretriz_dissolve, exten_field, 'DOUBLE')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.length@KILOMETERS!'
    arcpy.CalculateField_management(output_Diretriz_dissolve, exten_field, expression, 'PYTHON')

    # Salvar a feature class combinada no geodatabase de saída
    output_vegetacao = os.path.join(gdb_saida, 'Vegetacao')
    arcpy.CopyFeatures_management(output_Diretriz_dissolve, output_vegetacao)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Fito', 'Exten_km', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_Diretriz_dissolve)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Fito":"Fitofisionomia",
        "Exten_km": "Extensão da Travessia (km)",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_Diretriz_dissolve, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há Fitofisionomias que interceptam a Diretriz."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Fitofisionomia', 'Extensão da Travessia (km)', 'Vértices']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Vegetacao.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)

    arcpy.Delete_management(output_intersect_veg)
    arcpy.Delete_management(output_Diretriz_dissolve)
def geomorfologia():
    # GEOMORFOLOGIA 


    # Realizar o intersect entre os shapefiles
    output_intersect_relevo_diretriz = "in_memory/intersect_relevo_diretriz" 
    arcpy.Intersect_analysis([input_relevo, arcpy.Intersect_analysis([input_vegetacao, output_diretriz_gerada], output_intersect_veg, "ALL", "", "INPUT")
    ], output_intersect_relevo_diretriz, "ALL", "", "INPUT")

    # Definir os parâmetros do Dissolve
    input_features = output_intersect_relevo_diretriz
    output_Diretriz_dissolve = "in_memory/intersect_relevo_diretriz_Dissolve"
    dissolve_field = "Classes_EMBRAPA_; Classes"
    statistics_fields = []  # Lista vazia para dissolver todos os atributos

    # Realizar o Dissolve
    arcpy.Dissolve_management(input_features, output_Diretriz_dissolve, dissolve_field, statistics_fields)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_km'
    arcpy.AddField_management(output_Diretriz_dissolve, exten_field, 'DOUBLE')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.length@KILOMETERS!'
    arcpy.CalculateField_management(output_Diretriz_dissolve, exten_field, expression, 'PYTHON')

    # Calcular o campo "Extensao (%)"
    total_extensao = 0

    # Calcular a soma total da extensão
    with arcpy.da.SearchCursor(output_Diretriz_dissolve, exten_field) as cursor:
        for row in cursor:
            total_extensao += row[0]

    # Criar novo campo "Extensao (%)"
    arcpy.AddField_management(output_Diretriz_dissolve, 'Percent', 'DOUBLE')

    # Calcular o percentual para cada classe
    with arcpy.da.UpdateCursor(output_Diretriz_dissolve, [exten_field, 'Percent']) as cursor:
        for row in cursor:
            exten_km = row[0]
            percentual = (exten_km / total_extensao) * 100
            row[1] = percentual
            cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_relevo = os.path.join(gdb_saida, 'Geomorfologia')
    arcpy.CopyFeatures_management(output_Diretriz_dissolve, output_relevo)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Classes', 'Classes_EMBRAPA_' ,'Exten_km', 'Percent']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_Diretriz_dissolve)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Classes": "Classes de Relevo",
        "Classes_EMBRAPA_": "Faixa Declividade",
        "Percent": "Extensão (%)",
        "Exten_km": "Extensão (km)"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_Diretriz_dissolve, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Classes de Relevo', 'Faixa Declividade', 'Extensão (%)', 'Extensão (km)']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Geomorfologia.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)

    arcpy.Delete_management(output_intersect_relevo_diretriz)
    arcpy.Delete_management(output_Diretriz_dissolve)
def usosolo():
    # USO E OCUPAÇÃO DO SOLO


    # Realizar o intersect entre os shapefiles
    output_intersect_uso = "in_memory/intersect_uso_solo" 
    arcpy.Intersect_analysis([input_uso, output_diretriz_gerada], output_intersect_uso, "ALL", "", "INPUT")

    # Definir os parâmetros do Dissolve
    input_features = output_intersect_uso
    output_Diretriz_dissolve = "in_memory/intersect_uso_diretriz_Dissolve"
    dissolve_field = "Classes"
    statistics_fields = []  # Lista vazia para dissolver todos os atributos

    # Realizar o Dissolve
    arcpy.Dissolve_management(input_features, output_Diretriz_dissolve, dissolve_field, statistics_fields)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_km'
    arcpy.AddField_management(output_Diretriz_dissolve, exten_field, 'DOUBLE')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.length@KILOMETERS!'
    arcpy.CalculateField_management(output_Diretriz_dissolve, exten_field, expression, 'PYTHON')

    # Calcular o campo "Extensao (%)"
    total_extensao = 0

    # Calcular a soma total da extensão
    with arcpy.da.SearchCursor(output_Diretriz_dissolve, exten_field) as cursor:
        for row in cursor:
            total_extensao += row[0]

    # Criar novo campo "Extensao (%)"
    arcpy.AddField_management(output_Diretriz_dissolve, 'Percent', 'DOUBLE')

    # Calcular o percentual para cada classe
    with arcpy.da.UpdateCursor(output_Diretriz_dissolve, [exten_field, 'Percent']) as cursor:
        for row in cursor:
            exten_km = row[0]
            percentual = (exten_km / total_extensao) * 100
            row[1] = percentual
            cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_relevo = os.path.join(gdb_saida, 'Uso_do_Solo')
    arcpy.CopyFeatures_management(output_Diretriz_dissolve, output_relevo)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Classes', 'Exten_km', 'Percent']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_Diretriz_dissolve)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Classes": "Classes de Uso e Ocupação do Solo",
        "Percent": "Extensão (%)",
        "Exten_km": "Extensão (km)"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_Diretriz_dissolve, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Classes de Uso e Ocupação do Solo', 'Extensão (%)', 'Extensão (km)']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Uso_e_Ocupacao_do_Solo.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)

    arcpy.Delete_management(output_intersect_uso)
    arcpy.Delete_management(output_Diretriz_dissolve)
def erodibilidade():
    # ERODIBILIDADE


    # Realizar o intersect entre os shapefiles
    output_intersect_erosao = "in_memory/intersect_erodibilidade" 
    arcpy.Intersect_analysis([input_Erodibilidade, output_diretriz_gerada], output_intersect_erosao, "ALL", "", "INPUT")

    # Definir os parâmetros do Dissolve
    input_features = output_intersect_erosao
    output_Diretriz_dissolve = "in_memory/intersect_uso_diretriz_Dissolve"
    dissolve_field = "Classes"
    statistics_fields = []  # Lista vazia para dissolver todos os atributos

    # Realizar o Dissolve
    arcpy.Dissolve_management(input_features, output_Diretriz_dissolve, dissolve_field, statistics_fields)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_km'
    arcpy.AddField_management(output_Diretriz_dissolve, exten_field, 'DOUBLE')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.length@KILOMETERS!'
    arcpy.CalculateField_management(output_Diretriz_dissolve, exten_field, expression, 'PYTHON')

    # Calcular o campo "Extensao (%)"
    total_extensao = 0

    # Calcular a soma total da extensão
    with arcpy.da.SearchCursor(output_Diretriz_dissolve, exten_field) as cursor:
        for row in cursor:
            total_extensao += row[0]

    # Criar novo campo "Extensao (%)"
    arcpy.AddField_management(output_Diretriz_dissolve, 'Percent', 'DOUBLE')

    # Calcular o percentual para cada classe
    with arcpy.da.UpdateCursor(output_Diretriz_dissolve, [exten_field, 'Percent']) as cursor:
        for row in cursor:
            exten_km = row[0]
            percentual = (exten_km / total_extensao) * 100
            row[1] = percentual
            cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_relevo = os.path.join(gdb_saida, 'Erodibilidade')
    arcpy.CopyFeatures_management(output_Diretriz_dissolve, output_relevo)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Classes', 'Exten_km', 'Percent']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_Diretriz_dissolve)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Classes": "Classes",
        "Percent": "Extensão (%)",
        "Exten_km": "Extensão (km)"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_Diretriz_dissolve, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Classes', 'Extensão (%)', 'Extensão (km)']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Erodibilidade.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def edificacoes():
    # EDIFICAÇÕES


    # Realizar o intersect entre os shapefiles
    output_intersect_edificacoes = "in_memory/intersect_edificacoes" 
    arcpy.Intersect_analysis([input_edificacoes, output_faixa_servidao], output_intersect_edificacoes, "ALL", "", "INPUT")

    # Criar novo campo "Cont" como Inteiro
    cont_field = "Cont"
    arcpy.AddField_management(output_intersect_edificacoes, cont_field, "SHORT")

    # Criar dicionário para rastrear a contagem de valores de "Vertices"
    vertices_count = {}

    # Calcular a contagem de valores de "Vertices"
    with arcpy.da.SearchCursor(output_intersect_edificacoes, "Vertices") as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices in vertices_count:
                vertices_count[vertices] += 1
            else:
                vertices_count[vertices] = 1

    # Atualizar o campo "Cont" com os valores correspondentes
    with arcpy.da.UpdateCursor(output_intersect_edificacoes, ["Vertices", cont_field]) as cursor:
        for row in cursor:
            vertices = row[0]
            if vertices in vertices_count:
                row[1] = vertices_count[vertices]
                cursor.updateRow(row)

    # Definir os parâmetros do Dissolve
    input_features = output_intersect_edificacoes
    output_dissolve_layer = "in_memory/intersect_edificacoes_Dissolve"
    dissolve_field = "Vertices", "Cont"
    statistics_fields = []  # Lista vazia para dissolver todos os atributos

    # Realizar o Dissolve
    arcpy.Dissolve_management(input_features, output_dissolve_layer, dissolve_field, statistics_fields)

    # Salvar a feature class combinada no geodatabase de saída
    output_relevo = os.path.join(gdb_saida, 'Edificacoes')
    arcpy.CopyFeatures_management(output_dissolve_layer, output_relevo)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Vertices', 'Cont']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_dissolve_layer)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Vertices": "Vértices",
        "Cont": "Número de Edificações",
        
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_dissolve_layer, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Vértices', 'Número de Edificações']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Edificacoes.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)

    arcpy.Delete_management(output_intersect_edificacoes)
    arcpy.Delete_management(output_dissolve_layer)
def coordenadas():

    # COORDENADAS

    # Criar novo campo "Vertices" do tipo texto
    #campo_vertices = 'Vertices'
    #AddField(input_vertices, campo_vertices, 'TEXT', field_length=100)

    # Atualizar o campo "Vertices" com base no campo "Ordem"
    #with arcpy.da.UpdateCursor(input_vertices, ['Ordem', campo_vertices]) as cursor:
        #for row in cursor:
            #ordem = row[0]
            #if ordem == 0:
                #row[1] = 'SE Abdon Batista II'
            #elif ordem == 40:
                #row[1] = 'SE Curitiba Oeste'
            #else:
                #row[1] = f'V{ordem:02d}'
            #cursor.updateRow(row)

    # Nome do campo "Parcial"
    campo_parcial = 'Parcial'

    # Adicionar o campo "Parcial" à tabela de atributos
    arcpy.AddField_management(input_vertices, campo_parcial, 'DOUBLE')

    # Criar um cursor para ler e atualizar os vértices
    with arcpy.da.UpdateCursor(input_vertices, ['SHAPE@', campo_parcial]) as cursor:
        previous_vertex = None
        for row in cursor:
            vertex = row[0].getPart()
            if previous_vertex is not None:
                # Criar geometrias de ponto a partir dos vértices
                previous_point = arcpy.PointGeometry(previous_vertex)
                current_point = arcpy.PointGeometry(vertex)
                # Calcular a distância entre os vértices consecutivos
                distance_km = previous_point.distanceTo(current_point) / 1000  # Convertendo para quilômetros
                row[1] = distance_km
                cursor.updateRow(row)
            previous_vertex = vertex

    # Criar um cursor para ler e atualizar os valores
    with arcpy.da.UpdateCursor(input_vertices, [campo_parcial]) as cursor:
        for row in cursor:
            valor_parcial = row[0]
            if valor_parcial is None:
                row[0] = 0
                cursor.updateRow(row)

    #Nome do campo "Progressiva"
    campo_progressiva = 'Progressiva'

    #Adicionar o campo 'Progressiva' na tabela de atributos
    arcpy.AddField_management(input_vertices, campo_progressiva, 'DOUBLE')

    #Criar um cursor para calcular os valores do campo progressiva
    with arcpy.da.UpdateCursor(input_vertices, [campo_parcial, campo_progressiva]) as cursor:
        previous_parcial = 0
        for row in cursor:
            valor_parcial = row[0]
            progressiva = valor_parcial + previous_parcial
            row[1] = progressiva
            cursor.updateRow(row)
            previous_parcial = progressiva

    # Nomes dos campos para as coordenadas geográficas
    latitude = 'Latitude'
    longitude = 'Longitude'

    # Adicionar os campos de latitude e longitude à tabela de atributos
    arcpy.AddField_management(input_vertices, latitude, 'DOUBLE')
    arcpy.AddField_management(input_vertices, longitude, 'DOUBLE')

    # Criar um cursor para ler e atualizar os valores
    with arcpy.da.UpdateCursor(input_vertices, ['SHAPE@XY', latitude, longitude]) as cursor:
        sr_utm = arcpy.SpatialReference(32722)  # Código UTM para a zona 22S
        sirgas_2000 = arcpy.SpatialReference(4674)  # Código do SIRGAS 2000
        for row in cursor:
            x, y = row[0]
            point_utm = arcpy.PointGeometry(arcpy.Point(x, y), sr_utm)
            point_sirgas_2000 = point_utm.projectAs(sirgas_2000)
            row[1] = point_sirgas_2000.firstPoint.Y
            row[2] = point_sirgas_2000.firstPoint.X
            cursor.updateRow(row)

    # Salvar a feature class combinada no geodatabase de saída
    output_coordenadas = os.path.join(gdb_saida, 'Coordenadas')
    arcpy.CopyFeatures_management(input_vertices, output_coordenadas)

    #Exportar para Excel

    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Vertices', 'Latitude', 'Longitude', 'Parcial', 'Progressiva']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_coordenadas)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Vertices":"Vértices",
        "Latitude": "Latitude",
        "Longitude": "Longitude",
        "Parcial":"Parcial (km)",
        "Progressiva": "Progressiva (km)"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_coordenadas, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Definir a ordem desejada das colunas
    ordem_colunas = ['Vértices', 'Latitude', 'Longitude', 'Parcial (km)', 'Progressiva (km)']

    # Reordenar as colunas do DataFrame
    df = df[ordem_colunas]

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Coordenadas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def linhas_transmissao_paralelas():

    # LINHAS DE TRANSMISSÃO PARALELAS


    # Criar uma camada em memória para o input_Linhas_Transmissao
    arcpy.MakeFeatureLayer_management(input_Linhas_Transmissao, 'input_Linhas_Transmissao_lyr')

    # Selecionar as features de input_Linhas_Transmissao que intersectam com a faixa de servidão
    arcpy.SelectLayerByLocation_management('input_Linhas_Transmissao_lyr', 'INTERSECT', output_faixa_servidao)

    # Dividir as linhas nos vértices
    split_lines = "in_memory/SplitLines"
    arcpy.SplitLine_management('input_Linhas_Transmissao_lyr', split_lines)

    # Criar uma camada em memória para as linhas divididas
    arcpy.MakeFeatureLayer_management(split_lines, 'splitlines_lyr')

    # Realizar seleção por localização para identificar feições inteiramente contidas na faixa de servidão
    arcpy.SelectLayerByLocation_management('splitlines_lyr', "COMPLETELY_WITHIN", output_faixa_servidao)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_m'
    arcpy.AddField_management('splitlines_lyr', exten_field, 'DOUBLE')

    # Calcular a extensão em metros
    expression = '!SHAPE.length@METERS!'
    arcpy.CalculateField_management('splitlines_lyr', exten_field, expression, 'PYTHON')

    arcpy.DeleteField_management('splitlines_lyr', 'Extensao')

    identity_output = "in_memory/LTs_Paralelas_Identity"
    arcpy.analysis.Identity('splitlines_lyr', output_faixa_servidao, identity_output)

    # Excluir a coluna desnecessária
    arcpy.DeleteField_management(identity_output, 'Extensao')

    # Realizar o dissolve 
    output_dissolve = "in_memory/dissolverodovias"
    arcpy.Dissolve_management(identity_output, output_dissolve, ['Nome', 'Vertices', 'Sequencial'])

    # Transformar em camadas (layers)
    arcpy.MakeFeatureLayer_management(output_diretriz_gerada, 'output_diretriz_lyr')
    arcpy.MakeFeatureLayer_management(output_dissolve, 'output_dissolve_lyr')

    # Selecionar feições que não intersectam a diretriz gerada
    arcpy.SelectLayerByLocation_management('output_dissolve_lyr', "INTERSECT", 'output_diretriz_lyr', "", "NEW_SELECTION", "INVERT")

    # Criar um novo campo chamado extensao
    extensao_field = 'Exten_m'
    arcpy.AddField_management('output_dissolve_lyr', extensao_field, 'FLOAT')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.geodesicLength@METERS!'
    arcpy.CalculateField_management('output_dissolve_lyr', extensao_field, expression, 'PYTHON')

    output_lines_final = os.path.join(gdb_saida, 'LTs_Paralelas')
    arcpy.CopyFeatures_management('output_dissolve_lyr', output_lines_final)


    #Exportar para Excel


    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Nome', 'Exten_m', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe('output_dissolve_lyr')
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Nome":"Nome",
        "Exten_m": "Extensão (m)",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray('output_dissolve_lyr', campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Linhas de Transmissão paralelas que interceptam a faixa de servidão."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Linhas_de_Transmissao_Paralelas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def rodovias_paralelas():
    # RODOVIAS PARALELAS


    # Criar uma camada em memória 
    arcpy.MakeFeatureLayer_management(input_rodovias, 'input_rodovias')

    # Selecionar as features de rodovias que intersectam com a faixa de servidão
    arcpy.SelectLayerByLocation_management('input_rodovias', 'INTERSECT', output_faixa_servidao)

    # Dividir as linhas nos vértices
    split_lines = "in_memory/SplitLines"
    arcpy.SplitLine_management('input_rodovias', split_lines)

    # Criar uma camada em memória para as linhas divididas
    arcpy.MakeFeatureLayer_management(split_lines, 'splitlines_lyr')

    # Realizar seleção por localização para identificar feições inteiramente contidas na faixa de servidão
    arcpy.SelectLayerByLocation_management('splitlines_lyr', "COMPLETELY_WITHIN", output_faixa_servidao)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_m'
    arcpy.AddField_management('splitlines_lyr', exten_field, 'DOUBLE')

    # Calcular a extensão em metros
    expression = '!SHAPE.length@METERS!'
    arcpy.CalculateField_management('splitlines_lyr', exten_field, expression, 'PYTHON')

    arcpy.DeleteField_management('splitlines_lyr', 'Extensao')

    identity_output = "in_memory/LTs_Paralelas_Identity_rodovias"
    arcpy.analysis.Identity('splitlines_lyr', output_faixa_servidao, identity_output)

    # Excluir a coluna desnecessária
    arcpy.DeleteField_management(identity_output, 'Extensao')

    # Realizar o dissolve 
    output_dissolve = "in_memory/dissolverodovias"
    arcpy.Dissolve_management(identity_output, output_dissolve, ['vl_br', 'sg_uf', 'ul', 'ds_jurisdi', 'Sequencial', 'Vertices'])

    # Transformar em camadas (layers)
    arcpy.MakeFeatureLayer_management(output_diretriz_gerada, 'output_diretriz_lyr')
    arcpy.MakeFeatureLayer_management(output_dissolve, 'output_dissolve_lyr')

    # Selecionar feições que não intersectam a diretriz gerada
    arcpy.SelectLayerByLocation_management('output_dissolve_lyr', "INTERSECT", 'output_diretriz_lyr', "", "NEW_SELECTION", "INVERT")

    # Criar um novo campo chamado extensao
    extensao_field = 'Exten_m'
    arcpy.AddField_management('output_dissolve_lyr', extensao_field, 'FLOAT')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.geodesicLength@METERS!'
    arcpy.CalculateField_management('output_dissolve_lyr', extensao_field, expression, 'PYTHON')

    # Adicionar novo campo "Sigla_Rodovia" do tipo string
    campo_sigla_rodovia = "Sigla_Rodovia"
    arcpy.AddField_management('output_dissolve_lyr', campo_sigla_rodovia, "TEXT", field_length=50)

    # Atualizar o campo "Sigla_Rodovia" com os valores desejados
    with arcpy.da.UpdateCursor('output_dissolve_lyr', ["ds_jurisdi", "vl_br", "sg_uf", campo_sigla_rodovia]) as cursor:
        for row in cursor:
            if row[0] == "Federal":
                row[3] = "Rodovia BR-" + row[1]
            else:
                row[3] = "Rodovia " + row[2] + "-" + row[1]
            cursor.updateRow(row)

    # Exportar a seleção para o geodatabase de saída
    output_lines_final = os.path.join(gdb_saida, 'Rodovias_Paralelas')
    arcpy.CopyFeatures_management('output_dissolve_lyr', output_lines_final)


    #Exportar para Excel


    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Sigla_Rodovia', 'Exten_m', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe(output_lines_final)
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Nome":"Rodovia",
        "Exten_m": "Extensão (m)",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray(output_lines_final, campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Rodovias paralelas que interceptam a faixa de servidão."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Rodovias_Paralelas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def ferrovias_paralelas():
    # FERROVIAS PARALELAS


    # Criar uma camada em memória para o input_Ferrovias
    arcpy.MakeFeatureLayer_management(input_ferrovias, 'input_ferrovias_lyr')

    # Selecionar as features de input_ferrovias que intersectam com a faixa de servidão
    arcpy.SelectLayerByLocation_management('input_ferrovias_lyr', 'INTERSECT', output_faixa_servidao)

    # Dividir as linhas nos vértices
    split_lines = "in_memory/SplitLines"
    arcpy.SplitLine_management('input_ferrovias_lyr', split_lines)

    # Criar uma camada em memória para as linhas divididas
    arcpy.MakeFeatureLayer_management(split_lines, 'splitlines_lyr')

    # Realizar seleção por localização para identificar feições inteiramente contidas na faixa de servidão
    arcpy.SelectLayerByLocation_management('splitlines_lyr', "COMPLETELY_WITHIN", output_faixa_servidao)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_m'
    arcpy.AddField_management('splitlines_lyr', exten_field, 'DOUBLE')

    # Calcular a extensão em metros
    expression = '!SHAPE.length@METERS!'
    arcpy.CalculateField_management('splitlines_lyr', exten_field, expression, 'PYTHON')

    arcpy.DeleteField_management('splitlines_lyr', 'Extensao')

    identity_output = "in_memory/Ferrovias_Paralelas_Identity"
    arcpy.analysis.Identity('splitlines_lyr', output_faixa_servidao, identity_output)

    # Excluir a coluna desnecessária
    arcpy.DeleteField_management(identity_output, 'Extensao')

    # Realizar o dissolve 
    output_dissolve = "in_memory/dissolve_ferrovias"
    arcpy.Dissolve_management(identity_output, output_dissolve, ['tip_situac', 'sigla', 'municipio', "uf", "Vertices", "Sequencial"])

    # Transformar em camadas (layers)
    arcpy.MakeFeatureLayer_management(output_diretriz_gerada, 'output_diretriz_lyr')
    arcpy.MakeFeatureLayer_management(output_dissolve, 'output_dissolve_lyr')

    # Selecionar feições que não intersectam a diretriz gerada
    arcpy.SelectLayerByLocation_management('output_dissolve_lyr', "INTERSECT", 'output_diretriz_lyr', "", "NEW_SELECTION", "INVERT")

    # Criar um novo campo chamado extensao
    extensao_field = 'Exten_m'
    arcpy.AddField_management('output_dissolve_lyr', extensao_field, 'FLOAT')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.geodesicLength@METERS!'
    arcpy.CalculateField_management('output_dissolve_lyr', extensao_field, expression, 'PYTHON')

    output_lines_final = os.path.join(gdb_saida, 'Ferrovias_Paralelas')
    arcpy.CopyFeatures_management('output_dissolve_lyr', output_lines_final)


    #Exportar para Excel


    # Lista dos campos selecionados para exportação
    campos_selecionados = ['sigla', 'tip_situac', 'municipio', 'uf', 'Exten_m', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe('output_dissolve_lyr')
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "sigla": "Benfeitoria",
        "tip_situac": "Situação",
        "municipio": "Município",
        "uf": "UF",
        "Exten_m": "Extensão (m)",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray('output_dissolve_lyr', campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Ferrovias Parapelas na faixa de servidão."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Ferrovias_Paralelas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def dutovias_paralelas():
    # DUTOVIAS PARALELAS


    # Criar uma camada em memória para Dutovias
    arcpy.MakeFeatureLayer_management(input_Dutovias, 'input_dutovias_lyr')

    # Selecionar as features de input_dutovias que intersectam com a faixa de servidão
    arcpy.SelectLayerByLocation_management('input_dutovias_lyr', 'INTERSECT', output_faixa_servidao)

    # Dividir as linhas nos vértices
    split_lines = "in_memory/SplitLines"
    arcpy.SplitLine_management('input_dutovias_lyr', split_lines)

    # Criar uma camada em memória para as linhas divididas
    arcpy.MakeFeatureLayer_management(split_lines, 'splitlines_lyr')

    # Realizar seleção por localização para identificar feições inteiramente contidas na faixa de servidão
    arcpy.SelectLayerByLocation_management('splitlines_lyr', "COMPLETELY_WITHIN", output_faixa_servidao)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_m'
    arcpy.AddField_management('splitlines_lyr', exten_field, 'DOUBLE')

    # Calcular a extensão em metros
    expression = '!SHAPE.length@METERS!'
    arcpy.CalculateField_management('splitlines_lyr', exten_field, expression, 'PYTHON')

    arcpy.DeleteField_management('splitlines_lyr', 'Extensao')

    identity_output = "in_memory/Dutovias_Paralelas_Identity"
    arcpy.analysis.Identity('splitlines_lyr', output_faixa_servidao, identity_output)

    # Excluir a coluna desnecessária
    arcpy.DeleteField_management(identity_output, 'Extensao')

    # Realizar o dissolve 
    output_dissolve = "in_memory/dissolve_dutovias"
    arcpy.Dissolve_management(identity_output, output_dissolve, ['Name', "Vertices", "Sequencial"])

    # Transformar em camadas (layers)
    arcpy.MakeFeatureLayer_management(output_diretriz_gerada, 'output_diretriz_lyr')
    arcpy.MakeFeatureLayer_management(output_dissolve, 'output_dissolve_lyr')

    # Selecionar feições que não intersectam a diretriz gerada
    arcpy.SelectLayerByLocation_management('output_dissolve_lyr', "INTERSECT", 'output_diretriz_lyr', "", "NEW_SELECTION", "INVERT")

    # Criar um novo campo chamado extensao
    extensao_field = 'Exten_m'
    arcpy.AddField_management('output_dissolve_lyr', extensao_field, 'FLOAT')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.geodesicLength@METERS!'
    arcpy.CalculateField_management('output_dissolve_lyr', extensao_field, expression, 'PYTHON')

    output_lines_final = os.path.join(gdb_saida, 'Dutovias_Paralelas')
    arcpy.CopyFeatures_management('output_dissolve_lyr', output_lines_final)


    #Exportar para Excel


    # Lista dos campos selecionados para exportação
    campos_selecionados = ['Name', 'Exten_m', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe('output_dissolve_lyr')
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "Name": "Benfeitoria",
        "Exten_m": "Extensão (m)",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray('output_dissolve_lyr', campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Dutovias Parapelas na faixa de servidão."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Dutovias_Paralelas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)
def adutoras_paralelas():
    # ADUTORAS PARALELAS


    # Criar uma camada em memória para Adutoras
    arcpy.MakeFeatureLayer_management(input_Adutoras, 'input_adutoras_lyr')

    # Selecionar as features de input_Adutoras que intersectam com a faixa de servidão
    arcpy.SelectLayerByLocation_management('input_adutoras_lyr', 'INTERSECT', output_faixa_servidao)

    # Dividir as linhas nos vértices
    split_lines = "in_memory/SplitLines"
    arcpy.SplitLine_management('input_adutoras_lyr', split_lines)

    # Criar uma camada em memória para as linhas divididas
    arcpy.MakeFeatureLayer_management(split_lines, 'splitlines_lyr')

    # Realizar seleção por localização para identificar feições inteiramente contidas na faixa de servidão
    arcpy.SelectLayerByLocation_management('splitlines_lyr', "COMPLETELY_WITHIN", output_faixa_servidao)

    # Criar novo campo "Exten" como Double
    exten_field = 'Exten_m'
    arcpy.AddField_management('splitlines_lyr', exten_field, 'DOUBLE')

    # Calcular a extensão em metros
    expression = '!SHAPE.length@METERS!'
    arcpy.CalculateField_management('splitlines_lyr', exten_field, expression, 'PYTHON')

    arcpy.DeleteField_management('splitlines_lyr', 'Extensao')

    identity_output = "in_memory/Adutoras_Paralelas_Identity"
    arcpy.analysis.Identity('splitlines_lyr', output_faixa_servidao, identity_output)

    # Excluir a coluna desnecessária
    arcpy.DeleteField_management(identity_output, 'Extensao')

    # Realizar o dissolve 
    output_dissolve = "in_memory/dissolve_dutovias"
    arcpy.Dissolve_management(identity_output, output_dissolve, ['ADUTORA', 'SITUAÇÃO', 'ESTADO', "Vertices", "Sequencial"])

    # Transformar em camadas (layers)
    arcpy.MakeFeatureLayer_management(output_diretriz_gerada, 'output_diretriz_lyr')
    arcpy.MakeFeatureLayer_management(output_dissolve, 'output_dissolve_lyr')

    # Selecionar feições que não intersectam a diretriz gerada
    arcpy.SelectLayerByLocation_management('output_dissolve_lyr', "INTERSECT", 'output_diretriz_lyr', "", "NEW_SELECTION", "INVERT")

    # Criar um novo campo chamado extensao
    extensao_field = 'Exten_m'
    arcpy.AddField_management('output_dissolve_lyr', extensao_field, 'FLOAT')

    # Calcular a extensão em quilômetros
    expression = '!SHAPE.geodesicLength@METERS!'
    arcpy.CalculateField_management('output_dissolve_lyr', extensao_field, expression, 'PYTHON')

    output_lines_final = os.path.join(gdb_saida, 'Adutoras_Paralelas')
    arcpy.CopyFeatures_management('output_dissolve_lyr', output_lines_final)


    #Exportar para Excel


    # Lista dos campos selecionados para exportação
    campos_selecionados = ['ADUTORA', 'SITUAÇÃO', 'ESTADO', 'Exten_m', 'Vertices']

    # Obter os nomes originais dos campos
    desc = arcpy.Describe('output_dissolve_lyr')
    campos_originais = [field.name for field in desc.fields if field.name in campos_selecionados]

    # Mapear os nomes dos campos selecionados para os nomes desejados na exportação
    nome_cabecalhos = {
        "ADUTORA": "Benfeitoria",
        "SITUAÇÃO": "Situação",
        "ESTADO": "UF",
        "Exten_m": "Extensão (m)",
        "Vertices": "Vértices"
    }

    # Criar um dataframe pandas a partir da tabela de atributos com os campos selecionados
    table = arcpy.da.TableToNumPyArray('output_dissolve_lyr', campos_originais, skip_nulls=False)
    df = pd.DataFrame(table)

    # Verificar se o dataframe está vazio
    if df.empty:
        df = pd.DataFrame({"Mensagem": ["Não há registros de Adutoras Parapelas na faixa de servidão."]})

    # Renomear os cabeçalhos no dataframe
    df.rename(columns=nome_cabecalhos, inplace=True)

    # Caminho para o arquivo Excel de saída
    excel_saida = os.path.join(excelfiles, 'Adutoras_Paralelas.xlsx')

    # Exportar o dataframe para o arquivo Excel
    df.to_excel(excel_saida, index=False)



    municipios()
    localidades()
    linhas_transmissao()
    rodovias()
    ferrovias()
    gasoduto_transporte()
    gasoduto_distribuicao()
    dutovias()
    adutoras()
    hidrografia()
    aerodromos()
    quilombolas()
    cavidades()
    sitios_arqueologicos()
    ocorrencias_fossiliferas()
    indigenas()
    ucs()
    zona_amortecimento()
    apcb()
    assentamento()
    processos_minerarios()
    vegetacao()
    geomorfologia()
    usosolo()
    erodibilidade()
    edificacoes()
    coordenadas()
    linhas_transmissao_paralelas()
    rodovias_paralelas()
    ferrovias_paralelas()
    dutovias_paralelas()
    adutoras_paralelas()


ucs()
