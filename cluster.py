import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
"""
Végig kell menni összes pr-en, hogy homeosztázisban melyik aktív és melyik nem. Annotált pr-eken brr:
IC-kből sample
"""

class Bounds:
    def __init__(self,upper,lower):
        self.upper=upper
        self.lower=lower

ics = pd.read_excel('./olderVers/reactionsICs.xlsx',sheet_name="Apoptosis",usecols="A:B",header=None)
species = pd.read_excel('./olderVers/reactionsICs.xlsx',sheet_name="species",header=None)[0].tolist()
species = [x.lower() for x in species]

pr_ics=dict()
for i,r in ics.iterrows():
    bounds=r[1]
    pr=str(r[0]).lower()
    if "-" in str(bounds):
        x=bounds.split("-")
        ub=float(x[0])
        lb=float(x[1])
    else:
        ub=float(bounds)*1.5
        lb=float(bounds)*0.5
    pr_ics[pr]=Bounds(ub,lb)

x=[]
y=[]
for d in pr_ics.values():
    x.append(np.log10(d.lower))
    y.append(np.log10(d.upper))
plt.scatter(x,y)
plt.show()

for k,v in pr_ics.items():
    if np.isnan(v.upper) or np.isnan(v.lower):
        print(k)

