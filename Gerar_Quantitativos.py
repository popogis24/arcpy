import arcpy

# Inputs
dados_relatorio = arcpy.GetParameterAsText(0)
area_estudo = arcpy.GetParameterAsText(1)
pasta_output = arcpy.GetParameterAsText(2)
tabela_excel = arcpy.GetParameterAsText(3)
arcpy.env.workspace = dados_relatorio

# Loop
featureclasses = arcpy.ListFeatureClasses()
for fc in featureclasses:
    output = str(fc) + '_clipped'
    clip = arcpy.analysis.Clip(fc, area_estudo, f'{pasta_output}/{output}.shp', "")

    # Ferramentas dentro do loop
    poligono = arcpy.management.AddGeometryAttributes(clip, 'AREA', "", "SQUARE_METERS")
    ponto = arcpy.management.AddGeometryAttributes(clip, 'POINT_X_Y_Z_M', "", "")

    # Verificar o tipo de feição
    desc = arcpy.Describe(clip)
    if desc.shapeType == 'Polygon':
        poligono
    elif desc.shapeType == 'Point':
        ponto
    else:
        pass
    
    #agora pego o resultado do clip e transformo em tabela
    nome_xls = str(fc)
    arcpy.conversion.TableToExcel(clip, nome_xls, "", "")
    

    


