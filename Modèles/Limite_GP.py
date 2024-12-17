import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
from CoolProp.Plots import PropertyPlot

P = np.linspace(1e5, 1000e5, 1000)
T = np.linspace(273.15, 273.15+500, 1000)

rho_reel = np.zeros(len(T))
rho_gp = np.zeros(len(T))

P_test = 1

for i in range(len(T)):
    rho_reel[i] = PropsSI('D', 'T', 273.15, 'P', P[i], 'H2')
    rho_gp[i] = P[i]/4157/273.15

plt.figure(1)
plt.plot(P/1e5,rho_gp,label='Gaz Parfait')
plt.plot(P/1e5,rho_reel,label='Gaz Réel')
plt.title('Variation de la masse volumique (isotherme : 273.15 K)')
plt.ylabel('Masse volumique en kg.m$^3$')
plt.xlabel('Pression en bar')
plt.grid()
plt.legend()
plt.show()

plt.figure(2)
plt.plot(P/1e5,(abs(rho_reel-rho_gp)/rho_gp)*100)
plt.grid()
plt.show()

plot = PropertyPlot('H2', 'pt')
plot.calc_isolines()
plot.show()
