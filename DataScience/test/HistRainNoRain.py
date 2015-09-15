from pandas import *
import matplotlib.pyplot as plt
import pandasql


data = pandas.read_csv("turnstile_weather_v2.csv")

rain_days_data = pandasql.sqldf("select * from data where rain=1".lower(), locals())
no_rain_days_data = pandasql.sqldf("select * from data where rain=0".lower(), locals())

print no_rain_days_data.describe()

print rain_days_data.describe()

plt.hist([rain_days_data.ENTRIESn_hourly,no_rain_days_data.ENTRIESn_hourly] ,stacked=True, fill=True,color=['crimson', 'burlywood' ],
                            label=['Rain', 'No rain' ],bins=20)
plt.title("The ridership on rainy and not rainy days")
plt.xlabel('ENTRIESn hourly')
plt.legend()
#plt.figure()



#print no_rain_days_data.describe() 

#plt.hist(no_rain_days_data.ENTRIESn_hourly,histtype='bar', stacked=True, fill=True)
#plt.title("The ridership on calm days")
#plt.xlabel('ENTRIESn_hourly')

plt.show()