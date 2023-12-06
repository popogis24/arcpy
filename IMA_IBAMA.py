import arcpy
import os

arcpy.env.overwriteOutput = True
acessos = arcpy.GetParameterAsText(0)
app = arcpy.GetParameterAsText(1)
junkspace = arcpy.GetParameterAsText(2)
output = arcpy.GetParameterAsText(3)
arcpy.env.workspace = junkspace
arcpy.env.addOutputsToMap = False


#split acessos
acessos = acessos.split(";")
app = arcpy.management.CopyFeatures(in_features=app, out_feature_class='app_ver')
arcpy.AddField_management(app, "Verifica", "TEXT")
arcpy.CalculateField_management(app, "Verifica", "1")

for acesso in acessos:
    filename = os.path.basename(acesso)
    arcpy.AddMessage(filename)
    acesso = arcpy.Dissolve_management(acesso, "dissolve", ["Name", "FolderPath"], "", "MULTI_PART", "DISSOLVE_LINES")

    identity = arcpy.Identity_analysis(acesso, app, "identity", "ALL", "", "NO_RELATIONSHIPS")
    identity4m_layer = arcpy.MakeFeatureLayer_management(identity, "identity4m_layer")
    sl_4m = arcpy.SelectLayerByAttribute_management(identity4m_layer, "NEW_SELECTION", "Verifica <> '1'")
    buffer4m = arcpy.Buffer_analysis(sl_4m, "buffer4m", "4 Meters", "FULL", "ROUND", "NONE", "", "PLANAR")



    sl_1 = arcpy.SelectLayerByAttribute_management(identity4m_layer, "NEW_SELECTION", "Verifica = '1'")
    buff_clip = arcpy.Buffer_analysis(sl_1,'buffclip','4 Meters','FULL','FLAT','NONE','','PLANAR')
    sl4m_erased = arcpy.analysis.Erase(buffer4m,buff_clip,'sl4m_erased')
    buffer3m = arcpy.Buffer_analysis(sl_1, "buffer3m", "3 Meters", "FULL", "FLAT", "NONE", "", "PLANAR")
    merge = arcpy.Merge_management([buffer3m, sl4m_erased], "Produto_Final")
    #make feature layer do merge
    merge_layer = arcpy.MakeFeatureLayer_management(merge, "merge_layer")


    with arcpy.da.SearchCursor(merge, ["FID"]) as cursor:
        #cria um shape vazio para receber os dados
        arcpy.CreateFeatureclass_management(arcpy.env.workspace, "Produto_Final_no_Over", "POLYGON", "", "", "", "Produto_Final")
        for row in cursor:
            #seleciona a linha e da um erase com o shape vazio
            sl = arcpy.SelectLayerByAttribute_management(merge_layer, "NEW_SELECTION", "FID = {}".format(row[0]))
            erase = arcpy.Erase_analysis(sl, "Produto_Final_no_Over", "erase_{}".format(row[0]))
            #da um append no erase com o shape vazio
            arcpy.Append_management(erase, "Produto_Final_no_Over", "NO_TEST")
            #deleta o erase
            arcpy.Delete_management(erase)
            
        

    #explode to multi part o merge
    explode = arcpy.MultipartToSinglepart_management(merge, "explode")
    #transforma em ponto
    centroids = arcpy.FeatureToPoint_management(explode, "centroids", "INSIDE")
    #dá um spatial join no produto_final_no_over com os centroids

    spatial_join = arcpy.SpatialJoin_analysis("Produto_Final_no_Over", centroids, os.path.join(output,filename+'_P.shp'), "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "INTERSECT", "", "")

#apaga tudo da do workspace