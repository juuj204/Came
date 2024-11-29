#Código para realizar o plot da geometria do came de rolete

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import numpy as np
import scipy as sc
import pandas as pd

dados = pd.read_csv('dados.csv') 

r_base = 45                         #Raio do círculo base (mm)
r_principal = 50                    #Raio do círculo primitivo (mm)   
r_rolete = r_principal - r_base     #Raio do rolete (mm)

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

x0 = []         #Pontos em x do came
y0 = []         #Pontos em y do came
angulos = []    #Angulos para cada ponto

#Repouso de 0 a 90
for i in range(0,90):
    x = r_base * np.cos(np.deg2rad(i))
    y = r_base * np.sin(np.deg2rad(i))
    x0.append(x)
    y0.append(y)
    angulos.append(i)

#Subida de 90 a 170
for i in range(len(dados)):
    if dados.loc[i,'teta'] >= 90 and dados.loc[i,'teta'] <= 170:
        x = (r_base + dados.loc[i,'posicao']) * np.cos(np.deg2rad(dados.loc[i,'teta']))
        y = (r_base + dados.loc[i,'posicao']) * np.sin(np.deg2rad(dados.loc[i,'teta']))
        x0.append(x)
        y0.append(y)
        angulos.append(dados.loc[i,'teta'])

#Repouso de 170 a 200
for i in range(170,200):
    x = (r_base + 20) * np.cos(np.deg2rad(i))
    y = (r_base + 20) * np.sin(np.deg2rad(i))
    x0.append(x)
    y0.append(y)
    angulos.append(i)

#Descida de 200 a 230
for i in range(len(dados)):
    if dados.loc[i,'teta'] >= 200 and dados.loc[i,'teta'] <= 230:
        x = (r_base + dados.loc[i,'posicao']) * np.cos(np.deg2rad(dados.loc[i,'teta']))
        y = (r_base + dados.loc[i,'posicao']) * np.sin(np.deg2rad(dados.loc[i,'teta']))
        x0.append(x)
        y0.append(y)
        angulos.append(dados.loc[i,'teta'])

#Repouso de 230 a 320
for i in range(230,320):
    x = (r_base + 10) * np.cos(np.deg2rad(i))
    y = (r_base + 10) * np.sin(np.deg2rad(i))
    x0.append(x)
    y0.append(y)
    angulos.append(i)

#Descida de 320 a 360
for i in range(len(dados)):
    if dados.loc[i,'teta'] >= 320 and dados.loc[i,'teta'] <= 360:
        x = (r_base + dados.loc[i,'posicao']) * np.cos(np.deg2rad(dados.loc[i,'teta']))
        y = (r_base + dados.loc[i,'posicao']) * np.sin(np.deg2rad(dados.loc[i,'teta']))
        x0.append(x)
        y0.append(y)
        angulos.append(dados.loc[i,'teta'])

came = pd.DataFrame({'x': x0,'y': y0,'teta': angulos})

#------------------------------------------------------------------------------------------#
# Curva do rolete
#------------------------------------------------------------------------------------------#

x_prim = []         #Pontos em x da curva primitiva
y_prim = []         #Pontos em y da curva primitiva

for i in range(len(came)):
    r_came = (came.loc[i,'x'] ** 2 + came.loc[i,'y'] ** 2) ** (1/2)
    x = (r_came + r_rolete) * np.cos(np.deg2rad(came.loc[i,'teta']))
    y = (r_came + r_rolete) * np.sin(np.deg2rad(came.loc[i,'teta']))
    x_prim.append(x)
    y_prim.append(y)

curva_primitiva = pd.DataFrame({'x': x_prim, 'y': y_prim, 'teta': came['teta']})
    
#------------------------------------------------------------------------------------------#
# Plotando os gráficos
#------------------------------------------------------------------------------------------#

c_base = circulo(r_base,0,0)
c_principal = circulo(r_principal,0,0)

xrol = curva_primitiva['x']
yrol = curva_primitiva['y']

fig, ax = plt.subplots()

ax.plot(c_base['x'], c_base['y'], linestyle='dotted', color='black', label='Círculo de Base')
ax.plot(c_principal['x'], c_principal['y'], linestyle='dotted', color='blue', label='Círculo Principal')
ax.plot(came['x'], came['y'], color='red', label='Came')
ax.plot(curva_primitiva['x'], curva_primitiva['y'], linestyle='--', color='green', label='Curva Primitiva')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Came Com Seguidor de Rolete')
ax.legend(loc=1, handlelength=2, labelcolor='black', frameon=False, draggable=True)
ax.set_aspect('equal', adjustable='box')
plt.axhline(0, color='black', linewidth=1, label='Eixo X')  
plt.axvline(0, color='black', linewidth=1, label='Eixo Y') 
#ticks = np.arange(-r_base*2, r_base*2, r_base/5)  
#plt.xticks(ticks)  
#plt.yticks(ticks)    

moving_point, = ax.plot([], [], 'ro')

c_rolete = Circle((0, 0), r_rolete, color='green', fill=False)
ax.add_patch(c_rolete)

def update(frame):
    xpos = curva_primitiva['x'].iloc[frame]  
    ypos = curva_primitiva['y'].iloc[frame]  
    c_rolete.set_center((xpos, ypos))
    return c_rolete, 

ani = FuncAnimation(fig, update, frames=len(curva_primitiva), interval=50)

plt.show()
