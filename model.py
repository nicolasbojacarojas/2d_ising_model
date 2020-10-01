
import numpy as np
import matplotlib.pyplot as plt

#crear el sistema de espines
def sistema(x):
#generación de números aleatorios en una matriz cuadrada 0 y -1
    red = np.random.randint(-1,1,(x,x))
    #los espacios en la red con valor 0 se cambian a 1
    red[red==0]=1
    return red
    
#funcion que mide la magnetizacion presente en la red
def med_magnetizacion(red):
    m=np.sum(red)
    return m

#funcion que calcula la energia del sistema sin el efecto del campo magnetico
def energia(red):
    e=0
    for i in range(len(red)):
        for j in range(len(red)):
            e += -red[i,j]*(red[fronteras(i-1),j] + red[fronteras(i+1),j]) + red[i,fronteras(j+1)] + red[i,fronteras(j-1)]
    return e

#condiciones de frontera, se aplican las condiciones de manera vertical y horizontal en la red de forma independiente
def fronteras(p):
    if p > x-1:
        return 0
    if p < 0:
        return x-1
    else:
        return p

def cambioespin(red,beta):
    for i in range(x):
        for j in range(x):
        #Se toman valores aleatorios de a y b para invertir cualquier valor de espin en la red
            a = np.random.randint(0,x)
            b = np.random.randint(0,x)
            #se toma el valor de espin de la red
            spin_value = red[fronteras(a-1), b] + red[fronteras(a+1), b] + red[a, fronteras(b-1)] + red[a, fronteras(b+1)]
            #se invierten los espines de la red
            inversion = -red[a,b]
            #se reliza el calculo de la energia de la red
            energia = 2*red[a,b]*spin_value
            #se prueban las condiciones sugeridas en la tarea
            if energia < 0:
                red[a,b] = -red[a,b]
            elif np.exp(-beta*energia) > np.random.rand():
                red[a,b] = -red[a,b]
    return red

#tamaño de la red:
x=10
#distintos valores de tempertura
t_0=100
#valores de temperatura
t=np.linspace(1,4,t_0)
#creacion de la red
red = sistema(x)
#repeticiones a realizar para la estabilizacion de la energia
p_0 = 1000
#número de veces para evolucionar el estado:
p = 1000
#listas a guardar los valores de energia y magnetizacion para cada temperatura
e = np.ones(t_0)
m = np.ones(t_0)
#variables para realizar la primera grafica para la cual se estabilizan los valores de energia dada una temperatura
beta_0 = 0.4
red2 = sistema(x)
#funcionamiento de la simulacion sin evolucion en temperatura
#iteracion para la estabilizacion del sistema
e_lista_prueba = np.ones(p)

for j in range(p_0):
	cambioespin(red2,beta_0)
for j in range(p):
	cambioespin(red2,beta_0)
	e_lista_prueba[j] = energia(red2)
plt.plot(e_lista_prueba/(p_0*x*x))
plt.ylabel("energia")
plt.savefig("evolucion_energia")
plt.close()
	
#funcionamiento de la simulacion con la evolucion de temperatura
for i in range(t_0):
	#se toman los valores de beta, teniendo en cuenta que son inversos de la temperatura
	beta = 1./t[i]
	#variables a guardar los valores de energia y magnetizacion de la evolucion del sistema dada una temperatura
	e_1 = 0
	m_1 = 0
	#evolucion del estado hasta estabilizarse
	for j in range(p_0):
		cambioespin(red,beta)
	#evolucion del estado una vez se encuentra estable
	for j in range(p):
		cambioespin(red,beta)
		e_0 = energia(red)
		m_0 = med_magnetizacion(red)
		e_1 += e_0
		m_1 += m_0
	e[i] = e_1/(p*x*x)
	m[i] = m_1/(p*x*x)
#realizacion de la grafica pedida para la magnetizacion
plt.scatter(t,m)
plt.xlabel("temperatura")
plt.ylabel("magnetizacion")
plt.savefig("grafica_magnetizacion_temperatura")
plt.close()
#se anexa una grafica de la evolucion de la energia con la temperatura
plt.plot(t,e)
plt.xlabel("temperatura")
plt.ylabel("energia")
plt.savefig("grafica_energia_temperatura")
