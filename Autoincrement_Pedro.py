-Em "Pre-Logic Script Code" digite:


rec=0
def autoIncrement():
 global rec
 pStart = 1 #muda para nao iniciar do num 1
 pInterval = 1 #mude este numero para mudar o intervalo de seq
 if (rec == 0): 
  rec = pStart 
 else: 
  rec = rec + pInterval 
 return rec


-No campo abaixo "Nome do campo=" digite apenas:
autoIncrement()
