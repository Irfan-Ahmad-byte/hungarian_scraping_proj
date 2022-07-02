import pandas as pd
import sys

excel = sys.argv[1]

name = ''.join(excel.split('.')[:-1])

excel = pd.read_excel(excel)

cols = excel.columns

data_dict = {}
for col in cols:
	data_dict[col]=excel[col]

df = pd.DataFrame(data_dict)

df.to_excel(f'{name}_data.xlsx', index=False)

print(f'file successfully saved as {name}_data.xlsx')
