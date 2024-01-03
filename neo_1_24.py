import os
import arcpy
import arcpy.analysis as an
import arcpy.management as mn
import arcpy.converson as cs

lt = input('Digite o caminho do shapefile: ')
nome_da_lt = input('Digite o nome da LT: ')
numero_do_lote = input('Digite o número do lote: ')
workspace = input('Digite o caminho do workspace: ')
pasta_excel = input('Digite o caminho da pasta onde serão salvos os arquivos excel: ')
uso_solo = input('Digite o nome do shapefile de uso do solo: ')

arcpy.env.workspace = workspace

def intersect(fc,uso):
    
    output = os.path.join(workspace, fr"Lote{numero_do_lote}_{nome_da_lt}_x_Uso_do_Solo")

    uso_clipado = an.PairwiseClip(uso, fc, fr"temp_{nome_da_lt}_clip")
    uso_dissolvido = an.PairwiseDissolve(uso_clipado, output, "Classe")
    uso_calculado = mn.CalculateField(uso_dissolvido, "Area_ha", "!shape.area@hectares!", "PYTHON3")
    mn.Delete(uso_clipado)
    return uso_calculado

def toexcel(shp):
    shapefile_final = intersect(lt,uso_solo)
    nome_shapefile_final = os.path.basename(shapefile_final)
    cs.TableToExcel(shapefile_final, os.path.join(pasta_excel, fr"{nome_shapefile_final}.xlsx"))





    