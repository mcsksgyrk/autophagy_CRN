import pandas as pd
import numpy as np
import jinja2
from parseICs import *


df = pd.read_excel('../reactionsICs_w_species.xlsx', header=None,
                   sheet_name='ics', usecols="A:B")
bounds = generateBounds(df)
species = getSpecies('../corrected.csv')

source_data = pd.read_csv('../dataXu/tun100nm.csv')
variables = source_data.columns
# ic-vel skálázza a datat
for x in range(0, 10):
    ics = generateICs(species, bounds)
    dataDf = source_data.copy()
    dataDf.time = source_data.time*60
    for v in variables:
        if v in ics.keys():
            if v == "caspasea":
                dataDf[v] = dataDf[v]*ics['caspase']
            else:
                dataDf[v] = dataDf[v]*ics[v]
    dataPoints = []
    for i, row in dataDf.iterrows():
        dataPoints.append(compileDataRow(variables, row.values))

    file_loader = jinja2.FileSystemLoader('../dataXu')

    env = jinja2.Environment(loader=file_loader)

    template = env.get_template('data_test1.xml')

    output = template.render(ics=ics, variables=variables[1:], dataPoints=dataPoints)

    save_path = './meas_data_files/test'
    with open(save_path+str(x)+'.xml',  "w") as f:
        f.write(output)
