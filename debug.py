    if filename == 'Adutoras_SNIRH_ANA_2021'
        fields_to_keep = ['nm_adt_adu','adt_status','adt_uf']
    elif filename == 'Aerodromos_ANAC_2022':
        fields_to_keep = ['Codigo_OAC','CIAD','Denominaca']
    elif filename == 'Aerogeradores_ANEEL_2023':
        fields_to_keep = ['NOME_EOL','DEN_AEG','POT_MW','CEG','OPERACAO']
    elif filename == 'APCB_Amazonia':
        fields_to_keep = ['Import_bio','Prior_acao','COD_Area']
    elif filename == 'APCB_Caatinga':
        fields_to_keep = ['Import_bio','Prior_acao','COD_area','Nome_area']
    elif filename == 'APCB_Cerrado_Pantanal':
        fields_to_keep = ['Import_bio','Prior_acao','COD_area','NOME']
    elif filename == 'APCB_Mata_Atlantica':
        fields_to_keep = ['ImportBio','Prioridade','COD_area']
    elif filename == 'APCB_ZonaCosteira':
        fields_to_keep = ['NOME_AP','IMP','PRIO']
    elif filename == 'Aves_Migratorias_Areas_Ameacadas_CEMAVE_2022':
        fields_to_keep = []#não tem campos de interesse, verificar se não vai ter bug
    elif filename == 'Aves_Migratorias_Areas_Concentracao_CEMAVE_2022':
        fields_to_keep = []#não tem campos de interesse, verificar se não vai ter bug
    elif filename == 'Bases_de_Combustíveis_EPE':
        fields_to_keep = ['nome_base','munic']
    elif filename == 'Bases_de_GLP_EPE':
        fields_to_keep = ['nome_base','munic','razao_soci']
    elif filename == 'Biomas_IBGE_2019_250000':
        fields_to_keep = ['Bioma']
    elif filename == 'Blocos_Disponiveis_OPC_1009_ANP':
        fields_to_keep = ['nome_bacia','nomenclatu','nome_setor']
    elif filename == 'Cavidades_CANIE_19122022':
        fields_to_keep = ['Caverna','Municipio','Localidade']
    elif filename == 'Centrais_Geradoras_Hidrelétricas_CGH_ANEEL':
        fields_to_keep = ['NOME']
    elif filename == 'CGH_Base_Existente_EPE':
        fields_to_keep = ['NOME']
    elif filename == 'CGH_Expansao_Planejada_EPE':
        fields_to_keep = ['Nome']
    elif filename == 'Conservacao_Aves_IBAS':
        fields_to_keep = ['Nome_1']
    elif filename == 'Dutos_de_escoamento_EPE':
        fields_to_keep = ['Nome_Dut_1','Categoria']
    elif filename == 'Dutovias_MINFRA_2018':
        fields_to_keep = ['Nome_Duto']
    elif filename == 'EOL_Base_Existente_EPE':
        fields_to_keep = ['Nome']
    elif filename == 'EOL_Expansao_Planejada_EPE':
        fields_to_keep = ['nome']
    elif filename == 'Ferrovias_MINFRA':
        fields_to_keep = ['tip_situac','bitola']
    elif filename == 'Gasodutos_de_distribuição_EPE_2023':
        fields_to_keep = ['Distrib']
    elif filename == 'Gasodutos_de_transporte_EPE_2023':
        fields_to_keep = ['Nome_Dut_1','Categoria']
    elif filename == 'Geologia_IBGE':
        fields_to_keep = ['nm_unidade']
    elif filename == 'Geomorfologia_IBGE':
        fields_to_keep = ['nm_unidade']
    elif filename == 'Hidrovias_ANTAQ':
        fields_to_keep = ['HID_NM','HID_DS_CUR']
    elif filename == 'IBAs_MataAtlantica_SaveBrasil_2023':
        fields_to_keep = ['Nome_1','Bioma']
    elif filename == 'Lei_Mata_Atlantica_MMA':
        fields_to_keep = []#não tem campos de interesse, verificar se não vai ter bug
    elif filename == 'Localidades_IBGE_2010':
        fields_to_keep = 'NM_LOCALID'
    elif filename == 'LT_Existente_EPE_2023':
        fields_to_keep = ['Nome','Tensao','Ano_opera']
    elif filename == 'LT_Planejada_EPE_2023':
        fields_to_keep = ['Nome','Tensao']
    elif filename == 'Municipios_2022_IBGE':
        fields_to_keep = ['NM_MUNICIP','SIGLA_UF']
    elif filename == 'Ocorrencias_Fossiliferas_CPRM':
        fields_to_keep = ['LOCALIDADE']
    elif filename == 'PCH_Base_Existente_EPE':
        fields_to_keep = ['NOME']
    elif filename == 'PCH_Expansao_Planejada_EPE_2023':
        fields_to_keep = 'nome'
    elif filename == 'Pedologia_IBGE':
        fields_to_keep = ['legenda']
    elif filename == 'Pequenas_Centrais_Hidrelétricas_PCH_ANEEL':ibas
        fields_to_keep = ['NOME']
    elif fields_to_keep == 'Pivo_Central_Irrigacao_ANA_2019':
        fields_to_keep = ['NM_MUNICIP']
    elif filename == 'Plantas_de_biodiesel_EPE':
        fields_to_keep = ['Nome']
    elif filename == 'Plantas_de_etanol_EPE':
        fields_to_keep = ['Nome']
    elif filename == 'Polos_de_processamento_de_gás_natural_EPE':
        fields_to_keep = ['Nome']
    elif filename == 'Potencial_Cavidades_ICMBio':
        fields_to_keep = ['GRAU_DE_PO']
    elif filename == 'Reserva_Biodiversidade_Mata_Atlantica_RBMA':
        fields_to_keep = 'CLASSE'
    elif filename == 'Rodovia_Estadual_DNIT':
        fields_to_keep =['Tipo_Trech','Unidade_Fe','Codigo_Rod']
    elif filename == 'Rodovia_Federal_DNIT':
        fields_to_keep =['Nome_Tipo','Codigo_BR']
    elif filename == 'RPPNs_ICMBio':
        fields_to_keep = ['nome']
    elif filename == 'Sitios_Arqueologicos_IPHAN':
        fields_to_keep = ['identifica']
    elif filename == 'Subestações_Base_Existente_EPE_2023':
        fields_to_keep = ['Nome','Tensao','Ano_Opera']
    elif filename == 'Subestacoes_Expansao_Planejada_EPE_2023':
        fields_to_keep = ['Nome','Tensao','Ano_Opera']
    elif filename == 'Terminais_de_Petroleo_e_Derivados_EPE':
        fields_to_keep = ['nome_ter','munic']
    elif filename == 'Territorios_Quilombolas_INCRA_2023':
        fields_to_keep = ['nm_comunid','nm_municip','nr_process','fase','responsave']
    elif filename == 'Terras_Indigenas_FUNAI':
        fields_to_keep = ['terrai_nom','municipio','etnia_nome']
    elif filename == 'Trecho_Drenagem_ANA_2013':
        fields_to_keep = []#não tem campos de interesse, verificar se não vai ter bug
    elif filename == 'UHE_Base_Existente_EPE_2023':
        fields_to_keep = ['NOME']
    elif filename == 'Unidades_de_Conservacao_MMA':
        fields_to_keep =['NOME_UC1','CATEGORI3','ESFERA5','GRUPO4','ANO_CRIA6']
    elif filename == 'Usina_Fotovoltaica_UFV_ANEEL_2023':
        fields_to_keep = ['nome','munic']
    elif filename == 'Usina_Termeletricas_UTE_ANEEL_2023':
        fields_to_keep = ['nome']
    elif filename == 'Usinas_Hidrelétricas_UHE_ANEEL_2023':
        fields_to_keep = ['NOME']
    elif filename == 'UTE_Biomassa_Existente_EPE_2023':
        fields_to_keep = ['nome']
    elif filename == 'Vegetacao_IBGE':
        fields_to_keep = ['legenda']
    elif filename == 'Vilas_IBGE_2021':
        fields_to_keep = ['nome']