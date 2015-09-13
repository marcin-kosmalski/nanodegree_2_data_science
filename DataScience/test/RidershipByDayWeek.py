from pandas import *
import matplotlib.pyplot as plt
import pandasql


data = pandas.read_csv("turnstile_weather_v2.csv")


ridership=pandasql.sqldf("select day_week,avg(ENTRIESn_hourly) as entriesn_hourly_per_day_week  from data group by day_week".lower(), locals())
print ridership

plt.plot(ridership['day_week'], ridership['entriesn_hourly_per_day_week'])

plt.title("Average value of ENTRIESn hourly per weekday")
plt.xlabel('A day of the week')
plt.ylabel('Average value of ENTRIESn hourly')

plt.show()