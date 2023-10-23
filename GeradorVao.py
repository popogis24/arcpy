import arcpy
import os
import pandas as pd
import numpy as np

arcpy.env.overwriteOutput = True

# Caminho para o geodatabase de entrada
input_diretriz = arcpy.GetParameterAsText(0)
arcpy.env.workspace = fr'C:\Users\anderson.souza\Documents\CHESF\Piloto_quantitativo\workspace'# Defina o caminho correto para sua pasta de trabalho
gdb_saida = ''


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
    output_diretriz_gerada = arcpy.GetParameterAsText(3)
    arcpy.CopyFeatures_management(output_split, output_diretriz_gerada)

    #largura da faixa de servidao em metros
    fs_distancia = arcpy.GetParameterAsText(1)

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
    output_faixa_servidao = arcpy.GetParameterAsText(2)
    arcpy.CopyFeatures_management(no_over, output_faixa_servidao)
    return output_diretriz_gerada, output_faixa_servidao

diretriz()
#deleta as features criadas no workplace
arcpy.Delete_management('SplitVertices')
arcpy.Delete_management('erase_copy')
arcpy.Delete_management('faixa_servidao_buffer')
arcpy.Delete_management('feature_copiada')
arcpy.Delete_management('teste2')