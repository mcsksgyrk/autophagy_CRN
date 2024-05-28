import pandas as pd
import numpy as np
import jinja2

"""
Excelből beolvassa egyenleteket és paramétereket egy dataframe-be,
majd parsolja egyenleteket (unique species megkeresi),
egyenletek paraméterek és species-ek jina .inp-ba pakolja
"""


def getSpecies(df):
    df[0] = df[0].str.replace(' ', '')
    df[0] = df[0].str.replace(':', '_')
    ss = df[0].str.split(r"[^a-zA-Z0-9\s]").explode().unique()
    species = np.array(ss[ss != ''], dtype=str)
    return species


df = pd.read_excel('../reactionsICs.xlsx', header=None)
species = getSpecies(df)
df[3] = df[3].fillna(df[1]/60)

reactions = df[0].to_numpy()
params = df[3].to_numpy()


tt = np.vstack((reactions, params)).T


file_loader = jinja2.FileSystemLoader('inputmintk')
env = jinja2.Environment(loader=file_loader)

template = env.get_template('mechanism.inp')

output = template.render(items=tt, species=species)

with open("test_run", "w") as f:
    f.write(output)

#species.tofile("species.txt",sep = '\n',format = '%s')
