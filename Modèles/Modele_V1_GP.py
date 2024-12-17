import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp

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
dm_electrolyseur = 400/86400 # [kg s-1] 
h_electrolyseur = Cp * T_electrolyseur # [J kg-1] 
# --------- Electrolyseur --------- #

dm_buffer = dm_electrolyseur # Initialisation du débit en sortie de buffer

t = np.linspace(0, 86400, 10000) # Vecteur temporel (en s)

# Sous fonction pour déclarer les équations différentielles
def modele_V1(t, y, dm1, h1, dm2, h2):   
    
    M_buffer, U_buffer, P_buffer, M_stockage, U_stockage, P_stockage = y 
        
    if P_stockage >= P_stockage_max: 
        dm2=0
    
    # Buffer
    dM_dt_buffer = dm1 - dm2
    dU_dt_buffer = dm1*h1 - dm2*h2
    dp_dt_buffer = (dm1-dm2)*h1*r/Cv/V_buffer
    
    # Stockage
    dM_dt_stockage = dm2
    dU_dt_stockage = dm2*h2
    dp_dt_stockage = dm2*h1*r/Cv/V_stockage
    
    return [dM_dt_buffer, dU_dt_buffer, dp_dt_buffer, dM_dt_stockage, dU_dt_stockage, dp_dt_stockage] 

# Evènements pour détecter/arrêter
def max_pressure_buffer(t, y, dm1, h1, dm2, h2):
    M_buffer, U_buffer, P_buffer, M_stockage, U_stockage, P_stockage = y
    return P_buffer - P_buffer_max

max_pressure_buffer.terminal = True 
max_pressure_buffer.direction = 0 

# Fonction pour résoudre les équations différentielles

y0 = [M_buffer_ini, U_buffer_ini, P_buffer_ini , M_stockage_ini, U_stockage_ini, P_stockage_ini]
args = (dm_electrolyseur,h_electrolyseur,dm_electrolyseur,h_electrolyseur)
sol = solve_ivp(modele_V1, [t[0],t[-1]], y0=y0, args=args, t_eval=t, events=max_pressure_buffer, dense_output=True)

T_buffer = (sol.y[1]/(sol.y[0]*Cv)) 
h_buffer = sol.y[0]*Cp*T_buffer 

pression_max = np.ones(len(sol.y[0]))
pression_max = pression_max*70

plt.figure(1) 
plt.plot(sol.t,sol.y[2]/1e5, label="Buffer (lim. " + str(round(P_buffer_max/1e5)) + " bar)")
plt.plot(sol.t,sol.y[5]/1e5, label="Stockage (lim. " + str(round(P_stockage_max/1e5)) + " bar)")
plt.plot(sol.t,pression_max,"r--")
plt.axvline(x=44700,color='r',linestyle="--")
plt.text(500,78,f"{max(sol.y[2]/1e5):.2f}"+" bar",color='r')
plt.xlabel("Temps (s)")
plt.ylabel("Pression (bar)")
plt.title("Pression P en bar dans le buffer et le stockage")
plt.xlim([0,max(sol.t)])
plt.legend()
plt.grid() 
