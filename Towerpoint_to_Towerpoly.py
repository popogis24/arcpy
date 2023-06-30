import arcpy
arcpy.env.overwriteOutput = True

autoincremento = '''
rec=0
def autoIncrement():
 global rec
 pStart = 1 #muda para nao iniciar do num 1
 pInterval = 1 #mude este numero para mudar o intervalo de seq
 if (rec == 0): 
  rec = pStart 
 else: 
  rec = rec + pInterval 
 return rec
 '''

# Define os inputs como parâmetros do script
torres = arcpy.GetParameterAsText(0)
lt = arcpy.GetParameterAsText(1)

# Define as variáveis de saída
field_comprimento = arcpy.GetParameterAsText(2)
field_largura = arcpy.GetParameterAsText(3)
output = arcpy.GetParameterAsText(4)
workspace = arcpy.GetParameterAsText(5)

arcpy.env.workspace = workspace

#2. dissolve LT - aqui eu pego a lt e dissolvo
lt_dissolve=arcpy.management.Dissolve(lt, 'lt_dissolve', '', '', '', '', '')

#3. split vlt pelas torres splito a lt a partir das torres
vlt = arcpy.management.SplitLineAtPoint(lt_dissolve, torres, 'vlt', 10)

#4. add campo 'vão'  adiciono o campo 'vao' na lt splitada
arcpy.management.CalculateField(vlt, 'vao', 'autoIncrement()', '', autoincremento, 'FLOAT', '')

#5. feature vertices to points -  transformo a lt splitada em pontos
vlt_end = arcpy.management.FeatureVerticesToPoints(vlt, 'vlt_end', 'END')

#6. spatial join - 
vlt_end_sj = arcpy.analysis.SpatialJoin(vlt_end, torres, 'vlt_end_sj', '', '', '', '', '', '')

#7. add campo 'comp2' e 'larg2' 
arcpy.management.CalculateField(vlt_end_sj, 'larg2', fr'!{field_largura}!/2', '', '', 'FLOAT', '')
arcpy.management.CalculateField(vlt_end_sj, 'comp2', fr'!{field_comprimento}!/2', '', '', 'FLOAT', '')

#7.2. buffer vlt - end 
buffer_torres = arcpy.analysis.Buffer(vlt_end_sj, 'buffer_torres', 'comp2', '', '', '', '', '')

#8. join
vlt_join = arcpy.management.JoinField(
    in_data=vlt,
    in_field="vao",
    join_table=vlt_end_sj,
    join_field="vao",
    fields="larg2;comp2",
    fm_option="NOT_USE_FM",
    field_mapping=None
)

#9. buffer
buffer_linhas = arcpy.analysis.Buffer(vlt_join, 'buffer_linhas', 'comp2', 'RIGHT', '', '', '', '')

#cria um feature class
praca_linha = arcpy.management.CreateFeatureclass(
    out_path=fr"C:\Users\anderson.souza\Documents\teste",
    out_name="praca_linha",
    geometry_type="POLYLINE",
    template=None,
    has_m="DISABLED",
    has_z="DISABLED",
    spatial_reference=torres,
    config_keyword="",
    spatial_grid_1=0,
    spatial_grid_2=0,
    spatial_grid_3=0,
    out_alias=""
)
arcpy.management.AddField(in_table=praca_linha, field_name='vao', field_type='FLOAT')




#################### inicia o loop ####################
cursor = arcpy.SearchCursor(vlt_end_sj)

for row in cursor:
    vao_row = row.getValue('vao')
    sl_vlt_end_sj = arcpy.management.SelectLayerByAttribute(in_layer_or_view=vlt_end_sj, selection_type='NEW_SELECTION', where_clause=f'"vao"={vao_row}')
    sl_buffer_torres = arcpy.management.SelectLayerByAttribute(in_layer_or_view=buffer_torres, selection_type='NEW_SELECTION', where_clause=f'"vao"={vao_row}')
    sl_buffer_linhas = arcpy.management.SelectLayerByAttribute(in_layer_or_view=buffer_linhas, selection_type='NEW_SELECTION', where_clause=f'"vao"={vao_row}')

    #10. erase
    meia_lua = arcpy.analysis.Erase(sl_buffer_torres, sl_buffer_linhas, 'meia_lua', '')

    #FEATURE TO LINE
    meia_lua_linha = arcpy.management.FeatureToLine(meia_lua, 'meia_lua_linha', '', '')

    #split line at vertices
    meia_lua_linha_split = arcpy.management.SplitLine(in_features=meia_lua_linha, out_feature_class='meia_lua_linha_split')

    #12. select by location
    sl_linha_meia_lua = arcpy.management.SelectLayerByLocation(meia_lua_linha_split, '', sl_vlt_end_sj, '', '', '')

    #13 copy features
    copy_linha = arcpy.management.CopyFeatures(
    in_features=sl_linha_meia_lua,
    out_feature_class='copy_linha',
    config_keyword="",
    spatial_grid_1=None,
    spatial_grid_2=None,
    spatial_grid_3=None)
    
    dissolve_copy_linha = arcpy.management.Dissolve(in_features=copy_linha, out_feature_class='dissolve_copy_linha',dissolve_field='vao')
    '''
    #11. feature v. to points
    pto_meia_lua = arcpy.management.FeatureVerticesToPoints(meia_lua, 'pto_meia_lua', '')

    #12. select by location
    sl_pto_meia_lua = arcpy.management.SelectLayerByLocation(pto_meia_lua, '', buffer_linhas, 10, '', '')

    #13. point to line 
    linha = arcpy.management.PointsToLine(Input_Features=sl_pto_meia_lua, Output_Feature_Class='linha', Line_Field='vao')
    '''
    #14. append em fc de linha
    #arcpy.management.Append(inputs=dissolve_copy_linha, target=praca_linha, schema_type='TEST_AND_SKIP', field_mapping=None, subtype='', expression='', match_fields=None, update_geometry='NOT_UPDATE_GEOMETRY')
    


    arcpy.management.Append(
        inputs=dissolve_copy_linha,
        target=praca_linha,
        schema_type="NO_TEST",
        field_mapping='Id "Id" true false false 6 Long 0 6,First,#;vao "vao" true false false 13 Float 0 0,First,#,teste,vao,-1,-1',
        subtype="",
        expression="",
        match_fields=None,
        update_geometry="NOT_UPDATE_GEOMETRY"
    )



#15.1 dissolve pra eliminar os vértices
praca_dissolve = arcpy.management.Dissolve(praca_linha, 'pracas_dissolve', dissolve_field='vao', multi_part='SINGLE_PART', unsplit_lines='UNSPLIT_LINES')

#16. Spatial join 'vao'
sj_pracas_linha = arcpy.analysis.SpatialJoin(praca_dissolve, vlt_end_sj, 'sj_pracas_linha', join_operation='JOIN_ONE_TO_ONE', join_type='KEEP_ALL', match_option='INTERSECT', search_radius=10)

#17. buffer flat end
arcpy.analysis.Buffer(sj_pracas_linha, output, 'larg2', '', 'FLAT', '', '', '')
