import arcpy

# Define os inputs como parâmetros do script
torres = arcpy.GetParameterAsText(0)
lt = arcpy.GetParameterAsText(1)

# Define as variáveis de saída
field_comprimento = arcpy.GetParameterAsText(2)
field_largura = arcpy.GetParameterAsText(3)
output = arcpy.GetParameterAsText(4)

#adiciona a nova field
arcpy.management.AddField(torres, "comp2", 'FLOAT', "", "", "", "", "", "", "")

#calcula a nova field
arcpy.management.CalculateField(torres, 'comp2', fr'!{field_comprimento}!/2', "", "", "", "")

# Processa o buffer das torres
arcpy.Buffer_analysis(torres, "buff1output", field_comprimento, "FULL", "ROUND", "NONE", "", "PLANAR")

# Processa o intersect
arcpy.Intersect_analysis(["buff1output", lt], "intersect_output", "ALL", "", "INPUT")

# Processa o buffer da lt
arcpy.Buffer_analysis('intersect_output', output, field_largura, "FULL", "FLAT", "NONE", "", "PLANAR")

#adiciona a nova field
arcpy.management.AddField(output, "STATUS", 'TEXT', "", "", "", "", "", "", "")

# Extrai os vertices
arcpy.management.FeatureVerticesToPoints(lt, 'ftv', "")

# Cria uma camada a partir do arquivo de saída
arcpy.management.MakeFeatureLayer(output, 'output_layer')

# Select by location
arcpy.management.SelectLayerByLocation('output_layer', 'INTERSECT', 'ftv', "", "", "")

# Calcula a nova field apenas nas features selecionadas
arcpy.management.CalculateField('output_layer', 'STATUS', "'Refazer'", "", "", "", "")
