import pandas as pd
import numpy as np
"""
2 lépés
- intervallumok
- utána aktív inaktív formák ha vannak
- 2.nek összesen legyen annyi a koncija?
- hard force fixed ICs:
    - caspasea=0
    - AUT = amit kiszámoltam cikkből
"""


def sampleBounds(bounds):
    if bounds[1] == 0:
        return 0.0
    l, b = np.log(bounds)
    s = np.random.uniform(l, b)
    return np.exp(s)


def getSpecies(path):
    df_ = pd.read_csv(path)
    df_ = df_[~df_['reactions'].str.contains('REV')]
    ss = df_['reactions'].str.split(r"[^a-zA-Z0-9-_.\s]").explode().unique()
    species = np.array(ss[ss != ''], dtype=str)
    return species


def generateBounds(df):
    bounds = dict()
    for index, row in df.iterrows():
        val = row[1]
        lb = 0
        ub = 0
        if type(val) is str:
            aux = val.split("-")
            lb = float(aux[0])*10**(-12)
            ub = float(aux[1])*10**(-12)
        else:
            lb = float(val)*0.5*10**(-12)
            ub = float(val)*1.5*10**(-12)
        bounds[row[0]] = [lb, ub]
    return bounds


def generateICs(species, bounds):
    to_file = dict()
    for s in species:
        if s not in bounds.keys():
            to_file[s] = 0
            continue
    # listából kinézi, hogy van e IC-je
    for s in species:
        if s in bounds.keys():
            ic = sampleBounds(bounds[s])
            to_file[s] = ic
            if s+'a' in species:
                ic_a = bounds[s][1]-ic
                to_file[s+'a'] = ic_a
        # ezeknek a kezdeti értéke nem változik
        to_file['REF'] = 1.0
        # itt kérdés, hogy legyen e continuity a caspase és caspasea között
        to_file['caspasea'] = 0
        # ezt külön sample, mol/cm^3, autophagosome koncentráció/sejt,
        # excelben ref
        to_file['AUT'] = sampleBounds([2.78*10**(-22), 1.39*10**(-21)])
    return to_file


def compileDataRow(variables, dataPoints):
    meas = ""
    for v in variables:
        meas = meas+"<%s>" % v + "{:.4e}" + "</%s>" % v
    start = "<dataPoint>"
    close = "</dataPoint>"
    row = start+meas.format(*dataPoints)+close
    return row


#af = pd.read_csv('../dataXu/tun100nm.csv')
#variables = df.columns
#
#
#to_xml = []
#for index, row in df.iterrows():
#    to_xml.append(compileDataRow(variables, row.values))
#to_xml

#df = pd.read_excel('../reactionsICs_w_species.xlsx', header=None,
#                   sheet_name='ics', usecols="A:B")
#bounds = generateBounds(df)
#species = getSpecies('../corrected.csv')
#generateICs(species, bounds)
