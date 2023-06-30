
#insira do codeblock


unidade_baixo_pot=["Depósitos de barreira holocênica - Depósitos de praiais e cristas lagunas",
"Depósitos de barreira holocênica - Depósitos de retrabalhamento eólico",
"Depósitos de barreira holocênica - depósitos deltáicos",
"Depósitos de barreira holocênica - Depósitos eólicos",
"Depósitos de planície lagunar atual",
"Depósitos colúvio-aluvionares",
"Depósitos flúvio-lagunares",
"Depósitos de leque aluvial",
"Depósitos de planície de inundação",
"Depósitos eólicos atuais",
"Serra Alta"]

unidade_alto_pot=["Depósitos de turfeira","Depósitos praiais antigos",
"Depósitos de planície lagunar",
"Depósitos de planície lagunar associadas a barreira III",
"Depósitos de barreira pleistocênica 2 - Depósitos eólicos",
"Depósitos de barreira pleistocênica 2 - Depósitos praiais e eólicos",
"Depósitos de barreira pleistocênica 3 - Depósitos de planície lagunar",
"Depósitos de barreira pleistocênica 3 - Depósitos eólicos",
"Botucatu",
"Rio Bonito"]

unidade_medio_pot=["Rio do Rasto","Irati","Palermo"]
ocorr_improvavel=["Serra Geral","Caxias","Gramado"]

def paleo(periodo,epoca,unidade):
    if periodo == "Neógeno" and epoca == "Holoceno" and unidade in unidade_baixo_pot:
        return "Baixo Potencial"
    elif periodo == "Neógeno" and epoca == "Holoceno" and unidade in unidade_alto_pot:
        return "Alto Potencial"
    elif periodo == "Neógeno" and epoca == "Pleistoceno" and unidade in unidade_alto_pot:
        return "Alto Potencial"
    elif periodo == "Cretáceo" and epoca == "Inferior" and unidade in ocorr_improvavel:
        return "Ocorrência Improvável"
    elif periodo == "Jurássico" and epoca == "Superior" and unidade in unidade_alto_pot:
        return "Alto Potencial"
    elif periodo == "Permiano" and unidade in unidade_baixo_pot:
        return "Baixo Potencial"
    elif periodo == "Permiano" and unidade in unidade_medio_pot:
        return "Médio Potencial"
    elif periodo == "Permiano" and unidade in unidade_alto_pot:
        return "Alto Potencial"
    else:
        return ""
    
