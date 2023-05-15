import arcpy

# Inputs
camadas = arcpy.GetParameterAsText(0)
area_estudo = arcpy.GetParameterAsText(1)
pasta_output = arcpy.GetParameterAsText(2)
pasta_excel = arcpy.GetParameterAsText(3)

arcpy.env.workspace = camadas

# Loop
featureclasses = arcpy.ListFeatureClasses()
for fc in featureclasses:
    output = str(fc) + '_clipped'
    clip = arcpy.analysis.Clip(fc, area_estudo, f'{pasta_output}/{output}.shp', "")

    # Verificar o tipo de feição
    desc = arcpy.Describe(clip)
    if desc.shapeType == 'Polygon':
        poligono = arcpy.management.AddGeometryAttributes(clip, 'AREA', "", "SQUARE_METERS")
    elif desc.shapeType == 'Point':
        ponto = arcpy.management.AddGeometryAttributes(clip, 'POINT_X_Y_Z_M', "", "")
    else:
        pass
    
    #agora pego o resultado do clip e transformo em tabela
    nome_xls = fr'{pasta_excel}/quantitativo_{str(fc)}'
    trans_tabela = arcpy.conversion.TableToExcel(clip, nome_xls, "", "")
    if desc.shapeType == 'Polygon' or desc.shapeType == 'Point':
        trans_tabela
    else:
        pass

        

#fim

