import numpy as np
import random
import joblib
from flask import Flask , render_template , request , flash , redirect , url_for
import datetime

def getCoords(coords):  
    for i in range(len(coords)):
        if(coords[i] == '['):
            start = i 
        if(coords[i] == ']'):
            end = i+1
            break 

    coords = coords[start+1 : end-1]
    pair = coords.split(",")
    x = float(pair[0])
    y = float(pair[1])        
    return x , y 
def getAgeGroup(age):
    try : 
        age = int(age)
        if(age>64):
            return 1
        if(age<18):
            return 5
        if(age>19 and age<25):
            return 3
        if(age>24 and age<45):
            return 4
        if(age>44 and age<65):
            return 2

    except : 
        return 0  
def getSex(sexe):
    d = 0 
    m = 0 
    f = 0
    e = 0
    u = 0
    if(sexe=='D'):
        d=1
    if(sexe=='F'):
        f=1
    if(sexe=='M'):
        m=1
    if(sexe=='E'):
        e=1
    if(sexe=='U'):
        u=1    
    return d,e,f,m,u
def getRaces(race):
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    o = 0
    if(race=='a'):
        a = 1
    if(race=='b'):
        b = 1
    if(race=='c'):
        c = 1
    if(race=='d'):
        d = 1
    if(race=='e'):
        e = 1
    if(race=='f'):
        f = 1
    if(race=='g'):
        g = 1
    if(race=='o'):
        o = 1

    return a , b, c , d, o, e , f , g
def getPatrolBoro(PATROL_BORO):
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    o = 0
    if(PATROL_BORO=='a'):
        a = 1
    if(PATROL_BORO=='b'):
        b = 1
    if(PATROL_BORO=='c'):
        c = 1
    if(PATROL_BORO=='d'):
        d = 1
    if(PATROL_BORO=='e'):
        e = 1
    if(PATROL_BORO=='f'):
        f = 1
    if(PATROL_BORO=='g'):
        g = 1
    if(PATROL_BORO=='o'):
        o = 1

    return a , b, c , d, e , f , g , o    


def getBoro(BORO):
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0

    if(BORO=='a'):
        a = 1
    if(BORO=='b'):
        b = 1
    if(BORO=='c'):
        c = 1
    if(BORO=='d'):
        d = 1
    if(BORO=='e'):
        e = 1
 
    return a , b, c , d, e 

def getLocOccur(LOC_OF_OCCUR):
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0

    if(LOC_OF_OCCUR=='a'):
        a = 1
    if(LOC_OF_OCCUR=='b'):
        b = 1
    if(LOC_OF_OCCUR=='c'):
        c = 1
    if(LOC_OF_OCCUR=='d'):
        d = 1
    if(LOC_OF_OCCUR=='e'):
        e = 1
 
    return a , b, c , d, e 

def getTime(time):
    time = str(time)
    tmp = time.split(':')[0]
    if int(tmp)>6 and int(tmp)<=12:
        return 1
    elif int(tmp)>12 and int(tmp)<=17 :
        return 2
    elif int(tmp)<20:
        return 3
    else : 
        return 4
def getKeyFromValue(arg):
    t = []
    for k , v in df_mapping.items():
        if v == arg :
            t.append(k)
    return t 
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def index():
    coords = ''
    if request.method == "POST":
        coords = request.form.get('coords')
        name = request.form.get('name')
        race = request.form.get('race')
        sexe = request.form.get('sexe')
        age = request.form.get('age')
        PATROL_BORO = request.form.get('PATROL_BORO')
        LOC_OF_OCCUR = request.form.get('LOC_OF_OCCUR')
        BORO = request.form.get('BORO')
        ADDR_PCT_CD = request.form.get('ADDR_PCT_CD')
        ADDR_PCT_CD = float(ADDR_PCT_CD)
        BEHIND= random.choice([344., 109., 341., 578., 116., 118., 351., 107., 347., 235., 233.,352., 361., 106., 236.])
        all_crimes = ["assualt","grand larency","petit larency",
        "harrasment","exposed to weapons","criminal crimes","public safty crimes","administrative crimes","vehical crimes",
        "drugs and alcaholic crimes","theif and robbery ","kidnapping","frauds","children crimes"]

        trip_time_str = request.form.get('trip_time')
        trip_time = datetime.datetime.strptime(trip_time_str, '%Y-%m-%dT%H:%M')
        Latitude, Longitude = getCoords(coords)
        VIC_AGE_GROUP = getAgeGroup(age)
        VIC_SEX_D, VIC_SEX_E, VIC_SEX_F, VIC_SEX_M, VIC_SEX_U = getSex(sexe)
        a , b , c , d , e , f , g , o  = getRaces(race)
        time = getTime(trip_time.time())

        BKLYNNORTH, BKLYNSOUTH, BRONX,MANNORTH,MANSOUTH,QUEENSNORTH,QUEENSSOUTH,STATENISLAND =getPatrolBoro(PATROL_BORO)
        BORO_NM_BRONX,BORO_NM_BROOKLYN,BORO_NM_MANHATTAN,BORO_NM_QUEENS,BORO_NM_STATENISLAND=getBoro(BORO)
        FRONT,INSIDE,OPPOSITE,REAR,UNKNOWN=getLocOccur(LOC_OF_OCCUR)

        input = [ADDR_PCT_CD,Latitude, Longitude, VIC_AGE_GROUP, trip_time.month, trip_time.year, trip_time.day, time,VIC_SEX_D, VIC_SEX_E, VIC_SEX_F, VIC_SEX_M, VIC_SEX_U, a , b , c , d , e , f , g , o, BKLYNNORTH, BKLYNSOUTH, BRONX,MANNORTH,MANSOUTH,QUEENSNORTH,QUEENSSOUTH,STATENISLAND, BORO_NM_BRONX,BORO_NM_BROOKLYN,BORO_NM_MANHATTAN,BORO_NM_QUEENS,BORO_NM_STATENISLAND, FRONT,INSIDE,OPPOSITE,REAR,BEHIND,UNKNOWN]
        coords = [Latitude , Longitude ]
        input = [input]
        rf_model = joblib.load("rf_model.h5")

        result1 = rf_model.predict(input)
        proba = rf_model.predict_proba(input)
        CrimesList = dict(zip(all_crimes, proba[0]))
        return render_template("result.html", crimes = CrimesList)
        
    return render_template("index.html", coords = coords )

if __name__ == '__main__':
    app.run(debug=True)