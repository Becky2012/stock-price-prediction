#import tools
import re    
import urllib.request
import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
############################################################################
from scipy import interpolate
############################################################################
import datetime as dt
#receive the real time stock price via google finance
url='http://www.google.com/finance/getprices?q=APPL&p=50d&f=d,c,h,l,o,v'
f1=str(urllib.request.urlopen(url).read())
result=f1[2:-1].split('\\n')
#process unstructured online real time data
data=[]
for eachLine in result:
    if len(eachLine)<1:
        continue
    if re.match('\d',eachLine) is not None or eachLine[0]=='a':
        data.append(eachLine.split(','))
print(len(data))
#save a list as numpy array
npdata=np.array(data)   
print(npdata)
dfdata=pd.DataFrame(npdata,columns=["DATE","CLOSE","HIGH","LOW","OPEN","VOLUMN"])
dfdata["DATE"]=range(1,(len(data)+1))
print (dfdata)
fdfdata=dfdata.apply(pd.to_numeric)
print(fdfdata['DATE'].describe())
############################################################################
#predict the stock price of next business day 
newx=np.array(fdfdata['DATE'])
newx=np.append(newx,[50])
print(newx)
newy = interpolate.UnivariateSpline(fdfdata['DATE'],fdfdata['CLOSE'],s=200)(newx)
############################################################################
#Visualize stock price chart
plt.figure(figsize=(13,7),dpi=80)
plt.title("Stock price - spline regression & prediction(APPL)",fontsize=18)
plt.xlabel("50 Days",fontsize=14, color='black')
plt.ylabel("Price (dollors: $)",fontsize=14, color='black')
#plt.plot(x,y)
plt.plot(fdfdata['DATE'],fdfdata['CLOSE'],label="Close",color="#87CEFA",linewidth=2.5,linestyle="-")
plt.plot(fdfdata['DATE'],fdfdata['OPEN'],label="Open",color="#FF1493",linewidth=2.5,linestyle="-")
plt.plot(fdfdata['DATE'],fdfdata['HIGH'],label="High",color="#90EE90",linewidth=2.5,linestyle="-")
plt.plot(fdfdata['DATE'],fdfdata['LOW'],label="Low",color="#FFFF00",linewidth=2.5,linestyle="-")
plt.plot(newx,newy,label="Regression",color="#000000",linewidth=2.5,linestyle="--")
plt.xlim([0.0, 51.0])
plt.legend(loc="upper left")
plt.grid(True)
plt.savefig('stock.pdf')
