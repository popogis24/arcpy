import arcpy

 

 

# variavel do raster
raster = fr"R:\09-Banco_De_Dados_Geografico\01-Clientes\PMF\RIOS_URBANOS\Raster\MDE_SIGSC\mde_floripa2.tif"
#variavel do shapefile
shapefile = fr"R:\\09-Banco_De_Dados_Geografico\\01-Clientes\\PMF\\RIOS_URBANOS\\Banco_Dados.gdb\\Dados_Caruso\\MICROBACIAS_ESTUDO_quantitativos"

 

 

#faça um extract by mask do raster utilizando o cada feição do shapefile usando a coluna nm_utp, e salve cada raster com o nome da feição
with arcpy.da.SearchCursor(shapefile, ["nm_utp"]) as cursor:
    for row in cursor:
        #cria um layer temporario para cada feição
        shapefile1=arcpy.MakeFeatureLayer_management(shapefile, "layer", "nm_utp = '" + row[0] + "'")
        arcpy.gp.ExtractByMask_sa(raster, shapefile1, fr"R:\\09-Banco_De_Dados_Geografico\\01-Clientes\\PMF\\RIOS_URBANOS\\Raster\\Div_Bacias\\" + row[0] + ".tif")





