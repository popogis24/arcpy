# Definindo a lista de chaves
chaves = [
    "nm_adt_adu", "adt_status", "adt_uf", "Codigo_OAC", "CIAD", "Denominaca",
    "NOME_EOL", "DEN_AEG", "POT_MW", "CEG", "OPERACAO", "Import_bio", "Prior_acao",
    "COD_Area", "Nome_area", "NOME", "ImportBio", "Prioridade", "COD_area", "NOME_AP",
    "IMP", "PRIO", "nome_base", "munic", "razao_soci", "Bioma", "nome_bacia",
    "nomenclatu", "nome_setor", "Caverna", "Municipio", "Localidade", "tip_situac",
    "bitola", "Distrib", "Nome_Dut_1", "Categoria", "nm_unidade", "HID_NM",
    "HID_DS_CUR", "Nome_1", "NM_LOCALID", "Tensao", "Ano_opera", "NM_MUNICIP",
    "SIGLA_UF", "LOCALIDADE", "Nome_Duto", "NOME_ter", "GRAU_DE_PO", "CLASSE",
    "Tipo_Trech", "Unidade_Fe", "Codigo_Rod", "Nome_Tipo", "Codigo_BR", "nome",
    "Identifica", "Nome_Opera", "nm_comunid", "nm_municip", "nr_process", "fase",
    "responsave", "terrai_nom", "etnia_nome"
]

# Definindo a lista de valores (os significados)
valores = [
    "Nome do aditivo/adutora", "Status do aditivo", "UF do aditivo", "Código OAC",
    "CIAD", "Denominação", "Nome do EOL", "Denominação AEG", "Potência em MW", "CEG",
    "Operação", "Importância biológica", "Prioridade da ação", "Código da área",
    "Nome da área", "Nome", "Importância biológica", "Prioridade", "Código da área",
    "Nome da AP", "Importância", "Prioridade", "Nome da base", "Município",
    "Razão social", "Bioma", "Nome da bacia", "Nomenclatura", "Nome do setor",
    "Caverna", "Município", "Localidade", "Tipo de situação", "Bitola", "Distribuição",
    "Nome do dut 1", "Categoria", "Nome da unidade", "HID_NM", "HID_DS_CUR",
    "Nome 1", "Nome da localidade", "Tensão", "Ano de operação", "Nome do município",
    "Sigla UF", "Localidade", "Nome do duto", "Nome ter", "Grau de poluição",
    "Classe", "Tipo de trecho", "Unidade federativa", "Código rodoviário",
    "Nome do tipo", "Código BR", "Nome", "Identificação", "Nome da operação",
    "Nome da comunidade", "Nome do município", "Número do processo", "Fase",
    "Responsável", "Terreno nomeado", "Nome da etnia"
]

# Criando o dicionário
dicionario = dict(zip(chaves, valores))

# Exibindo o dicionário
for key in dicionario:
    print(fr"'{key}'", ":", fr"'{dicionario[key]}'")
'nm_adt_adu' : 'Nome do aditivo/adutora'
'adt_status' : 'Status do aditivo'
'adt_uf' : 'UF do aditivo'
'Codigo_OAC' : 'Código OAC'
'CIAD' : 'CIAD'
'Denominaca' : 'Denominação'
'NOME_EOL' : 'Nome do EOL'
'DEN_AEG' : 'Denominação AEG'
'POT_MW' : 'Potência em MW'
'CEG' : 'CEG'
'OPERACAO' : 'Operação'
'Import_bio' : 'Importância biológica'
'Prior_acao' : 'Prioridade da ação'
'COD_Area' : 'Código da área'
'Nome_area' : 'Nome da área'
'NOME' : 'Nome'
'ImportBio' : 'Importância biológica'
'Prioridade' : 'Prioridade'
'COD_area' : 'Código da área'
'NOME_AP' : 'Nome da AP'
'IMP' : 'Importância'
'PRIO' : 'Prioridade'
'nome_base' : 'Nome da base'
'munic' : 'Município'
'razao_soci' : 'Razão social'
'Bioma' : 'Bioma'
'nome_bacia' : 'Nome da bacia'
'nomenclatu' : 'Nomenclatura'
'nome_setor' : 'Nome do setor'
'Caverna' : 'Caverna'
'Municipio' : 'Município'
'Localidade' : 'Localidade'
'tip_situac' : 'Tipo de situação'
'bitola' : 'Bitola'
'Distrib' : 'Distribuição'
'Nome_Dut_1' : 'Nome do dut 1'
'Categoria' : 'Categoria'
'nm_unidade' : 'Nome da unidade'
'HID_NM' : 'HID_NM'
'HID_DS_CUR' : 'HID_DS_CUR'
'Nome_1' : 'Nome 1'
'NM_LOCALID' : 'Nome da localidade'
'Tensao' : 'Tensão'
'Ano_opera' : 'Ano de operação'
'NM_MUNICIP' : 'Nome do município'
'SIGLA_UF' : 'Sigla UF'
'LOCALIDADE' : 'Localidade'
'Nome_Duto' : 'Nome do duto'
'NOME_ter' : 'Nome ter'
'GRAU_DE_PO' : 'Grau de poluição'
'CLASSE' : 'Classe'
'Tipo_Trech' : 'Tipo de trecho'
'Unidade_Fe' : 'Unidade federativa'
'Codigo_Rod' : 'Código rodoviário'
'Nome_Tipo' : 'Nome do tipo'
'Codigo_BR' : 'Código BR'
'nome' : 'Nome'
'Identifica' : 'Identificação'
'Nome_Opera' : 'Nome da operação'
'nm_comunid' : 'Nome da comunidade'
'nm_municip' : 'Nome do município'
'nr_process' : 'Número do processo'
'fase' : 'Fase'
'responsave' : 'Responsável'
'terrai_nom' : 'Terreno nomeado'
'etnia_nome' : 'Nome da etnia'