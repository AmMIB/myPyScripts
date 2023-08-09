#!/usr/bin/env python
# coding: utf-8
from impala.dbapi import connect
import pandas as pd

##create dinamic input with 
fileName = 'myFile.xlsx'
dateval = '20230101'

#Define Impala Connection
impala_host='host name/ip'
impala_port=21050
impala_ssl=True
impala_db='database'
impala_user='username'
impala_krb_service_name='impala'
impala_auth='GSSAPI'

def impala_init():
    conn = connect(host=impala_host, port=impala_port, use_ssl=impala_ssl, database=impala_db, user=impala_user, kerberos_service_name=impala_krb_service_name, auth_mechanism=impala_auth)
    return conn

conn=impala_init()
cur = conn.cursor()

xldf = pd.read_excel(fileName, engine='openpyxl')
xldf = xldf.replace('\n|\'|,|"', '', regex=True) #clean line break/quote/comma
xldf=xldf.fillna(0)
r, c = xldf.shape
xldf=xldf.astype('string')
xldf['zero']='0' #to have a leading zero
xldf['location']=xldf[['zero','c2','c3']].agg(''.join, axis=1)

xldf=xldf.drop(['zero'],axis=1)

i = 0
insertLs=[]
while (r-1>i) :
    i+=1
    insertLs.append('("'+xldf.iloc[i]['cn']+'","'+xldf.iloc[i]['cnodn']+'","'+xldf.iloc[i]['v']+'","'+
    xldf.iloc[i]['enodnid']+'","'+xldf.iloc[i]['cid']+'","'+xldf.iloc[i]['source']+'","'+
    xldf.iloc[i]['t']+'","'+xldf.iloc[i]['andir']+'","'+xldf.iloc[i]['lat']+'","'+xldf.iloc[i]['log']+'","'+
    xldf.iloc[i]['add']+'","'+xldf.iloc[i]['location']+'","'+dateval+'")')
    if i%10000==0:
        insertStr=str(insertLs)
        insertStr=insertStr[1:len(insertStr)-1].replace("'","")
        print(i)
        query = "insert into database.table_name values "+insertStr
        cur.execute(query)
        insertLs.clear()

insertStr=str(insertLs)
insertStr=insertStr[1:len(insertStr)-1].replace("'","")
query = "insert into database.table_name values "+insertStr
cur.execute(query)
insertLs.clear()
print(i)

