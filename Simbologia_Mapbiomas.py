layer = arcpy.GetParameterAsText(0)
nova_coluna = arcpy.GetParameterAsText(1)


codeblock_class= '''
def analise(x):
    if x == 1:
        return"Floresta"
    if x == 3:
        return"Formação Florestal"
    if x == 4:
        return"Formação Savânica"
    if x == 5:
        return"Mangue"
    if x == 49:
        return"Restinga Arborizada"
    if x == 10:
        return"Formação Natural não Florestal"
    if x == 11:
        return"Campo Alagado e Área Pantanosa"
    if x == 12:
        return"Formação Campestre"
    if x == 32:
        return"Apicum"
    if x == 29:
        return"Afloramento Rochoso"
    if x == 50:
        return"Restinga Herbácea"
    if x == 13:
        return"Outras Formações não Florestais"
    if x == 14:
        return"Agropecuária"
    if x == 15:
        return"Pastagem"
    if x == 18:
        return"Agricultura"
    if x == 19:
        return"Lavoura Temporária"
    if x == 39:
        return"Soja"
    if x == 20:
        return"Cana"
    if x == 40:
        return"Arroz"
    if x == 62:
        return"Algodãobeta"
    if x == 41:
        return"Outras Lavouras Temporárias"
    if x == 36:
        return"Lavoura Perene"
    if x == 46:
        return"Café"
    if x == 47:
        return"Citrus"
    if x == 48:
        return"Outras Lavouras Perenes"
    if x == 9:
        return"Silvicultura (monocultura)"
    if x == 21:
        return"Mosaico de Usos"
    if x == 22:
        return"Área não Vegetada"
    if x == 23:
        return"Praia, Duna e Areal"
    if x == 24:
        return"Área Urbanizada"
    if x == 30:
        return"Mineração"
    if x == 25:
        return"Outras Áreas não Vegetadas"
    if x == 26:
        return"Corpo D'água"
    if x == 33:
        return"Rio, Lago e Oceano"
    if x == 31:
        return"Aquicultura"
    if x == 27:
        return"Não observado"
'''


arcpy.management.CalculateField(in_table=layer, field=nova_coluna, expression='analise(!gridcode!)', expression_type='PYTHON3', code_block=codeblock_class)

