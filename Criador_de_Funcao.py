field = input('Insira a coluna a ser alterada: ')
format_field = input ('Insira o formato da sua coluna: ').strip().casefold()


#Primeira letra maiúscula
def capt():
    capt = f'!{field}!.capitalize()'
    print(f'Cole isso aqui no campo "Expression": {capt}')

#Todas as letras minusculas
def casefold():
    casefold = f'!{field}!.casefold()'
    print(f'Cole isso aqui no campo "Expression: "{casefold}')

#Todas as letras maiusculas
def upper():
    upper = f'!{field}!.upper()'
    print(f'Cole isso aqui no campo "Expression: "{upper}')

#Remover espaços extras no início do texto
def strip():
    strip = f'!{field}!.strip()'
    print(f'Cole isso aqui no campo "Expression: "{strip}')

#Substituir caracteres
def replace():
    char_existente = input('Localizar os caracteres: ')
    char_novo = input('Substituir por: ')
    replace = f'!{field}!.replace("{char_existente}", "{char_novo}")'
    print(f'Cole isso aqui no campo "Expression": {replace}')
    
#Extrair parte do texto com base em uma posição inicial e final
def slice():
    start = int(input('Posição inicial: '))
    end = int(input('Posição final: '))
    sliced = f'!{field}![{start}:{end}]'
    print(f'Cole isso aqui no campo "Expression": {sliced}')

#Arredondar números com uma quantidade especifica de casas decimais
def round():
    decimals = int(input('Informe o número de casas decimais: '))
    rounded = f'round(!{field}!, {decimals})'
    print(f'Cole isso aqui no campo "Expression": {rounded}')

#Concatenar colunas 
def concatenate():
    second_field = input('Informe o nome da segunda coluna: ')
    concatenate = f'!{field}! + " " + !{second_field}!'
    print(f'Cole isso aqui no campo "Expression": {concatenate}')   

#Formatar como título
def title():
    title = f'!{field}!.title()'
    print(f'Cole isso aqui no campo "Expression": {title}')

#######
    
#Correlacionar colunas com a expressão "SE"
#def se()
#    field_correlate = input('Insira a coluna a ser correlacionada: '):
#    format_field_correlate = input('Sua coluna correlacionada é de texto? (Digite "SIM" ou "NÃO")').strip().casefold()
#        if field_correlate == 'sim':
#            return
#        elif field_correlate == 'não':
#            return 
            

def main():
    escolha = input('Qual será a tarefa realizada? ')
    if escolha == 'Primeira letra maiúscula':
        return capt()
    if escolha == 'Todas as letras minúsculas':
        return casefold()
    if escolha == 'Todas as letras maiúsculas':
        return upper()
    if escolha == 'Remover o espaço antes do texto':
        return strip()  
    if escolha == 'Localizar e substituir caracteres':
        return replace()
    if escolha == 'Extrair parte do texto com base em uma posição inicial e final':
        return slice()
    if escolha == 'Arredondar números com uma quantidade especifica de casas decimais':
        return round()
    if escolha == 'Concatenar duas colunas':
        return concatenate()
    if escolha == 'Formatar como título':
        return title()
    
main()



    
    
           
