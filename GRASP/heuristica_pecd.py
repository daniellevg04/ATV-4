import math
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.spatial import ConvexHull
from scipy.spatial.qhull import QhullError

# Definir los círculos desiguales (tamaño y cantidad)
# circulos = [{"radio": radio} for radio in range(1, 8)]  # Radios del 1 al 7

circulos = [{'radio': i+1} for i in range(10) for j in range(10)]
print(circulos)

# Función para resolver el problema

def resolver_problema(circulos):
    circulos.sort(key=lambda x: -x["radio"])  # Ordenar círculos de mayor a menor radio
    posiciones = [{"x": 0, "y": 0, "radio": circulos[0]["radio"]}]

    element=0
    cambiorg = 0
    for i in range(1, len(circulos)):
        # colocado = False
        # temp_origem = None
        if cambiorg == 0:
            element = 0
        else:
            element = element
            cambiorg = 0

        if i % 2 == 0:

            angulo = 0
            poslist = 0

            while angulo < 360:
                # if angulo > 360:
                #     angulo = 
                angulo_rad = math.radians(angulo)
                x = posiciones[element]["x"] + (posiciones[element]["radio"] + circulos[i]["radio"]) * math.cos(angulo_rad)
                y = posiciones[element]["y"] + (posiciones[element]["radio"] + circulos[i]["radio"]) * math.sin(angulo_rad)
                
                permitido = True
                
                for j in range(len(posiciones)):
                    distancia_centros = math.sqrt((x - posiciones[j]["x"])**2 + (y - posiciones[j]["y"])**2)
                    if distancia_centros < circulos[i]["radio"] + posiciones[j]["radio"]:
                        permitido = False
                        break     

                if permitido:
                    posiciones.append({"x": x, "y": y, "radio": circulos[i]["radio"]})
                    
                    break 
                
                if not permitido and angulo == 360-1: 

                    if len(posiciones) <= len(circulos):
                        cambiorg = 1
                        angulo = 0  
                        lista_temp = []
                        for j in range(1, len(posiciones)):
                            dist = math.sqrt((posiciones[j]["x"] - posiciones[0]["x"])**2 + (posiciones[j]["y"] - posiciones[0]["y"])**2)
                            lista_temp.append([j,dist])
                        lista_temp = sorted(lista_temp, key=lambda x: x[1])

                        element = lista_temp[poslist][0]
                        poslist += 1

                        print (element, angulo)
                    else:
                        angulo = 400
                else: 
                    angulo +=1

                # angulo +=1
            
            print(i+1,"- ", angulo)
        else:

            angulo = 360
            poslist = 0

            while angulo > 0:

                angulo_rad = math.radians(angulo)
                x = posiciones[element]["x"] + (posiciones[element]["radio"] + circulos[i]["radio"]) * math.cos(angulo_rad)
                y = posiciones[element]["y"] + (posiciones[element]["radio"] + circulos[i]["radio"]) * math.sin(angulo_rad)
                
                permitido = True
                
                for j in range(len(posiciones)):
                    distancia_centros = math.sqrt((x - posiciones[j]["x"])**2 + (y - posiciones[j]["y"])**2)
                    if distancia_centros < circulos[i]["radio"] + posiciones[j]["radio"]:
                        permitido = False
                        break     

                if permitido:
                    posiciones.append({"x": x, "y": y, "radio": circulos[i]["radio"]})
                    
                    break 
                
                if not permitido and angulo == 1: 

                    if len(posiciones) <= len(circulos):
                        cambiorg = 1
                        angulo = 360  
                        lista_temp = []
                        for j in range(1, len(posiciones)):
                            dist = math.sqrt((posiciones[j]["x"] - posiciones[0]["x"])**2 + (posiciones[j]["y"] - posiciones[0]["y"])**2)
                            lista_temp.append([j,dist])
                        lista_temp = sorted(lista_temp, key=lambda x: x[1])

                        element = lista_temp[poslist][0]
                        poslist += 1

                        print (element, angulo)
                    else:
                        angulo = -1
                else: 
                    angulo -=1

                # angulo +=1
            print(i+1,"- ", angulo)

    return posiciones

# Iniciar el cronómetro
start_time = time.time()

# Llamar a la función para resolver el problema
posiciones_circulos = resolver_problema(circulos)

# Detener el cronómetro
end_time = time.time()

# Calcular el tiempo de ejecución
execution_time = end_time - start_time
print("Tiempo de ejecución:", execution_time, "segundos")

#INICIO para calcular nuevo centro y el radio de la circunferencia mayor 
circulos = np.zeros((len(posiciones_circulos),3))
for i,val in enumerate(posiciones_circulos):
    circulos[i,0] = val['x']
    circulos[i,1] = val['y']
    circulos[i,2] = val['radio']

try:
    # Calcular el círculo mínimo envolvente
    centro = [0,0]
    r_maior = 1000000000000
    for i in range(len(posiciones_circulos)):
        for j in range(len(posiciones_circulos)):
        
            text = 'C'+str(i)+'QG'+str(j)
            hull = ConvexHull(circulos[:, :2], qhull_options=text)
            cent_tem = hull.points[hull.vertices].mean(axis=0)
            raio_tem = np.max(np.linalg.norm(circulos[:, :2] - cent_tem, axis=1) + circulos[:, 2])

            # print(i, text, raio_tem)
            if raio_tem < r_maior:
                r_maior = raio_tem
                centro = cent_tem
except QhullError:
    if r_maior == 1000000000000:
        centro = [0,0]
        r_maior = 0

posiciones_circulos.append({'x': centro[0],'y': centro[1],'radio': r_maior})
# FIN para calcular nuevo centro y el radio de la circunferencia mayor 

print('el radio es: ', r_maior)
# Visualizar la solución con la nueva capa de círculos
fig, ax = plt.subplots()

# Dibujar los círculos en el contenedor y agregar etiquetas numéricas
for i, circulo in enumerate(posiciones_circulos):
    circulo_dibujo = plt.Circle((circulo["x"], circulo["y"]), circulo["radio"], fill=False, color='r', lw=2)
    ax.add_patch(circulo_dibujo)
    ax.annotate(str(i + 1), (circulo["x"], circulo["y"]), color='b', fontsize=12, ha='center', va='center')

ax.set_aspect('equal')
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.gca().set_aspect('equal', adjustable='box')

plt.show()
