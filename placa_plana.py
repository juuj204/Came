#Código para realizar o plot da geometria do came de face plana

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
import numpy as np
import scipy as sc
import pandas as pd

dados = pd.read_csv('dados.csv') 

omega = 1                               #Velocidade angular do came
r_base = 160                            #Raio do círculo base (C) obtido no programa calcs.py (mm)
a = 33                                  #Tamanho a da placa plana (mm)
b = 33                                  #Tamanho b da placa plana (mm)
ab = 66                                 #Tamanho de a + b obtido no programa calcs.py

if a+b != ab:
    print(f'''
          #------------------------------------------------------------#
          O valor de a + b é diferente de {ab}. Mude e tentei novamente.
          #------------------------------------------------------------#
          ''')
    exit()

def circulo(r,x0,y0):
    '''
    função para adquirir os pontos de um círculo
    r: raio do círculo base
    x0, y0: coordenadas do centro
    '''
    x_points = []
    y_points = []
    angulos = []
    r0 = []

    for i in range(0, 360):
        x = x0 + r * np.cos(np.deg2rad(i))
        y = y0 + r * np.sin(np.deg2rad(i))
        r0.append((x**2 + y**2)**(1/2))
        angulos.append(i)
        x_points.append(x)
        y_points.append(y)

    c_base = pd.DataFrame({'x': x_points, 'y': y_points, 'teta': angulos})
    return(c_base)


#------------------------------------------------------------------------------------------#
# Construção do Came
#------------------------------------------------------------------------------------------#

x0 = []         #Lista com os pontos em x
y0 = []         #Lista com os pontos em y
angulos = []    #Lista com os angulos 
tg = []         #Lista com a tangente de cada ângulo (velocidade y_dot do código movimento_seguidor.py)
d = []          #Deslocamento do seguidor (posicao do código movimento_seguidor)

#Repouso de 0 a 90
for i in range(0,90):
    x = r_base * np.cos(np.deg2rad(i))
    y = r_base * np.sin(np.deg2rad(i))
    d.append(0)
    x0.append(x)
    y0.append(y)
    tg.append(0)
    angulos.append(i)

#Subida de 90 a 170 
for i in range(len(dados)):
    if dados.loc[i,'teta'] >= 90 and dados.loc[i,'teta'] <= 170:
        x = (r_base + dados.loc[i,'posicao']) * np.cos(np.deg2rad(dados.loc[i,'teta']))
        y = (r_base + dados.loc[i,'posicao']) * np.sin(np.deg2rad(dados.loc[i,'teta']))
        d.append(dados.loc[i,'posicao'])
        x0.append(x)
        y0.append(y)
        tg.append(dados.loc[i,'velocidade'])
        angulos.append(dados.loc[i,'teta'])

#Repouso de 170 a 200
for i in range(170,200):
    x = (r_base + 20) * np.cos(np.deg2rad(i))
    y = (r_base + 20) * np.sin(np.deg2rad(i))
    d.append(20)
    x0.append(x)
    y0.append(y)
    tg.append(0)
    angulos.append(i)

#Descida de 200 a 230
for i in range(len(dados)):
    if dados.loc[i,'teta'] >= 200 and dados.loc[i,'teta'] <= 230:
        x = (r_base + dados.loc[i,'posicao']) * np.cos(np.deg2rad(dados.loc[i,'teta']))
        y = (r_base + dados.loc[i,'posicao']) * np.sin(np.deg2rad(dados.loc[i,'teta']))
        d.append(dados.loc[i,'posicao'])
        x0.append(x)
        y0.append(y)
        tg.append(dados.loc[i,'velocidade'])
        angulos.append(dados.loc[i,'teta'])

#Repouso de 230 a 320
for i in range(230,320):
    x = (r_base + 10) * np.cos(np.deg2rad(i))
    y = (r_base + 10) * np.sin(np.deg2rad(i))
    d.append(10)
    x0.append(x)
    y0.append(y)
    tg.append(0)
    angulos.append(i)

#Descida de 320 a 360
for i in range(len(dados)):
    if dados.loc[i,'teta'] >= 320 and dados.loc[i,'teta'] <= 360:
        x = (r_base + dados.loc[i,'posicao']) * np.cos(np.deg2rad(dados.loc[i,'teta']))
        y = (r_base + dados.loc[i,'posicao']) * np.sin(np.deg2rad(dados.loc[i,'teta']))
        d.append(dados.loc[i,'posicao'])
        x0.append(x)
        y0.append(y)
        tg.append(dados.loc[i,'velocidade'])
        angulos.append(dados.loc[i,'teta'])

came = pd.DataFrame({'x': x0,'y': y0,'teta': angulos, 'tg': tg, 'd': d})

#------------------------------------------------------------------------------------------#
# Placa plana
#------------------------------------------------------------------------------------------#

xPlaca = []
yPlaca = []

for i in range(len(came)):
    x = (r_base + came.loc[i,'d']) * np.cos(np.deg2rad(came.loc[i,'teta'])) - (came.loc[i,'tg']/(omega*2*np.pi)) * np.sin(np.deg2rad(came.loc[i,'teta'])) 
    y = (r_base + came.loc[i,'d']) * np.sin(np.deg2rad(came.loc[i,'teta'])) + (came.loc[i,'tg']/(omega*2*np.pi)) * np.cos(np.deg2rad(came.loc[i,'teta'])) 
    xPlaca.append(x)
    yPlaca.append(y)

curvaPlaca = pd.DataFrame({'x': xPlaca, 'y': yPlaca, 'teta': came['teta'], 'tg': came['tg'], 'd': came['d']})

print(curvaPlaca)
#------------------------------------------------------------------------------------------#
# Plotando os gráficos
#------------------------------------------------------------------------------------------#
x
c_base = circulo(r_base,0,0)
c_principal = c_base


fig, ax = plt.subplots()

ax.plot(c_base['x'], c_base['y'], linestyle='dotted', color='black', label='Círculo Base')
ax.plot(c_principal['x'], c_principal['y'], linestyle='dotted', color='blue', label='Círculo Principal')
ax.plot(came['x'], came['y'], color='red', label='Came')
ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_title('Coordenadas do came')
ax.legend()
ax.legend(loc=1, handlelength=2, labelcolor='black', frameon=False, draggable=True)
ax.set_aspect('equal', adjustable='box')
plt.axhline(0, color='black', linewidth=1, label='Eixo X')  
plt.axvline(0, color='black', linewidth=1, label='Eixo Y') 
#ticks = np.arange(-r_base*2, r_base*2, r_base/5)  
#plt.xticks(ticks)  
#plt.yticks(ticks)    

moving_point, = ax.plot([], [], 'ro')

placaA = Rectangle((r_base,0), -a, 5, color='green')
placaB = Rectangle((r_base,0), b, 5, color='green')
ax.add_patch(placaA)
ax.add_patch(placaB)

def update(frame):
    xpos = curvaPlaca['x'].iloc[frame]  
    ypos = curvaPlaca['y'].iloc[frame]  
    tg = (curvaPlaca['teta'] -90).iloc[frame]
    placaA.set_xy((xpos, ypos ))
    placaA.set_angle(tg)
    placaB.set_xy((xpos, ypos ))
    placaB.set_angle(tg)

    return placaB, placaA, 

ani = FuncAnimation(fig, update, frames=len(curvaPlaca), interval=50)

plt.show()
