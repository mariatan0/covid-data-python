#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 20:05:33 2020

@author: isqsdac
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 11:47:00 2020

@author: isqsdac
"""

import io
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

#variables needed for ease of file access
path = '~/Desktop/data_set_project/'
file_1 = 'us_states_covid19_daily.csv'
file_2 = 'CAUR.csv'
file_3 = 'HIURN.csv'
file_4 = 'NYUR.csv'
file_5 = 'TXUR.csv'
path_2 = '~/Desktop/data_set_project/output/'
output_1 = 'aggregate merged cases and unemployment rate.csv'
output_2 = 'merged ca.csv'
output_3 = 'merged hi.csv'
output_4 = 'merged ny.csv'
output_5 = 'merged tx.csv'

#pull daily covid cases by state
df_daily_covid = pd.read_csv(path + file_1)  
df_daily_covid

#pull unemployment rate of California
df_ca = pd.read_csv(path + file_2)  
df_ca

#pull unemployment rate of Hawaii
df_hi = pd.read_csv(path + file_3)  
df_hi

#pull unemployment rate of NY
df_ny = pd.read_csv(path + file_4)  
df_ny

#pull unemployment rate of TX
df_tx = pd.read_csv(path + file_5)  
df_tx

#delete all unnecessary columns
df_daily_covid = df_daily_covid.loc[:, df_daily_covid.columns.intersection(['date', 'state', 'positiveIncrease'])]

df_ca['state']='CA'
df_hi['state']='HI'
df_tx['state']='TX'
df_ny['state']='NY'

#sep date into 3 columns
#for daily covid dates
df_daily_covid['date'] = df_daily_covid['date'].astype(str)
df_daily_covid['year'] = df_daily_covid['date'].str[0:4]
df_daily_covid['month'] = df_daily_covid['date'].str[4:6]
df_daily_covid['day'] = df_daily_covid['date'].str[6:8]
#CA dates
df_ca['year'] = df_ca['DATE'].str[0:4]
df_ca['month'] = df_ca['DATE'].str[5:7]
#HI dates
df_hi['year'] = df_hi['DATE'].str[0:4]
df_hi['month'] = df_hi['DATE'].str[5:7]
#ny dates
df_ny['year'] = df_ny['DATE'].str[0:4]
df_ny['month'] = df_ny['DATE'].str[5:7]
#tx dates
df_tx['year'] = df_tx['DATE'].str[0:4]
df_tx['month'] = df_tx['DATE'].str[5:7]


#group by month for daily covid data
df_daily_covid_ag = df_daily_covid[['state', 'year', 'month', 'positiveIncrease']].groupby(['state', 'year', 'month']).sum()
df_daily_covid_ag1 = df_daily_covid_ag.reset_index()
#sep index into columns
df_daily_covid_ag['state'] = df_daily_covid_ag.index.get_level_values(0)
df_daily_covid_ag['year'] = df_daily_covid_ag.index.get_level_values(1)
df_daily_covid_ag['month'] = df_daily_covid_ag.index.get_level_values(2)

#merge 
df_merged = df_daily_covid_ag1.merge(df_ca, how='left', left_on=['state', 'year', 'month'], right_on = ['state', 'year', 'month']).merge(df_hi, how='left', left_on=['state', 'year', 'month'], right_on = ['state', 'year', 'month']).merge(df_tx, how='left', left_on=['state', 'year', 'month'], right_on = ['state', 'year', 'month']).merge(df_ny, how='left', left_on=['state', 'year', 'month'], right_on = ['state', 'year', 'month']).drop(columns=['DATE_x', 'DATE_y'])

#drop rows
df_merged.drop(df_merged.index[0:35], inplace=True)
df_merged.drop(df_merged.index[7:56], inplace=True)
df_merged.drop(df_merged.index[14:178], inplace=True)
df_merged.drop(df_merged.index[21:84], inplace=True)
df_merged.drop(df_merged.index[28:87], inplace=True)

df_merged = df_merged.reset_index()
del df_merged['index']

#stack states UR into single column
df_merged_stacked= df_merged.set_index(['state','year','month','positiveIncrease']).stack().reset_index()
df_merged_stacked=df_merged_stacked.rename(columns={0:'unemployment rate'})
df_merged_stacked=df_merged_stacked[['state','year','month','positiveIncrease','unemployment rate']]

#output file of states, positive cases and unemployment rate
df_merged_stacked.to_csv(path_2 + output_1, index=True)

###
########################
## ur rate plot
month=df_merged['month']
caur=df_merged['CAUR']
txur=df_merged['TXUR']
nyur=df_merged['NYUR']
hiur=df_merged['HIURN']
plt.figure(0) ##all unemployment rates together
plt.plot(month,caur,label='CA',)
plt.plot(month,txur,label='TX')
plt.plot(month,nyur,label='NY')
plt.plot(month,hiur,label='HI')
## labels and lefgend
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title("State's Unemployment Rate 2020")
plt.legend()
plt.show()
##plt.savefig('plot.png')
###########################
##seperating the states up
df_merged_ca=df_merged.loc[0:6,['state','year','month','positiveIncrease', 'CAUR']] ##row 0 to 6; all columns
df_merged_hi=df_merged.loc[7:13,['state','year','month','positiveIncrease','HIURN']]
df_merged_ny=df_merged.loc[14:20,['state','year','month','positiveIncrease','NYUR']]
df_merged_tx=df_merged.loc[21:27,['state','year','month','positiveIncrease','TXUR']]

#output file for each state
df_merged_ca.to_csv(path_2 + output_2, index=True)
df_merged_hi.to_csv(path_2 + output_3, index=True)
df_merged_ny.to_csv(path_2 + output_4, index=True)
df_merged_tx.to_csv(path_2 + output_5, index=True)
#########################
######CALI#######################
plt.figure(1) ##positvie case rate ca

plt.plot(df_merged_ca['month'],df_merged_ca['positiveIncrease'],'o-')
plt.xlabel('Month')
plt.ylabel('Positive Cases')
plt.title('CA Positive Cases 2020')
plt.show(1)

plt.figure(2) ##unemployment rate ca
plt.plot(df_merged_ca['month'],df_merged_ca['CAUR'],'o-')
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('California Unemployment Rate 2020')
plt.show(2)
##
#########################
#########NY###################
plt.figure(3) ##positvie case rate ny

plt.plot(df_merged_ny['month'],df_merged_ny['positiveIncrease'],'o-',color='green')
plt.xlabel('Month')
plt.ylabel('Positive Cases')
plt.title('NY Positive Cases 2020')
plt.show(3)

plt.figure(4) ##unemployment rate ny
plt.plot(df_merged_ny['month'],df_merged_ny['NYUR'],'o-',color='green')

plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('New York Unemployment Rate 2020')
plt.show(4)
#####################################
##############HI####################
plt.figure(5) ##positvie case rate hi

plt.plot(df_merged_hi['month'],df_merged_hi['positiveIncrease'],'o-',color='red')
plt.xlabel('Month')
plt.ylabel('Positive Cases')
plt.title('HI Positive Cases 2020')
plt.show(5)

plt.figure(6) ##unemployment rate hi
plt.plot(df_merged_hi['month'],df_merged_hi['HIURN'],'o-',color='red')
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('Hawaii Unemployment Rate 2020')
plt.show(6)
##################################
#################TX#################
plt.figure(7) ##positvie case rate tx
plt.xlabel('Month')
plt.ylabel('Positive Cases')
plt.title('TX Positive Cases 2020')
plt.plot(df_merged_tx['month'],df_merged_tx['positiveIncrease'],'o-',color='orange')

plt.show(7)

plt.figure(8) ##unemployment rate tx
plt.plot(df_merged_tx['month'],df_merged_tx['TXUR'],'o-',color='orange')
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('Texas Unemployment Rate 2020')
plt.show(8)
#######################
#bar graphs for new cases
plt.figure(9)
plt.bar(df_merged['month'],df_merged['positiveIncrease'])
plt.title("All State's New Cases by Month")
plt.xlabel('Month')
plt.ylabel('New Cases')
plt.show(9)

plt.figure(10) ##new case rate ca
plt.xlabel('Month')
plt.ylabel('New Cases')
plt.title('New Cases in CA 2020')
plt.bar(df_merged_ca['month'],df_merged_ca['positiveIncrease'])
plt.show(10)

plt.figure(11) ##new case rate hi
plt.xlabel('Month')
plt.ylabel('New Cases')
plt.title('New Cases in HI 2020')
plt.bar(df_merged_hi['month'],df_merged_hi['positiveIncrease'])
plt.show(11)

plt.figure(12) ##new case rate ny
plt.xlabel('Month')
plt.ylabel('New Cases')
plt.title('New Cases in NY 2020')
plt.bar(df_merged_ny['month'],df_merged_ny['positiveIncrease'])
plt.show(12)

plt.figure(13) ##new case rate tx
plt.xlabel('Month')
plt.ylabel('New Cases')
plt.title('New Cases in TX 2020')
plt.bar(df_merged_tx['month'],df_merged_tx['positiveIncrease'])
plt.show(13)

#bar graph for unemployment rate
plt.figure(14) ##ur of ca
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('Unemployment Rate in CA 2020')
plt.bar(df_merged_ca['month'],df_merged_ca['CAUR'])
plt.show(14)

plt.figure(15) ##ur of hi
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('Unemployment Rate in HI 2020')
plt.bar(df_merged_hi['month'],df_merged_hi['HIURN'])
plt.show(15)

plt.figure(16) ##ur of ny
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('Unemployment Rate in NY 2020')
plt.bar(df_merged_ny['month'],df_merged_ny['NYUR'])
plt.show(16)

plt.figure(17) ##ur of tx
plt.xlabel('Month')
plt.ylabel('Unemployment Rate')
plt.title('Unemployment Rate in TX 2020')
plt.bar(df_merged_tx['month'],df_merged_tx['TXUR'])
plt.show(17)





































