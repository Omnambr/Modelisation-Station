import numpy as np 
import matplotlib.pyplot as plt 
from CoolProp.CoolProp import PropsSI

Gamma=1.4 
r=4157 # [J kg−1 K−1] 
Cp=r*Gamma/(Gamma-1) # [J kg−1 K−1] 
Cv=Cp/Gamma # [J kg−1 K−1] 

# --------- Buffer --------- #
V_buffer = 10 # [m3] 
P_buffer_ini = 1e5 # [Pa] 
P_buffer_max = 70e5 
T_buffer_ini = 273.15 # [K] 
U_buffer_ini = P_buffer_ini*V_buffer*Cv/r
M_buffer_ini = P_buffer_ini*V_buffer/(r*T_buffer_ini)
# --------- Buffer --------- #

# --------- Stockage --------- #
V_stockage = 3 # [m3] 
P_stockage_ini = 1e5 # [Pa] 
P_stockage_max = 400e5 
T_stockage_ini = 273.15 # [K] 
U_stockage_ini = P_stockage_ini*V_stockage*Cv/r 
M_stockage_ini = P_stockage_ini*V_stockage/(r*T_stockage_ini)
# --------- Stockage --------- #

# --------- Electrolyseur --------- #
T_electrolyseur = 273.15+60 # [K] 
dm1 = 400/86400 # [kg s-1] 
h1 = Cp * T_electrolyseur # [J kg-1] 
# --------- Electrolyseur --------- #

dm2 = dm1 # Initialisation du débit en sortie de buffer
h2 = h1 # Initialisation du e l'enthalpie en sortie de buffer

dt = 10
T = 18000
N = round(T/dt)
t = np.linspace(0, T, N)

m_buffer = np.zeros(N)
U_buffer = np.zeros(N)
P_buffer = np.zeros(N)
T_buffer = np.zeros(N)

m_stockage = np.zeros(N)
U_stockage = np.zeros(N)
P_stockage = np.zeros(N)
T_stockage = np.zeros(N)

m_buffer[0] = PropsSI('D', 'P', P_buffer_ini, 'T', T_buffer_ini, 'H2')*V_buffer
U_buffer[0] = PropsSI('U', 'P', 1e5, 'T', 273.15, 'H2')*m_buffer[0]
P_buffer[0] = P_buffer_ini
T_buffer[0] = T_buffer_ini

m_stockage[0] = PropsSI('D', 'P', P_stockage_ini, 'T', T_stockage_ini, 'H2')*V_stockage
U_stockage[0] = PropsSI('U', 'P', P_stockage_ini, 'T', T_stockage_ini, 'H2')*m_stockage[0]
P_stockage[0] = P_stockage_ini
T_stockage[0] = T_stockage_ini

# Itérations

for i in range(N-1):

    if P_stockage[i] >= P_stockage_max: 
        dm2=0

    if P_buffer[i] >= P_buffer_max: 
        break

    # -------- Buffer -------- #
    m_buffer[i+1] = m_buffer[i] + (dm1 - dm2)*dt
    U_buffer[i+1] = U_buffer[i] + (dm1*h1 - dm2*h2)*dt
    P_buffer[i+1] = PropsSI('P', 'U', U_buffer[i]/m_buffer[i], 'D', m_buffer[i]/V_buffer, 'H2')
    T_buffer[i+1] = PropsSI('T', 'P', P_buffer[i], 'D', m_buffer[i]/V_buffer, 'H2')
    # -------- Buffer -------- #

    # -------- Stockage -------- #
    m_stockage[i+1] = m_stockage[i] + dm2*dt
    U_stockage[i+1] = U_stockage[i] + dm2*h2*dt
    P_stockage[i+1] = PropsSI('P', 'U', U_stockage[i]/m_stockage[i], 'D', m_stockage[i]/V_stockage, 'H2')
    T_stockage[i+1] = PropsSI('T', 'P', P_stockage[i], 'D', m_stockage[i]/V_stockage, 'H2')
    # -------- Stockage -------- #    


# Fonction pour résoudre les équations différentielles

plt.figure(1) 
plt.plot(t,P_buffer/1e5, label="Buffer (lim. " + str(round(P_buffer_max/1e5)) + " bar)")
plt.plot(t,P_stockage/1e5, label="Stockage (lim. " + str(round(P_stockage_max/1e5)) + " bar)")
plt.axhline(P_buffer_max/1e5,linestyle="--",color='r')
plt.axvline(x=44700,linestyle="--",color='r')
plt.text(500,78,f"{max(P_buffer/1e5):.2f}"+" bar",color='r')
plt.xlabel("Temps (s)")
plt.ylabel("Pression (bar)")
plt.title("Pression P en bar dans le buffer et le stockage")
plt.xlim([0,max(t)])
plt.legend()
plt.grid()

plt.show()
