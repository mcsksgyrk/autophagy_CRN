import pandas as pd
import jinja2
from parseICs import generateICs, compileDataRow, generateBounds, getSpecies
import concurrent.futures
import time
import os


def scaleData(source_data, variables, ics):
    dataDf = source_data.copy()
    dataDf.time = source_data.time*60
    for v in variables:
        if v in ics.keys():
            if v == "caspasea":
                dataDf[v] = dataDf[v]*ics['caspase']
            else:
                dataDf[v] = dataDf[v]*ics[v]
    return dataDf


def compileDataTable(ics, variables, source_data):
    variables = source_data.columns
    dataDf = scaleData(source_data, variables, ics)
    dataPoints = []
    for i, row in dataDf.iterrows():
        dataPoints.append(compileDataRow(variables, row.values))
    return dataPoints


def generateOutput(ics, variables, dataPoints):
    file_loader = jinja2.FileSystemLoader('../dataXu')
    env = jinja2.Environment(loader=file_loader)
    template = env.get_template('data_test1.xml')
    output = template.render(ics=ics, variables=variables,
                             dataPoints=dataPoints)
    return output


# Define the function to generate a file with given content
def generate_file(file_index, directory, species, bounds, source_data):
    ics = generateICs(species, bounds)
    variables = source_data.columns
    dataPoints = compileDataTable(ics, variables, source_data)
    output = generateOutput(ics, variables[1:], dataPoints)
    filename = os.path.join(directory, f'file_{file_index}.xml')
    with open(filename, 'w') as f:
        f.write(output)
    return filename


# Directory to save files
output_directory = 'output_files'

# Create the directory if it does not exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Parameters for file generation
df = pd.read_excel('../reactionsICs_w_species.xlsx', header=None,
                   sheet_name='ics', usecols="A:B")
bounds = generateBounds(df)
species = getSpecies('../corrected.csv')

source_data = pd.read_csv('../dataXu/tun100nm.csv')
variables = source_data.columns

start_index = 1
end_index = 10000
max_workers = 10
# Use ThreadPoolExecutor to parallelize file generation
start_time = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = [executor.submit(generate_file, file_index, output_directory, species, bounds, source_data) for file_index in range(start_index, end_index + 1)]

# Collect the results
generated_files = [future.result() for future in concurrent.futures.as_completed(futures)]
stop_time = time.time()
elapsed = stop_time - start_time
print(f"Generated {len(generated_files)} files in %s"% elapsed)
