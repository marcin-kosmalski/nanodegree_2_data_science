
import numpy as np
from pandas import *
import matplotlib.pyplot as plt
import pandasql
from sklearn.linear_model import SGDRegressor
import math
from scipy import stats



def normalize_features(features):
    ''' 
    Returns the means and standard deviations of the given features, along with a normalized feature
    matrix.
    ''' 
    means = np.mean(features, axis=0)
    std_devs = np.std(features, axis=0)
    normalized_features = (features - means) / std_devs
    return means, std_devs, normalized_features

def recover_params(means, std_devs, norm_intercept, norm_params):
    ''' 
    Recovers the weights for a linear model given parameters that were fitted using
    normalized features. Takes the means and standard deviations of the original
    features, along with the intercept and parameters computed using the normalized
    features, and returns the intercept and parameters that correspond to the original
    features.
    ''' 
    intercept = norm_intercept - np.sum(means * norm_params / std_devs)
    params = norm_params / std_devs
    return intercept, params

def linear_regression(features, values):
    """
    Perform linear regression given a data set with an arbitrary number of features.
    """
    
    clf = SGDRegressor(n_iter=50)
    results = clf.fit(features, values)
    
    intercept = results.intercept_
    params = results.coef_
    
    return intercept, params

def predictions(dataframe):

    #Index([u'UNIT', u'DATEn', u'TIMEn', u'ENTRIESn', u'EXITSn', u'ENTRIESn_hourly',
    #  u'EXITSn_hourly', u'datetime', u'hour', u'day_week', u'weekday',
    #  u'station', u'latitude', u'longitude', u'conds', u'fog', u'precipi',
    #  u'pressurei', u'rain', u'tempi', u'wspdi', u'meanprecipi',
    #  u'meanpressurei', u'meantempi', u'meanwspdi', u'weather_lat',
    #  u'weather_lon'],

    features = dataframe[['rain','hour','weekday','meantempi']]
    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    #print len(dummy_units.columns)
    features = features.join(dummy_units)
    dummy_units2 = pandas.get_dummies(dataframe['conds'], prefix='conds')
    features = features.join(dummy_units2)
    #print len(dummy_units2.columns)
    
    print features.columns
    
    values = dataframe['ENTRIESn_hourly']
    features_array = features.values
    values_array = values.values
    
    means, std_devs, normalized_features_array = normalize_features(features_array)

    norm_intercept, norm_params = linear_regression(normalized_features_array, values_array)
    
    intercept, params = recover_params(means, std_devs, norm_intercept, norm_params)
    
   # print intercept
   # print params
   # print len(params)
    
    predictions = intercept + np.dot(features_array, params)
    
    return predictions


def compute_r_squared(data, predictions):
    y = data.tolist()
    avgy = np.mean(y)
    top = []
    down = []
    for i in range(0, len(y)):
        top.append((y[i] - predictions[i]) * (y[i] - predictions[i]))
        down.append((y[i] - avgy) * (y[i] - avgy))
    
    return 1 - np.sum(top) / np.sum(down)

def calcResiduals(data, predictions):
    y = data.tolist()
    residuals = []
    for i in range(0, len(y)):
       # residuals.append(math.sqrt((predictions[i]-y[i])*(predictions[i]-y[i])))
        residuals.append(predictions[i]-y[i])
       
    plt.hist(residuals,histtype='bar', stacked=True, fill=True,bins=500)   
    plt.title("Distribution of residuals")
    plt.xlabel('Residuals')
        
    #stats.probplot(residuals, plot=plt)  
    plt.show()   
    


data = pandas.read_csv("turnstile_weather_v2.csv")

#print data.columns
pred=predictions(data)


#print "Prediction made: "+str(len(pred))
print compute_r_squared(data['ENTRIESn_hourly'], pred)
#calcResiduals(data['ENTRIESn_hourly'], pred)



