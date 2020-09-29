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
def med_magnetizacion(red,x):
    m=np.sum(red)
    return m/x**2

#funcion que calcula la energia del sistema sin el efecto del campo magnetico
def energia(red,x):
    e=0
    for i in range(x):
        for j in range(x):
            e += -1*red[i,j]*(red[fronteras(i-1),j] + red[fronteras(i+1),j]) + red[i,fronteras(j+1)] + red[i,fronteras(j-1)]
    return e/x**2

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
            energia = (inversion-red[a,b])*spin_value
            #se prueban las condiciones sugeridas en la tarea
            if energia <= 0:
                red[a,b] = -red[a,b]
            elif np.exp(-beta**energia) > np.random.rand():
                red[a,b] = -red[a,b]

#tamaño de la red:
x=15
#distintos valores de tempertura
t_0=40
#valores de temperatura
t=np.linspace(1,5,t_0)
#creacion de la red
red = sistema(x)
#repeticiones a realizar para la estabilizacion de la energia
p_0 = 1000
#número de veces para evolucionar el estado:
p = 1000
#listas a guardar los valores de energia y magnetizacion para cada temperatura
e = np.ones(t_0)
m = np.ones(t_0)

for i in range(t_0):
	beta = 1./t[i]
	e_1 = 0
	m_1 = 0
	for j in range(p_0):
		cambioespin(red,beta)
	for j in range(p):
		cambioespin(red,beta)
		e_0 = energia(red,x)
		m_0 = med_magnetizacion(red,x)
		e_1 += e_0
		m_1 += m_0
	e[i] = e_1/(p*x*x)
	m[i] = m_1/(p*x*x)
"""
for i in range(t_0):
    cambioespin(red,beta)
    m = med_magnetizacion(red,x)
    e = energia(red,x)
    e_bar += e
    e_pro_0[i] = e
    m_bar += m
    m_pro_0[i] = m
    
    

for i in range(t):
    cambioespin(red, beta)
    m = med_magnetizacion(red,x)
    e = energia(x,x)
    m_bar += m
    m_pro[i] = m"""
    

plt.plot(t,e)
