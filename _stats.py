from scipy import stats
import math
import pandas as pd
import os

df_heat = pd.DataFrame()
for param1 in [dir for dir in os.listdir('opinionData/') if os.path.isdir('opinionData/' + dir)]:
	print(param1)
	df = pd.DataFrame()
	for param2 in [dir for dir in os.listdir('opinionData/' + param1 + '/') if os.path.isdir('opinionData/' + param1 + '/' + dir)]:
		print(param2)
		df_param = pd.DataFrame()
		for run in [dir for dir in os.listdir('opinionData/' + param1 + '/' + param2) if os.path.isdir('opinionData/' + param1 + '/' + param2 + '/' + dir)]:
			df_run = pd.read_csv('opinionData/' + param1 + '/' + param2 + '/' + run + '/results.csv')
			
			df_run = df_run.iloc[len(df_run) - 1 : len(df_run)]
			df_run = df_run.mean(numeric_only=True).transpose()
			df_param = df_param.append(df_run, ignore_index=True)

		means = df_param.mean(numeric_only=True)
		stds = df_param.std(numeric_only=True)
		n = len(df_param)
		cl = stats.t.ppf(0.95, n - 1) * stds / math.sqrt(n)
		
		print(means.tolist(),stds.tolist())
		df_mean = pd.DataFrame(means).transpose()
		df_lcl = pd.DataFrame(means - cl).transpose().add_suffix('_lcl')
		df_ucl = pd.DataFrame(means + cl).transpose().add_suffix('_ucl')
		df_param = df_mean.join([df_lcl, df_ucl], how='outer')
		
		name2, val2 = param2.split('=')[0], float(param2.split('=')[1])
		df_param.insert(0, '[{0}]'.format(name2), val2)
		
		df = df.append(df_param, ignore_index=True)

	
	df = df.sort_values(by=['[' + name2 + ']'])
	name1, val1 = param1.split('=')[0], float(param1.split('=')[1])
	df.to_csv('opinionData/' + param1 + '/' + '{0}={1}.csv'.format(name1, val1), index=False)
	df.insert(0, '[' + name1 + ']', val1, True)
	df_heat = df_heat.append(df)

df_heat = df_heat.sort_values(by=['[' + name1 + ']', '[' + name2 + ']'])
df_heat.to_csv('opinionData/heatmap.csv', index=False)