import numpy as np
import pandas as pd


# We'll use scipy.optimize.curve_fit to do the nonlinear regression
import scipy.optimize

import matplotlib.pyplot as plt

df = pd.read_csv('historico.csv')

df.head()

# = df.rename(columns={ 'Dias':'t', 'casos':'n' })

t_0 = -10;

def model(t, t0, R):
    return np.exp(R * (t-t0) )  

def model2(t, R, r):
    return r * np.exp(R * (t-t_0) )  


p0 = np.array([-10, .25]) # t0 R iniciais

p, _ = scipy.optimize.curve_fit(model, df['Dias'], df['casos'], p0=p0)

p0 = np.array([.25, 0.3])


t_0 = p[0]

p2, _ = scipy.optimize.curve_fit(model2, df['Dias'], df['recuperados'],  p0=p0)



plt.yscale('log')

plt.plot(df['Dias'], df['casos'], marker='.', linestyle='none', label='casos informados')
plt.plot(df['Dias'], df['recuperados']+df['mortos'], marker='+', linestyle='none', label='recuperados e mortos')
plt.plot(df['Dias'], df['mortos'], marker='+', linestyle='none', label='mortos')



t_smooth = np.linspace(min(df['Dias']), max(df['Dias']), 100)

n_smooth = model(t_smooth, *tuple(p))

plt.plot(t_smooth, n_smooth, marker='None', linestyle='-', color='gray', label='progressao geometrica');


n2_smooth = model2(t_smooth, *tuple(p2))

#plt.plot(t_smooth, n2_smooth, marker='None', linestyle='-', label='ajuste prog geometrica recuperados');


plt.xlabel('dias')
plt.ylabel('n de casos')

plt.legend()
plt.show()

print p
print p2
