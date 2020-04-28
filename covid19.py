import numpy as np
import scipy
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import pandas as pd
df = pd.read_csv('historico.csv')
df.head()
def proggeom(t, t0, R):
    return np.exp(R * (t-t0) )


pop = 211394901
i0 = 67446.0
p0 = np.array([-10.0, 1.0]) # t0 R iniciais
p, _ = scipy.optimize.curve_fit(proggeom, df['Dias'], df['casos'], p0=p0)

def model(y,t,a,b):
    dydt = -b * y * ( 1-y+ a*np.log(y)/b )
    return dydt

y0 = 1.0-i0/(pop*0.078) # fracao inicial 1 - n de casos / populacao * taxa notificacao

t = np.linspace(0, 200, 200);

# aproximacao da fase exponencial com dados totalizados:

# c = casos registrados
# dc/dt = -ds/dt = b*i*s0 = b*i
# dc = di + dr, dr/dt = a*i
# dc/dt = di/dt + a*i = b*i
# di/dt = (b-a)* i => i = i0*exp((b-a)* t)
# dc/dt = (b-a) * i + a * i = b*i0 * exo((b-a) * t)
# c = i0* b/(b-a)*( exp((b-a)* t) - 1) ~ C0 * exp((b-a)*t)
# R = b-a
# b = R + a
# dr/dt = i * a = a* i0 * exp( (b-a) * t )
# r = i0/(b-a) * ( exp((b-a) * t) -1 )
# c/r = b/a
# a = R/(c/r - 1)
# b = R + a
# usando dados de 17/04 (Johns Hopkins): pop*c = 33682, pop*r = 14026
# usando a media dos ultimos dias

#a = p[1] / ( 33682.0 / 16398 - 1 )
a = p[1] / 0.78595297588584 


b = p[1] + a


y1 = odeint(model, y0, t, args=(a,b,))
y2 = [ 1-y+a*np.log(y)/b for y in y1] 
y3 = [ 1 - y - (1-y+a*np.log(y)/b)  for y in y1]
y4 = [ a/b for y in y1]

i=0 
for y in y1: 
    i=i+1
    if y < a/b:
        break;

plt.plot(t, y1, 'r-', linewidth=2, label='susceptibles')
plt.plot(t, y2, 'g--', linewidth=2, label='infected')
plt.plot(t, y3, 'b--', linewidth=2, label='removed')
plt.plot(t, y4, 'r--', linewidth=1, label='A/B')

plt.xlabel('time')
plt.ylabel('fracao da populacao')
plt.legend()
#plt.yscale('log')
import re

def pts(v):
    return re.sub("(\d)(?=(\d{3})+(?!\d))", r"\1.", "%d" % v)

def letalidade():
#taxas de mortalidadde de covid19 por idadade na china
    death = [    0.0,   0.2,   0.2,   0.2,   0.4,   1.3,   3.6,   8.0, 14.8]
#             10-19, 20-29, 30-39, 40-49, 50-59, 60-69, 70-79, 80+
# piramide etaria do Brasil
    apm= [  7.0,  7.7,   8.1,   8.1,   6.7,   5.4,   3.5,   1.8, 0.7]
    apf= [  6.8,  7.3,   8.0,   8.2,   7.0,   5.9,   4.1,   2.2, 1.1]
    m = 0;
# media ponderada considerando que a mortalidade masculina eh 2/3 e a feminina 1/3
    for x in range(len(death)):  
        m = m + (2*apm[x] + apf[x]) * death[x] / (300 * 99.6);

    return m

from datetime import date, timedelta
print   "Populacao: %s\n"\
        "Max doentes: %s\n"\
        "Contrairao virus %s (%.2f%%)\n"\
        "Numero de mortos: %s\n"\
        "Pico da epidemia %s\n"\
        "Razao de reproducao (R0): %.3f\n"\
        "Tempo medio de recuperacao: %.2f" % (
                pts(pop),  
                pts(np.int(pop * (1-a/b+ a* np.log(a/b) / b) )), 
                pts(np.int (pop* y3.pop()[0] )), y3.pop()[0] * 100,
                pts(np.int (pop* y3.pop()[0] * letalidade())), 
                (date.today()+timedelta(i)).strftime('%d/%m/%Y')  , 
                b/a, 1/a) 

plt.show()

