import arcpy

poligonos = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

#polygon to line codigo completo
arcpy.PolygonToLine_management(poligonos, "ftl", "IDENTIFY_NEIGHBORS")

#transforma o ftl em layer
arcpy.MakeFeatureLayer_management("ftl", "featuretoline_lyr")

#selecione todas as linhas que tem dois vizinhos
arcpy.SelectLayerByAttribute_management("featuretoline_lyr", "NEW_SELECTION", '"LEFT_FID" <> -1 AND "RIGHT_FID" <> -1')

#crie uma camada temporaria com as linhas selecionadas
arcpy.MakeFeatureLayer_management("featuretoline_lyr", "featuretoline_lyr2")

#buffer de 10 milimetros nas linhas selecionadas, right, round, all
arcpy.Buffer_analysis("featuretoline_lyr2", "buffer", "2 Centimeters", "RIGHT", "ROUND", "ALL")

#crie uma camada temporaria com os poligonos
arcpy.MakeFeatureLayer_management(poligonos, "poligonos_lyr")

#erase dos poligonos com o buffer
arcpy.Erase_analysis("poligonos_lyr", "buffer", "erase")


#delete das camadas temporarias
arcpy.Delete_management("ftl")
arcpy.Delete_management("featuretoline_lyr")
arcpy.Delete_management("featuretoline_lyr2")
arcpy.Delete_management("buffer")
arcpy.Delete_management("poligonos_lyr")
arcpy.Delete_management("erase")

# Path: SIGAM_SnapOff.py
