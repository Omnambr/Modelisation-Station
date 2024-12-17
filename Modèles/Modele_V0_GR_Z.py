import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

Gamma = 1.4
r = 4157  # [J kg−1 K−1]
Cp = r*Gamma/(Gamma-1)  # [J kg−1 K−1]
Cv = Cp/Gamma  # [J kg−1 K−1]

V_buffer = 3  # [m3]
P_buffer_ini = 1e5  # [Pa]
P_buffer_max = 70e5
T_buffer_ini = 273.15  # [K]
U_ini = P_buffer_ini*V_buffer*Cv/r

T_electrolyseur = 273.15+60  # [K]
m1 = 400/86400  # [kg s-1]
h1 = Cp * T_electrolyseur  # [J kg-1]

dt = 0.1
T = 3600
N = round(T/dt)
t = np.linspace(0, T, N)

m_buffer = np.zeros(N)
U_buffer = np.zeros(N)
P_buffer = np.zeros(N)
P_buffer_GP = np.zeros(N)
T_buffer = np.zeros(N)
T_buffer_reel = np.zeros(N)

m_buffer[0] = PropsSI('D', 'P', P_buffer_ini, 'T', T_buffer_ini, 'H2')*V_buffer
U_buffer[0] = PropsSI('U', 'P', 1e5, 'T', 273.15, 'H2')*m_buffer[0]
P_buffer[0] = P_buffer_ini
P_buffer_GP[0] = P_buffer_ini
T_buffer[0] = T_buffer_ini
T_buffer_reel[0] = T_buffer_ini
temps = 0
t_max = 0
t_max_GP = 0

z = np.zeros(N)
z[0] = 1

P_buffer_z = np.zeros(N)
P_buffer_z[0] = P_buffer_ini

index = 0
index_GP = 0

for i in range(N-1):
    z[i+1] = P_buffer_GP[i]/1e5*(-1.12227785e-17*T_buffer[i]**5 + 3.91729068e-14*T_buffer[i]**4 - 0.0000000000544232804*T_buffer[i]**3 + 0.0000000382871094*T_buffer[i]**2 - 0.0000143071551*T_buffer[i]+0.00267469219) + \
        (-3.29566084e-18*T_buffer[i]**6 + 1.3274828e-14*T_buffer[i]**5 - 0.0000000000218937262*T_buffer[i]**4 +
         0.0000000189603233*T_buffer[i]**3 - 0.00000913254195*T_buffer[i]**2 + 0.00233668051*T_buffer[i]+0.751145766)
    m_buffer[i+1] = m_buffer[i] + m1*dt
    U_buffer[i+1] = U_buffer[i] + m1*h1*dt
    P_buffer[i+1] = PropsSI('P', 'U', U_buffer[i]/m_buffer[i], 'D', m_buffer[i]/V_buffer, 'H2')
    P_buffer_GP[i+1] = P_buffer_GP[i] + ((m1/V_buffer)*r*(m1*h1)/(m1*Cv))*dt
    P_buffer_z[i+1] = P_buffer_z[i] + (z[i]*m_buffer[i]*8.314*T_buffer[i]/2.016/V_buffer)*dt
    T_buffer[i+1] = (U_buffer[i]/(m_buffer[i]*Cv))
    T_buffer_reel[i+1] = PropsSI('T', 'P', P_buffer[i],
                                 'D', m_buffer[i]/V_buffer, 'H2')
    if P_buffer[i] <= P_buffer_max:
        t_max = temps
        index = i
    if P_buffer_GP[i] <= P_buffer_max:
        t_max_GP = temps
        index_GP = i
    temps = temps + dt

plt.figure(1)
plt.plot(t, m_buffer)
plt.title("Masse M en kg dans le réservoir en fonction du temps")
plt.xlabel("Temps (s)")
plt.ylabel("Masse (kg)")
plt.grid()

plt.figure(2)
plt.plot(t, T_buffer-273.15, label='Gaz Parfait')
plt.plot(t, T_buffer_reel-273.15, label='Gaz réel')
plt.axvline(t_max, ymin=0, ymax=(T_buffer_reel[index]-273.15)/(T_buffer_reel[-1]-200), linestyle='--', color='black')
plt.axvline(t_max_GP, ymin=0, ymax=(T_buffer[index_GP]-273.15)/(T_buffer_reel[-1]-200), linestyle='--', color='black')
plt.axhline(T_buffer[index_GP]-273.15, xmin=0, xmax = t_max_GP/t[-1], linestyle='--', color='black')
plt.axhline(T_buffer_reel[index]-273.15, xmin=0, xmax = t_max/t[-1], linestyle='--', color='black')
plt.text(1550, T_buffer[index_GP]-273.15+5, str(round(T_buffer[index_GP]-273.15)) + ' °C', color='black')
plt.text(1550, T_buffer_reel[index]-273.15+5, str(round(T_buffer_reel[index]-273.15)) + ' °C', color='black')
plt.title("Température T en °C dans le réservoir en fonction du temps")
plt.xlabel("Temps (s)")
plt.ylabel("Température (°C)")
plt.legend()
plt.xlim([0,t[-1]])
plt.ylim([0,T_buffer_reel[-1]-200])
plt.grid()
plt.savefig('Temperature.svg', format='svg', dpi=500)

plt.figure(3)
plt.plot(t, P_buffer/1e5, label='Gaz réel CoolProp')
plt.plot(t, P_buffer_GP/1e5, label='Gaz Parfait')
plt.plot(t, P_buffer_z/1e5, label='Gaz Parfait linéarisation')
plt.axhline(P_buffer_max/1e5, linestyle='--', color='r')
plt.axvline(t_max, ymin=0, ymax=0.36, linestyle='--', color='black')
plt.axvline(t_max_GP, ymin=0, ymax=0.36, linestyle='--', color='black')
plt.text(0, 73, str(P_buffer_max/1e5) + " bar", color='r')
plt.text(1600, 0, str(round(t[index])) + ' s', color='black')
plt.text(2400, 0, str(round(t[index_GP])) + ' s', color='black')
plt.title("Pression P en bar dans le réservoir en fonction du temps")
plt.xlabel("Temps (s)")
plt.ylabel("Pression (bar)")
plt.legend()
plt.grid()
plt.savefig('Pression.svg', format='svg', dpi=500)

plt.show()
