import CoolProp.CoolProp as CP
import matplotlib.pyplot as plt
import numpy as np
import math

DN = {"DN20": 21.6,             #Nominal diameters, mm
      "DN32": 35.9,
      "DN40": 41.8,
      "DN50": 53.0,
      "DN65": 68.8,
      "DN80": 80.8,
      "DN100": 105.3}

def dp(d_in, T, p, u, fluid): #(internal diameter, temperature, pressure, velocity, fluid)
      D_h = d_in / 1000 #hydraulic diameter, m
      ro = CP.PropsSI("D", "T", T, "P", p*10**5, fluid) #density, kg/m3
      visc_kin = CP.PropsSI("VISCOSITY", "T", T, "P", p*10**5, fluid) / ro #kinematic viscosity, m2/s
      Re = D_h * u / visc_kin #Reynolds number, -
      if Re < 2300:
            lam = 64 / Re #friction factor, -
      else:
            lam1 = 0.01
            Convergence = False
            while Convergence == False:
                  lam = (1 / (2 * math.log10(Re * math.sqrt(lam1)) - 0.8))**2
                  error = abs(lam1 - lam) / lam
                  if error < 0.5:
                        Convergence = True
                  else:
                        lam1 = lam1 + 0.01
      dp = lam * 1/(d_in/1000) * u**2 / 2 * ro #pressure drops per 1m of pipe, Pa
      return(dp)

for i in np.arange(1, 2, 0.1):
      print(dp(21.6, 77, 18, i, "nitrogen"))
