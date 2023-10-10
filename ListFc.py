import arcpy

arcpy.env.workspace = r"R:\09-Banco_De_Dados_Geografico\01-Clientes\ALUPAR\LT230KV_Henry_Borden\LI\LT\PROTOCOLO\LI_2022\CETESB\CETESB_Ajustes_Acessos\Shapefile\export.gdb"

featureclass = arcpy.ListFeatureClasses()
for fc in featureclass:
    filename = fc
    filename.replace(" ","_")
    print(fc," - concluido")
