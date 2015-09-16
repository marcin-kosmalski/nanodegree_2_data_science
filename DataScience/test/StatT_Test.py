import numpy as np
import scipy
import scipy.stats
import pandas




data = pandas.read_csv("turnstile_weather_v2.csv")

rainyData=data[data['rain']==1]['ENTRIESn_hourly']
noRainyData=data[data['rain']==0]['ENTRIESn_hourly']
print rainyData.count()
print noRainyData.count()

#print rainyData.describe()
#print noRainyData.describe()


print scipy.stats.mannwhitneyu(noRainyData,rainyData)

print scipy.stats.ttest_ind(rainyData,noRainyData , equal_var = False)

