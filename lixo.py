def dissolve(fc):
    fields_interesse = []
    filename = os.path.basename(fc)
    if filename == 'Adutoras_SNIRH_ANA_2021':
        fields_interesse.extend(['ADUTORA','SITUAÇÃO'])
    elif filename == 'Aerodromos_ANAC':
        fields_interesse.extend(['Código_OAC','CIAD','Nome'])
    elif filename == 'Aerogeradores_ANEEL_2023':
        fields_interesse.extend(['NOME_EOL','DEN_AEG','POT_MW','CEG','OPERACAO'])
    elif filename == 'Aproveitamento_Hidreletricos_AHE_ANEEL':
        fields_interesse.extend(['NOME','MUNIC_1','UF_1','RIO','ATO_LEGAL','TIPO_AHE','FASE','Menor_Distancia'])
    elif filename == 'Area_Imoveis_Rurais_SICAR_2023':
        fields_interesse.extend(['COD_IMOVEL','NUM_AREA','COD_ESTADO','SITUACAO','CONDICAO_I','NOM_MUNICI','TIPO_IMOVE'])
    elif filename == 'Areas_Quilombolas_INCRA':
        fields_interesse.extend(['nr_process','nm_comunid','nm_municip','cd_uf'])
    elif filename == 'Areas_Urbanizadas_IBGE_2019':
        fields_interesse.extend(['Densidade','Tipo','Menor_Distancia','Vertices','UF'])
    elif filename == 'Assentamentos_INCRA':
        fields_interesse.extend(['cd_sipra','nome_proje','municipio','area_hecta','capacidade','num_famili'])
    elif filename == 'Aves_Migratorias_AI_Riqueza_CEMAVE_2019':
        fields_interesse.extend([]):
    elif filename == 'Aves_Migratorias_Areas_Ameacadas_CEMAVE_2022':
        fields_interesse.extend(['name']):
    elif filename == 'Aves_Migratorias_Areas_Concentracao_CEMAVE_2022':
        fields_interesse.extend(['Critério','name'])
    elif filename == 'Blocos_Disponiveis_OPC_1009_ANP':
        fields_interesse.extend(['nome_bacia','nomenclatu','situacao_b','nome_setor','indice_blo','AreaANP'])
    elif filename == 'Bases_de_Combustíveis_EPE':
        fields_interesse.extend(['nome_base','munic','uf'])
    elif filename == 'Bases_de_GLP_EPE':
        fields_interesse.extend(['nome_base','munic','uf'])
    elif filename == 'Biomas_IBGE_2019_250000':
        fields_interesse.extend(['Bioma'])
    elif filename == 'Cavidades_CANIE_19122022':
        fields_interesse.extend(['Registro_N','Caverna','Municipio','UF','Localidade'])
    elif filename == 'Centrais_Geradoras_Hidrelétricas_CGH_ANEEL':
        fields_interesse.extend(['NOME','MUNIC_1','UF_1','RIO','ATO_LEGAL','TIPO_AHE'])
    elif filename == 'Conservacao_Aves_IBAS':
        fields_interesse.extend(['Código','Nome_1','Bioma'])
    elif filename == 'CGH__Base_Existente_EPE':
        fields_interesse.extend(['NOME','RIO','potencia','ceg'])
    elif filename == 'CGH__Expansão_Planejada_EPE':
        fields_interesse.extend(['NOME','RIO','potencia','ceg'])
    elif filename == 'Declividade_Caruso':
        fields_interesse.extend(['Classes'])
    elif filename == 'Dutovias_Gas_Oleo_Minerio_ANP':
        fields_interesse.extend(['name'])
    else:
        pass
    output = arcpy.Dissolve_management(fc, "fcdissolved", fields_interesse) 
    return output, fields_interesse