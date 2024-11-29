#Código com as funções utilizadas no trabalho: posição, velocidade, aceleração do came

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
import pandas as pd

omega = 1

def repouso(d, beta, teta0):
    '''
    função que representa o repouso
    d: deslocamento que o seguidor está repousando
    beta: intervalo de ângulo que ele fica repousando
    teta0: ângulo que ele inicia o repouso
    '''
    pos = [d, d]
    x = [teta0, teta0 + beta]
    vel = [0,0]
    ace = [0,0]
    return(pos, vel, ace, x)

def harmonico(y0, d, beta, teta0, omega, n):    

    '''
    função que representa o movimento uniforme para o came
    ângulos devem ser dados em graus
    y0: deslocamento inicial do estágio
    d: deslocamento (mm)
    beta: intervalo de ângulo do movimento
    teta0: ângulo inicial 
    omega: rotações por segundo 
    n: número de pontos para plot
    '''
    delta = beta / n
    pos = []
    vel = []
    ace = []
    x = []

    for i in range(0,n+1):
        y = d / 2 * (1 - np.cos(np.pi * np.deg2rad(delta*i) / np.deg2rad(beta)))  
        y_dot = np.pi * d * (omega * 2 * np.pi) / (2 * np.deg2rad(beta)) * np.sin(np.pi * np.deg2rad(delta*i) / np.deg2rad(beta))
        y_dot2 = d / 2 * (np.pi * (omega * 2 * np.pi) / np.deg2rad(beta)) ** 2 * np.cos(np.pi * np.deg2rad(delta*i) / np.deg2rad(beta))
        pos.append(y0 + y)
        vel.append(y_dot)
        ace.append(y_dot2)
        x.append(teta0+ delta*i)
    return pos, vel, ace, x

a = repouso(0,90,0)
b = harmonico(0,20,80,90,omega,100)
c = repouso(20,30,170)
d = harmonico(20,-10,30,200,omega,100)
e = repouso(10,90,230)
f = harmonico(10,-10,40,320,omega,100)

posicao = a[0] + b[0] + c[0] + d[0] + e[0] + f[0]
velocidade = a[1] + b[1] + c[1] + d[1] + e[1] + f[1]
aceleracao = a[2] + b[2] + c[2] + d[2] + e[2] + f[2]
teta = a[3] + b[3] + c[3] + d[3] + e[3] + f[3]

plt.figure(figsize=(12, 8))

# Gráfico 1:
plt.subplot(3, 1, 1)  
plt.plot(teta, posicao, marker='', color='blue')
plt.xlabel('θ (graus)')
plt.ylabel('y (mm)')
plt.title('Gráfico 1: θ x y')
plt.grid()
plt.legend()
plt.xlim(0,360) 
plt.ylim(0,20)
plt.xticks([0,90,170,200,230,320,360], ['0°','90°','170°','200°','230°','320°','360°'])
plt.axvline(x=90, color='black', linestyle=':')
plt.axvline(x=170, color='black', linestyle=':')
plt.axvline(x=200, color='black', linestyle=':')
plt.axvline(x=230, color='black', linestyle=':')
plt.axvline(x=320, color='black', linestyle=':')

# Gráfico 2: 
plt.subplot(3, 1, 2)  
plt.plot(teta, velocidade, marker='', color='green')
plt.xlabel('θ (graus)')
plt.ylabel('Velocidade (mm/s)')
plt.title('Gráfico 2: θ x v')
plt.grid()
plt.legend()
plt.xlim(0,360) 
plt.xticks([0,90,170,200,230,320,360], ['0°','90°','170°','200°','230°','320°','360°'])
plt.axvline(x=90, color='black', linestyle=':')
plt.axvline(x=170, color='black', linestyle=':')
plt.axvline(x=200, color='black', linestyle=':')
plt.axvline(x=230, color='black', linestyle=':')
plt.axvline(x=320, color='black', linestyle=':')

# Gráfico 3:
plt.subplot(3, 1, 3)  
plt.plot(teta, aceleracao, marker='', color='red')
plt.xlabel('θ (graus)')
plt.ylabel('Aceleração (mm/s²)')
plt.title('Gráfico 3: θ x a')
plt.grid()
plt.legend()
plt.xlim(0,360) 
plt.xticks([0,90,170,200,230,320,360], ['0°','90°','170°','200°','230°','320°','360°'])
plt.axvline(x=90, color='black', linestyle=':')
plt.axvline(x=170, color='black', linestyle=':')
plt.axvline(x=200, color='black', linestyle=':')
plt.axvline(x=230, color='black', linestyle=':')
plt.axvline(x=320, color='black', linestyle=':')

plt.tight_layout()
plt.show()

#df = pd.DataFrame({'posicao': posicao, 'velocidade': velocidade, 'aceleracao': aceleracao, 'teta': teta})
#df.to_csv('dados.csv')
