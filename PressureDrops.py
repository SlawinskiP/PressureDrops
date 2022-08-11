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

#for example, check results for: T=77K, p=18bar, nitrogen, k=0.05
T = float(input("Enter the temperature in K: "))
p = float(input("Enter te pressure in bar: "))
fluid = input("Enter the fluid: ")
k = float(input("Enter the absolute roughness of pipe: "))

def dp(d_in, T, p, u, k, fluid): #(internal diameter, temperature, pressure, velocity, fluid)
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
                  lam = (1 / (-2 * math.log10(2.5 / (Re * math.sqrt(lam1)) + k / (3.7 * d_in))))**2
                  error = abs(lam1 - lam) / lam
                  if error < 0.5:
                        Convergence = True
                  else:
                        lam1 = lam1 + 0.01
      dp = lam * 1/(d_in/1000) * u**2 / 2 * ro #pressure drops per 1m of pipe, Pa
      return(dp)

dp_DN20_list = []
dp_DN32_list = []
dp_DN40_list = []
dp_DN50_list = []
dp_DN65_list = []
dp_DN80_list = []
dp_DN100_list = []
u_list = np.arange(1, 2.1, 0.1) #recommended velocity in liquid line u=1-2m/s
for i in range(len(u_list)):
      u = u_list[i]
      dp_DN20 = dp(DN["DN20"], T, p, u, k, fluid)
      dp_DN32 = dp(DN["DN32"], T, p, u, k, fluid)
      dp_DN40 = dp(DN["DN40"], T, p, u, k, fluid)
      dp_DN50 = dp(DN["DN50"], T, p, u, k, fluid)
      dp_DN65 = dp(DN["DN65"], T, p, u, k, fluid)
      dp_DN80 = dp(DN["DN80"], T, p, u, k, fluid)
      dp_DN100 = dp(DN["DN100"], T, p, u, k, fluid)
      dp_DN20_list.append(dp_DN20)
      dp_DN32_list.append(dp_DN32)
      dp_DN40_list.append(dp_DN40)
      dp_DN50_list.append(dp_DN50)
      dp_DN65_list.append(dp_DN65)
      dp_DN80_list.append(dp_DN80)
      dp_DN100_list.append(dp_DN100)

plt.figure("Pressure drops per 1 meter of pipe in function of velociy.")
plt.plot(u_list, dp_DN20_list, label = "DN20")
plt.plot(u_list, dp_DN32_list, label = "DN32")
plt.plot(u_list, dp_DN40_list, label = "DN40")
plt.plot(u_list, dp_DN50_list, label = "DN50")
plt.plot(u_list, dp_DN65_list, label = "DN65")
plt.plot(u_list, dp_DN80_list, label = "DN80")
plt.plot(u_list, dp_DN100_list, label = "DN100")
plt.xlabel("Velocity, m/s")
plt.ylabel("Pressure drop per meter of pipe, Pa")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
