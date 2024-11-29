#Código para calcular o valor de alguns parâmetros que serão usados
import pandas as pd
import numpy as np
from movimento_seguidor import omega

dados = pd.read_csv('dados.csv') 

c = []

for i in range(len(dados)):
    c.append(-(dados.loc[i,"posicao"] + dados.loc[i,'aceleracao'] / ((omega*2*np.pi)**2)))

ab = 0

for i in range(len(dados)):
    if abs(2.2 * dados.loc[i,'velocidade'] / (omega*2*np.pi)) > ab:
        ab = abs(2.2 * dados.loc[i,'velocidade'] / (omega*2*np.pi))

#for i in range(len(dados)):
#    alpha.append(-np.arctan(1/max(c)*dados.loc[i,'velocidade']/omega))

print(f'''
O valor mínimo de C deve ser {max(c)} mm
O valor de a + b deve ser {ab} mm
''')


