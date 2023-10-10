import arcpy
import os.path

arcpy.env.addOutputsToMap = False
arcpy.env.overwriteOutput = True

#seta um workspace
arcpy.env.workspace = fr'R:\09-Banco_De_Dados_Geografico\01-Clientes\CHESF\PreLeilao_Lote2_3\GDB_Dados_Referenciais\PL_LOTE_02_03.gdb\Dados_Referenciais_F23'
#area do clip
clip = fr'C:\Users\anderson.souza\Downloads\FUSO_23.shp'
dataset_final= fr'R:\09-Banco_De_Dados_Geografico\01-Clientes\CHESF\PreLeilao_Lote2_3\GDB_Dados_Referenciais\PL_LOTE_02_03_Clipped.gdb\Dados_Referenciais_F23'

#conta quantas features tem no workspace

var_global = 0
#lista todos os feature classes dentro do workspace
fcList = arcpy.ListFeatureClasses()
count = len(fcList)
list_error = []
for fc in fcList:
    var_global += 1
    print("Andamento: " + str(var_global) + " de " + str(count))
    try:
        #clipa cada um dos feature classes e salva no mesmo dataset
        arcpy.Clip_analysis(fc, clip, os.path.join(dataset_final, fc + "_clip"))
        print("Clip realizado com sucesso para o feature class: " + fc)
    except:
        print("Erro no clip do feature class: " + fc + "... Tentando novamente...")
        try:
            #select by location
            arcpy.MakeFeatureLayer_management(fc, "layer")
            arcpy.SelectLayerByLocation_management("layer", "INTERSECT", clip)
            #salva o resultado do select by location em memoria
            arcpy.CopyFeatures_management("layer", "in_memory/layer")
            #clipa o resultado do select by location
            arcpy.Clip_analysis("in_memory/layer", clip, os.path.join(dataset_final, fc + "_clip"))
            print("Clip realizado com sucesso para o feature class: " + fc)
        except:
            try:
                #intersect
                arcpy.Intersect_analysis([fc, clip], os.path.join(dataset_final, fc + "_clip"))
                print("Clip realizado com sucesso para o feature class: " + fc)
            except:
                print("não deu...")
                fc_error = fc 
                list_error.append(fc_error)
                continue

        continue

print('Essas features deram erro: ')
for erro in list_error:
    print(erro)
