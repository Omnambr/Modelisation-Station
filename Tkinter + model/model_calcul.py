import numpy as np
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI

def simulation(d_electrolyseur,T_electrolyseur,V_buffer,P_buffer_ini,P_buffer_max,T_buffer_ini,tau_comp,eta_comp,eta_meca,eta_elec,V_stockage,P_stockage_ini,P_stockage_max,T_stockage_ini):  
    
    Gamma=1.4 
    r=4157 # [J kg−1 K−1] 
    Cp=r*Gamma/(Gamma-1) # [J kg−1 K−1] 
    Cv=Cp/Gamma # [J kg−1 K−1] 
    
    # --------- Electrolyseur --------- #
    h1 = Cp * T_electrolyseur # [J kg-1] 
    # --------- Electrolyseur --------- #    
    
    # --------- Buffer --------- #
    U_buffer_ini = P_buffer_ini*V_buffer*Cv/r
    M_buffer_ini = P_buffer_ini*V_buffer/(r*T_buffer_ini)
    # --------- Buffer --------- #
    
    # --------- Stockage --------- #
    U_stockage_ini = P_stockage_ini*V_stockage*Cv/r 
    M_stockage_ini = P_stockage_ini*V_stockage/(r*T_stockage_ini)
    # --------- Stockage --------- #
    
    dm2 = d_electrolyseur # Initialisation du débit en sortie de buffer
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
    
    eta_comp = 10
    Puissance_comp = np.zeros(N)
    
    eta_comp = 0.85  # Rendement isentropique
    eta_meca = 0.79  # Rendement mécanique
    eta_elec = 0.95  # Rendement électrique
    
    # ------------------ Itérations ------------------ #
    
    for i in range(N-1):
    
        if P_stockage[i] >= P_stockage_max: 
            dm2=0
    
        if P_buffer[i] >= P_buffer_max: 
            break
    
        # -------- Buffer -------- #
        m_buffer[i+1] = m_buffer[i] + (d_electrolyseur - dm2)*dt
        U_buffer[i+1] = U_buffer[i] + (d_electrolyseur*h1 - dm2*h2)*dt
        P_buffer[i+1] = PropsSI('P', 'U', U_buffer[i]/m_buffer[i], 'D', m_buffer[i]/V_buffer, 'H2')
        T_buffer[i+1] = PropsSI('T', 'P', P_buffer[i], 'D', m_buffer[i]/V_buffer, 'H2')
        # -------- Buffer -------- #
    
        # -------- Compresseur -------- #
        Puissance_comp[i] = dm2*(PropsSI('H', 'P', P_stockage[i], 'T', T_stockage[i], 'H2')- PropsSI('H', 'P', P_buffer[i], 'T', T_buffer[i], 'H2'))/eta_comp/eta_elec/eta_meca
        # -------- Compresseur -------- #
    
        # -------- Stockage -------- #
        m_stockage[i+1] = m_stockage[i] + dm2*dt
        U_stockage[i+1] = U_stockage[i] + dm2*h2*dt
        P_stockage[i+1] = PropsSI('P', 'U', U_stockage[i]/m_stockage[i], 'D', m_stockage[i]/V_stockage, 'H2')
        T_stockage[i+1] = PropsSI('T', 'P', P_stockage[i], 'D', m_stockage[i]/V_stockage, 'H2')
        # -------- Stockage -------- #    
        
    # ------------------ Itérations ------------------ #
        
    return t, P_buffer, P_stockage, Puissance_comp
        
