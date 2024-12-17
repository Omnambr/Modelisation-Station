import numpy as np 
import matplotlib.pyplot as plt 
from scipy.integrate import solve_ivp 
from CoolProp.CoolProp import PropsSI

Gamma=1.4 
r=4157 # [J kg−1 K−1] 
Cp=r*Gamma/(Gamma-1) # [J kg−1 K−1] 
Cv=Cp/Gamma # [J kg−1 K−1] 

V_buffer = 3 # [m3] 
P_buffer_ini = 1e5 # [Pa] 
P_buffer_max = 70e5 
T_buffer_ini = 273.15 # [K] 
U_ini = P_buffer_ini*V_buffer*Cv/r 

T_electrolyseur = 273.15+60 # [K] 
m1 = 400/86400 # [kg s-1] 
h1 = Cp * T_electrolyseur # [J kg-1] 

t = np.linspace(0, 86400, 10000)
i = 0

def buffer(t,y, m1, h1):    
    m, U, P = y
    dm_dt = m1 
    dU_dt = m1*h1 
    dp_dt = (m1/V_buffer)*r*(m1*h1)/(m1*Cv)
    return [dm_dt,dU_dt,dp_dt] 

def max_pressure(t, y, m1, h1): 
    m, U, P = y
    return P - P_buffer_max 

max_pressure.terminal = True 
max_pressure.direction = 0 

sol = solve_ivp(buffer, [t[0],t[-1]], [P_buffer_ini*V_buffer/(r*T_buffer_ini),U_ini,P_buffer_ini], args=(m1,h1), t_eval=t, events=max_pressure, dense_output=True) 

T_buffer = (sol.y[1]/(sol.y[0]*Cv)) 
h_buffer = sol.y[0]*Cp*T_buffer 

P_test2 = PropsSI('P', 'U', sol.y[1]/sol.y[0], 'D', sol.y[0]/V_buffer, 'H2')

print(P_test2)

plt.figure(1) 
plt.plot(sol.t,sol.y[0]) 
plt.title("Masse M en kg dans le réservoir en fonction du temps") 
plt.xlabel("Temps (s)") 
plt.ylabel("Masse (kg)") 
plt.grid() 

plt.figure(2) 
plt.plot(sol.t,T_buffer-273.15) 
plt.title("Température T en °C dans le réservoir en fonction du temps") 
plt.xlabel("Temps (s)") 
plt.ylabel("Température (°C)") 
plt.grid() 

plt.figure(3) 
plt.plot(sol.t,sol.y[2]/1e5) 
plt.title("Pression P en bar dans le réservoir en fonction du temps") 
plt.xlabel("Temps (s)") 
plt.ylabel("Presson (bar)") 
plt.grid() 

plt.figure(4) 
plt.plot(sol.t,P_test2/1e5, label='Gaz réel')
plt.plot(sol.t,sol.y[2]/1e5,label='P solve_ivp')
plt.title("Pression P en bar dans le réservoir en fonction du temps") 
plt.xlabel("Temps (s)") 
plt.ylabel("Presson (bar)")
plt.legend()
plt.grid() 


plt.show()
