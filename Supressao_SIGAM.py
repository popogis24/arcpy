uso_base = arcpy.GetParameterAsText(0)
shape_sigam = arcpy.GetParameterAsText(1)
id_projeto = arcpy.GetParameterAsText(2)
campo_classe = arcpy.GetParameterAsText(3)
campo_estagio = arcpy.GetParameterAsText(4)
campo_tipo = arcpy.GetParameterAsText(5)

########codeblocks########
codeblock_idtipovege = '''
def vegetacao_classe(veg_classe):
    if veg_classe == 'Contato Manguezal - Floresta Alta de Restinga':
        return '11'
    elif veg_classe == 'Floresta Alta de Restinga':
        return '6'
    elif veg_classe == 'Floresta Ombrófila Densa':
        return '12'
    elif veg_classe == 'Manguezal':
        return '2'
    else:
        return '0'
'''
codeblock_idtipoarea =''' 
def tipoarea (tipo):
    if tipo == 'Cursos d\'água':
        return == '7'
    elif tipo == 'Manguezal':
        return == '13'
    elif tipo == 'Nascentes':
        return == '14'
    elif tipo == '':
        return == 'Área Comum Não protegida'
    else:
        tipo == 'out'
'''

codeblock_vegtipo = '''
def tipoveg(idvegetacao):
    if idvegetacao == 8:
        return 'Brejo de Restinga'
    elif idvegetacao == 21:
        return 'Campo Cerrado'
    elif idvegetacao == 23:
        return 'Campo Limpo Cerrado'
    elif idvegetacao == 24:
        return 'Campo Sujo Cerrado'
    elif idvegetacao == 22:
        return 'Campo Úmido Cerrado'
    elif idvegetacao == 14:
        return 'Campos de Altitude'
    elif idvegetacao == 19:
        return 'Cerradão (c/estágio susc.)'
    elif idvegetacao == 20:
        return 'Cerrado Strictu Sensu (c/estágio susc.)'
    elif idvegetacao == 4:
        return 'Escrube (c/estágio susc.)'
    elif idvegetacao == 6:
        return 'Floresta Alta de Restinga (c/estágio susc.)'
    elif idvegetacao == 5:
        return 'Floresta Baixa de Restinga (c/estágio susc.)'    
    elif idvegetacao == 17:
        return 'Floresta de Transição Estacional/Cerradão (c/estágio susc.)'
    elif idvegetacao == 11:
        return 'Floresta de Transição Restinga/Encosta (Ombrófila Densa) (c/'
    elif idvegetacao == 16:
        return 'Floresta Estacional Decidual (Tropical Caducifólia) (c/estág'
    elif idvegetacao == 15:
        return 'Floresta Estacional Semidecidual (Tropical Subcaducifólia) ('
    elif idvegetacao == 12:
        return 'Floresta Ombrófila Densa (Pluvial Tropical) (c/estágio susc.'
    elif idvegetacao == 13:
        return 'Floresta Ombrófila Mista (Araucária) (c/estágio susc.)'
    elif idvegetacao == 9:
        return 'Floresta Paludosa'
    elif idvegetacao == 10:
        return 'Floresta Paludosa sobre Substrato Turfoso (c/estágio susc.)'
    elif idvegetacao == 2:
        return 'Manguezal'
    elif idvegetacao == 1:
        return 'Sem vegetação'
    elif idvegetacao == 18:
        return 'Vegetação com Influência Fluvial (Várzea)'
    elif idvegetacao == 25:
        return 'Vegetação com Influência Fluvial (Várzea)'
    elif idvegetacao == 3:
        return 'Vegetação de Praias e Dunas'
    elif idvegetacao == 7:
        return 'Vegetação Entre Cordões'
    elif idvegetacao == 28:
        return 'Vegetação Exótica'
    elif idvegetacao == 30:
        return 'Vegetação exótica com sub-bosque'
    else:
        return 'erro'
'''

codeblock_areatipo = '''
def remover_zeros(texto):
   novo_texto = texto.replace("00", "")
   return novo_texto
'''
codeblock_desestagio = '''
def estagioid(idestagiox):
    if idestagiox == 278:
        return 'Estágio Secundário Médio'
    elif idestagiox == 277:
        return 'Estágio Secundário Avançado'
    elif idestagiox == 279:
        return 'Estágio Secundário Inicial'
    elif idestagiox == 203:
        return 'Estágio Pioneiro'
    elif idestagiox == 204:
        return == 'Estágio Primário'
    else:
        return "Não se aplica"
'''
codeblock_idestagio ='''
def usoestagio(estagio):
    if estagio == "":
        return '297'
    elif estagio == "Avançado":
        return '277'
    elif estagio == 'Médio':
        return == '278'
    else:
        return ''
    '''
#multipart to singlepart
arcpy.management.MultipartToSinglepart(uso_base, 'exploded_uso_base')

#feature to point
arcpy.management.FeatureToPoint('exploded_uso_base', 'uso_base_point', 'INSIDE')

#spatial join
arcpy.analysis.SpatialJoin(shape_sigam, 'uso_base_point', 'shape_sigam', 'JOIN_ONE_TO_ONE', 'KEEP_ALL', "", "", "", "")

#CALCULATE FIELD
#ID_TIPO_AREA
arcpy.management.CalculateField(shape_sigam, 'idTipoArea', 'tipoarea(!campo_classe!)', "", codeblock_idtipoarea, "", "")

#ID_TIPOVEGE
arcpy.management.CalculateField(shape_sigam, 'idTipoVege', fr'vegetacao_classe(!{campo_classe}!)', "", codeblock_idtipovege, "", "")

#VegTipo
arcpy.management.CalculateField(shape_sigam, 'VegTipo', 'tipoveg(!idTipoVege!)', "", codeblock_vegtipo, "", "")
    
#AreaTipo
arcpy.management.CalculateField(shape_sigam, 'AreaTipo', 'remover_zeros(!AreaTipo!)', "", codeblock_areatipo, "", "")

#idEstagioS
arcpy.management.CalculateField(shape_sigam, 'idEstagioS', fr'estagioz(!{campo_estagio}!)', "", codeblock_idestagio , "", "")

#desEstagio
arcpy.management.CalculateField(shape_sigam, 'desEstagio', 'estagioid(!idEstagioS!)', "", codeblock_desestagio, "", "")

#IdProcDet
arcpy.management.CalculateField(shape_sigam, 'IdProcDet', fr'{id_projeto}', "", "", "", "")

#DATAATUALIZ
arcpy.management.CalculateField(shape_sigam, 'datAtualiz', "10/10/2001", "", "", "", "")