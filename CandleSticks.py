#for info on documentation see https://stackoverflow.com/questions/59745818/how-talib-is-detecting-patterns/59756160#59756160
#https://www.quantopian.com/posts/talib-cdl-candle-indicators
#https://manual.zorro-project.com/candle.htm
#https://cryptotrader.org/talib
#http://tadoc.org/
#https://rdrr.io/rforge/candlesticks/man/candlesticks-package.html
#https://arxiv.org/pdf/1808.00418.pdf
#https://www.ijitee.org/wp-content/uploads/papers/v8i7/G5451058719.pdf
#py36

import talib as ta
import pandas as pd
import mplfinance as mpf
import numpy as np
import uuid

#CDLDOJI: Doji, single candle pattern. Trend reversal.
#CDL2CROWS: Two Crows, a bearish candle pattern.

#----------USING SPY.csv and SPY_1443Days.csv to form Candle stick images(use both one after the other)-----------------

# candle_data_2000=pd.read_csv("C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\SPY_1443Days.csv", header=0, infer_datetime_format=True, parse_dates=True)
candle_data_2000=pd.read_csv("C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\SPY.csv", header=0, infer_datetime_format=True, parse_dates=True)
candle_data_2000['RSI'] = ta.RSI(candle_data_2000.Close, timeperiod=20)
# candle_data['MACD'], candle_data['macdsignal'],candle_data['macdhist'] = ta.MACDFIX(candle_data.Close, signalperiod=20)
candle_data_2000=candle_data_2000.drop(["Adj Close"], axis=1)
candle_data_2000['Date']=pd.to_datetime(candle_data_2000['Date']) 


path_to_images="C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\images_new\\"

candle_data_2000=candle_data_2000.set_index('Date')
result=pd.DataFrame(columns=['id','target'])

#----------Run the following code to form monthly candle stick graphs for each year--------
years=[2001,2002,2003,2005,2006,2007,2009,2010,2011,2013]
# dict_={'Jun':30,'Jul':31,'Aug':31,'Sep':30,'Oct':31,'Nov':30,'Dec':31}
# dict_={'Jan':29}
dict_={'Jan':31,'Feb':29,'Mar':31,'Apr':30,'May':31,'Jun':30,'Jul':31,'Aug':31,'Sep':30,'Oct':31,'Nov':30,'Dec':31}

for year in years:
    for key,value in dict_.items():
        start_date='{}-{}-01'.format(year,key)
        end_date='{}-{}-{}'.format(year,key,value)
        candle_month=candle_data_2000.loc[start_date:end_date]
        
        close=candle_month.Close
        n=candle_month.shape[0]
        try:
            if close[n-1]>=close[n-2]:
                target=1
            else:
                target=0
        finally:
            print(target)
        
        fig_id_=str(uuid.uuid4())
        result=result.append({"id":fig_id_+".png","target":target}, ignore_index=True)
        
        save = dict(fname=path_to_images+fig_id_+".png",dpi=10,bbox_inches='tight',pad_inches=0)
        # apdict = mpf.make_addplot(candle_month[["RSI","MACD"]], color='orange')
        apdict = mpf.make_addplot(candle_month["RSI"])
        # addplot=apdict
        mpf.plot(candle_month[-n:], type="candlestick",volume=True,mav=(3),figratio=(10,10),ylabel='',addplot=apdict,show_nontrading =True,savefig=save )
        fig_id_=""
        target=""
        del candle_month
# del result

#------------Saving the results in .csv------------
#---------------Must be run after the generation of all candle stick images
result.to_csv("C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\results.csv", index=False)




#-----------------**Code for seperating the candle stick images into Train and Test folder**---------------
#-----------------20% of the result set were seperated as validation set------------------

move_directory_train="C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\Train_images\\"
move_directory_val="C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\Val_images\\"

train=pd.read_csv("C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\TrainSet.csv", header=0)
validation=pd.read_csv("C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\validationSet.csv", header=0)


directory ="C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\images_new\\"

trainimg=0
valid=0
for subdir, dirs, files in os.walk(directory):
    count=0
    for filename in files:
        count+=1
        # file=os.path.splitext(filename)[0]
        if filename in str(validation.id):
            valid+=1
            shutil.copyfile(subdir+filename,move_directory_val+filename)
        else:
            trainimg+=1
            shutil.copyfile(subdir+filename,move_directory_train+filename)
            
    print(count)
    print(trainimg)
    print(valid)

print(result['target'].nunique())
print(len(result.loc[result['target']==1]))
print(len(result.loc[result['target']==0]))




#----------Code for resizing the images if required-----------------------
'''
import shutil,os
from PIL import Image
for subdir,dirs,files in os.walk(move_directory_val):
    for file in files:
        img= Image.open(subdir+file).convert('LA').resize(224*224)
        print(img.size)
        # img.save(val_directory+file)

'''
'''
import PIL
from PIL import Image,ImageChops
path="C:\\Users\\megha\\Documents\\UOFT\\UOFT Winter2020\\AI in Finance\\FinalProject\\Talib_PatternRecognition\\Dataset\\images_new\\aa394d4e-60dd-4da0-879a-be9791e256d7.png"
im = Image.open(path)
im.size
im.close
'''