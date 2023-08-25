import arcpy

arcpy.env.overwriteOutput = True

poligonos = arcpy.GetParameterAsText(0)
output = arcpy.GetParameterAsText(1)

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
 
#polygon to line codigo completo
arcpy.PolygonToLine_management(poligonos, "ftl", "IDENTIFY_NEIGHBORS")

#transforma o ftl em layer
arcpy.MakeFeatureLayer_management("ftl", "featuretoline_lyr")

#selecione todas as linhas que tem dois vizinhos
arcpy.SelectLayerByAttribute_management("featuretoline_lyr", "NEW_SELECTION", '"LEFT_FID" <> -1 AND "RIGHT_FID" <> -1')

#crie uma camada temporaria com as linhas selecionadas
arcpy.MakeFeatureLayer_management("featuretoline_lyr", "featuretoline_lyr2")

#buffer de 10 milimetros nas linhas selecionadas, full, round, all, geodesic
arcpy.Buffer_analysis("featuretoline_lyr2", "buffer", "10 Millimeters", "FULL", "ROUND", "ALL", "", "GEODESIC")

#crie uma camada temporaria com os poligonos
arcpy.MakeFeatureLayer_management(poligonos, "poligonos_lyr")

#erase dos poligonos com o buffer
arcpy.Erase_analysis("poligonos_lyr", "buffer", "erase")

#explode multpart to singlepart
arcpy.MultipartToSinglepart_management("erase", output)

#calculate field com autoincremento como double
arcpy.CalculateField_management(output, "div", "autoIncrement()", "PYTHON3", autoincremento,"LONG", "")


#output
#with arcpy.EnvManager(outputZFlag="Disabled", outputMFlag="Disabled"):
#arcpy.CopyFeatures_management("erase", output)

#delete das camadas temporarias
arcpy.Delete_management("ftl")
arcpy.Delete_management("featuretoline_lyr")
arcpy.Delete_management("featuretoline_lyr2")
arcpy.Delete_management("buffer")
arcpy.Delete_management("poligonos_lyr")
arcpy.Delete_management("erase")

# Path: SIGAM_SnapOff.py
