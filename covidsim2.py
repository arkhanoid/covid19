import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import fsolve

end_time = 2.5*365
start_vax = 350
start_vax_cr = end_time# 600


def covid( v, t):

    [s,i,r] = v

    #constantes 
    a = 1/14.0   # recuperacao 
    b = 2.2/14   # taxa infeccao
    g = 1/150    # taxa de perda de imunidade
    d = 1/200.0 if t > start_vax else 0 # taxa de vacinacao 
    e = 0.012    # renovacao da populacao
    f = 0.3     if t > start_vax_cr else  0 # fracao de criancas vacinadas    
    
    #equacoes 
    dsdt = -b*i*s + g*r + e*(1-f) - d*s - e*s
    didt =  b*i*s - a*i - e*i
    drdt =  a*i + d*s +e*f -e*r - g*r 

    return [dsdt, didt, drdt]

def covid2( v, t):

    [s,i,r] = v

    #constantes 
    a = 1/14.0   # recuperacao 
    b = 2.2/14   # taxa infeccao
    g = 1/150    # taxa de perda de imunidade
    d = 0#1/365.0 if t > start_vax else 0 # taxa de vacinacao 
    e = 0.012    # renovacao da populacao
    
    #equacoes 
    dsdt = -b*i*s + g*r + e - d*s - e*s
    didt =  b*i*s - a*i - e*i
    drdt =  a*i + d*s - e*r - g*r 

    return [dsdt, didt, drdt]


h0 = [1, 1e-6, 0]

def covid_it(h):
    return covid(h, end_time)

def covid2_it(h):
    return covid2(h, end_time)


yf = fsolve(covid_it, [0.33, 0.33, 0.34])

yf2 = fsolve(covid2_it, [0.33, 0.33, 0.34])

np.set_printoptions(precision = 3, suppress = True)

print "Susceptiveis Infectados Imunes\nSem Vax: %s\nCom Vax: %s\n" %  (  yf, yf2 )

t = np.linspace(0, end_time,100000)

y = odeint(covid, h0, t)


y2 = odeint(covid2, h0, t)


plt.plot(t, y[:,0], 'g-')
plt.plot(t, y[:,1], 'r-')
plt.plot(t, y[:,2], 'b-')

plt.plot(t, y2[:,0], 'g--')
plt.plot(t, y2[:,1], 'r--')
plt.plot(t, y2[:,2], 'b--')

plt.vlines(start_vax, 0, 1, 'k', 'dotted')
plt.vlines(start_vax_cr, 0, 1, 'b', 'dotted')
#plt.plot(y[:,0], y[:,1], 'g')
plt.legend(['Susc', 'Infec', 'Imune','Susc c/ Vax','Infec c/ Vax','Imune c/ Vax', 'Inicio Vax', 'Vax criancas'])
plt.show()

   
