import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DayLocator, DateFormatter
from SPARQLWrapper import SPARQLWrapper, JSON
import datetime
import itertools
import requests
import os
import numpy as  np
import sys

weakg_endpoint = 'http://localhost:8890/sparql'


def sparql_to_dataframe(endpoint, query):
    """
    Convert SPARQL results into a Pandas DataFrame.
    Credit: https://lawlesst.github.io/notebook/sparql-dataframe.html
    """
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()

    cols = results['head']['vars']
    out = []
    for row in results['results']['bindings']:
        item = []
        for c in cols:
            item.append(row.get(c, {}).get('value'))
        out.append(item)

    return pd.DataFrame(out, columns=cols)


def getMetropoleStations():
  query = '''
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX sosa: <http://www.w3.org/ns/sosa/>
    PREFIX weo: <http://ns.inria.fr/meteo/ontology/>
    PREFIX wevp: <http://ns.inria.fr/meteo/vocab/weatherproperty/>
    PREFIX wep: <http://ns.inria.fr/meteo/ontology/property/>
    prefix wdt: <http://www.wikidata.org/prop/direct/>
    prefix wd:   <http://www.wikidata.org/entity/>
    prefix geo2:    <http://www.w3.org/2003/01/geo/wgs84_pos#>

    select distinct ?stationID ?stationName  ?latitude ?longitude ?altitude ?dept ?region ?insee where {
    SERVICE<http://weakg.i3s.unice.fr/sparql>{
        ?station a weo:WeatherStation;
               weo:stationID ?stationID; rdfs:label ?stationName;
               weo:stationID ?id; geo2:altitude ?altitude;
               geo2:lat ?latitude; geo2:long ?longitude;
               dct:spatial ?e .
        ?e  wdt:P131 [rdfs:label ?region; wdt:P2585 ?insee].
        }

    SERVICE <https://query.wikidata.org/sparql> {
        ?e wdt:P131* ?dept .
        ?dept wdt:P31 wd:Q6465 .
        ?dept rdfs:label ?deptLabel .
        ?dept wdt:P2586 ?insee_dept_code .
        FILTER (lang(?deptLabel) = "fr")
        }
    }'''
  return query

def retrieve_weatherStations(endpoint) :
    query = getMetropoleStations()
    stations = sparql_to_dataframe(endpoint, query)
    return stations


def getStationId(stations):
  stations = list(stations["stationID"])
  stationsList = ''
  for k in stations:
    stationsList+="'" + k+"',"
  return stationsList[:-1]



def queryMin(year,month,stations):
  query = '''
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX sosa: <http://www.w3.org/ns/sosa/>
  PREFIX weo: <http://ns.inria.fr/meteo/ontology/>
  PREFIX wevp: <http://ns.inria.fr/meteo/vocab/weatherproperty/>
  PREFIX wep: <http://ns.inria.fr/meteo/ontology/property/>
  SELECT ?stationId  ?groupDate (MIN(?vp) -273.15  as ?dailyMinTemp) where {
    SERVICE<http://weakg.i3s.unice.fr/sparql> {
  ?station weo:stationID ?stationId .
  filter(?stationId in (%s))

}
  {
  ?obs a weo:MeteorologicalObservation;
            sosa:observedProperty wevp:airTemperature;
            sosa:hasSimpleResult ?vp;
            sosa:resultTime ?date;
            wep:madeByStation ?station.
    bind (day(?date)   as ?day)
    bind (month(?date) as ?month)
    bind (year(?date)  as ?year)
    filter(?year in (%s,%s))
    BIND (if(datatype(?year/4)=xsd:integer && ((?year/100)*100 != 0 || (?year/400)*400 = 0) , 1, 0) as ?bissexYear)

        BIND (if (?day = 31 || (?day = 30 && ?month in(4, 6, 9, 11)) || (?day >= 28 && ?month = 2), if(?day = 28 && ?month = 2 && ?bissexYear = 1, ?day+1,1), ?day+1)
        as ?newDay)

        BIND (if (?day = 31 || (?day = 30 && ?month in(4, 6, 9, 11)) || (?day >= 28 && ?month = 2),
        if (?month=12, 1, ?month+1), ?month) as ?newMonth)

        BIND (if (?day=31 && ?month=12, ?year+1, ?year) as ?newYear)

        BIND (
        xsd:date(if (hours(?date)>18 && hours(?date)<=24,
                concat(?newYear, "-", if (?newMonth<10, concat("0", ?newMonth), ?newMonth), "-",
                    if (?newDay<10, concat("0", ?newDay), ?newDay)),
                concat(?year, "-", if (?month<10, concat("0", ?month), ?month), "-",
                    if (?day<10, concat("0", ?day), ?day))))
        as ?groupDate)
    FILTER CONTAINS (STR(?groupDate) , '%s-%s' )
    }
    }
  group by ?groupDate ?stationId
  order by ?groupDate'''%(stations,year,year+1,year,month)
  return query

def get_min_24h(stations, year,month, endpoint):
    stationId = getStationId(stations)
    query_temp = queryMin( year,month,stationId)
    first_day_of_year = datetime.date.min.replace(year = year)
    last_day_of_year = datetime.date.max.replace(year = year)
    annual_temp = sparql_to_dataframe(endpoint, query_temp)
    annual_temp['groupDate'] = pd.to_datetime(annual_temp['groupDate'], format='%Y-%m-%d')
    annual_temp = annual_temp[(annual_temp.groupDate >= pd.to_datetime(first_day_of_year)) & (annual_temp.groupDate <= pd.to_datetime(last_day_of_year))].dropna(axis=1, how="all").reset_index(drop=True)
    return annual_temp


def queryMax(year,month,stations):
  query = '''
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX sosa: <http://www.w3.org/ns/sosa/>
  PREFIX weo: <http://ns.inria.fr/meteo/ontology/>
  PREFIX wevp: <http://ns.inria.fr/meteo/vocab/weatherproperty/>
  PREFIX wep: <http://ns.inria.fr/meteo/ontology/property/>
  SELECT ?stationId  ?groupDate (MAX(?vp) -273.15  as ?dailyMaxTemp) where {
  SERVICE<http://weakg.i3s.unice.fr/sparql> {
  ?station weo:stationID ?stationId .
  filter(?stationId in (%s))

}
  {
  ?obs a weo:MeteorologicalObservation;
            sosa:observedProperty wevp:airTemperature;
            sosa:hasSimpleResult ?vp;
            sosa:resultTime ?date;
            wep:madeByStation ?station.
    bind (day(?date)   as ?day)
    bind (month(?date) as ?month)
    bind (year(?date)  as ?year)
    filter(?year in (%s,%s))
    bind (if (datatype(?year/4)=xsd:integer && ((?year/100)*100 != 0 || (?year/400)*400 = 0) , 1, 0) as ?bissexYear)

    bind (
    if (?day = 1,
        if (?month in (1, 2, 4, 6, 8, 9, 11), 31,
        if (?month in (5, 7, 10, 12), 30,
        if (?bissexYear = 1, 29, 28))),
        ?day - 1)
    as ?previousDay)

    bind (if (?day = 1, if (?month=1, 12, ?month - 1), ?month)   as ?previousMonth)

    bind (if (?day = 1 && ?month=1, ?year - 1, ?year) as ?previousYear)

    bind (xsd:date(if(hours(?date)<=6 && hours(?date) >=0 ,

            concat(?previousYear, "-", if (?previousMonth<10, concat("0", ?previousMonth), ?previousMonth), "-",
                if (?previousDay<10, concat("0", ?previousDay), ?previousDay)),

            concat(?year, "-", if (?month<10, concat("0", ?month), ?month), "-",
                if (?day<10, concat("0", ?day), ?day))))
    as ?groupDate)
    FILTER CONTAINS (STR(?groupDate) , '%s-%s' )
    }
    }
  group by ?groupDate ?stationId
  order by ?groupDate'''%(stations,year,year+1,year,month)
  return query


def get_max_24h(stations, year,month, endpoint):
    stationId = getStationId(stations)
    query_temp = queryMax( year,month,stationId)
    first_day_of_year = datetime.date.min.replace(year = year)
    last_day_of_year = datetime.date.max.replace(year = year)
    annual_temp = sparql_to_dataframe(endpoint, query_temp)
    annual_temp['groupDate'] = pd.to_datetime(annual_temp['groupDate'], format='%Y-%m-%d')
    annual_temp = annual_temp[(annual_temp.groupDate >= pd.to_datetime(first_day_of_year)) & (annual_temp.groupDate <= pd.to_datetime(last_day_of_year))].dropna(axis=1, how="all").reset_index(drop=True)
    return annual_temp

def queryAvgTemp(year,month,stations):
  query = '''
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX sosa: <http://www.w3.org/ns/sosa/>
  PREFIX weo: <http://ns.inria.fr/meteo/ontology/>
  PREFIX wevp: <http://ns.inria.fr/meteo/vocab/weatherproperty/>
  PREFIX wep: <http://ns.inria.fr/meteo/ontology/property/>

  SELECT ?groupDate ?stationId  (AVG(?temp)- 273.15 as ?dailyAvgTemp) where{
  SERVICE<http://weakg.i3s.unice.fr/sparql> {
  ?station weo:stationID ?stationId .
  filter(?stationId in (%s))

}
      {
          ?obs a weo:MeteorologicalObservation;
          sosa:observedProperty wevp:airTemperature;
          sosa:hasSimpleResult ?temp;
          sosa:resultTime ?datetime;
          wep:madeByStation ?station.
          BIND (xsd:date(SUBSTR(STR(?datetime), 1,10)) as ?groupDate)
          FILTER CONTAINS (STR(?groupDate) , '%s-%s' )
      }
      }
    group by ?groupDate ?stationId
    order by ?groupDate
    '''%(stations,year,month)
  return query


def get_avg_24h(stations, year,month, endpoint):
    stationId = getStationId(stations)
    query_temp = queryAvgTemp( year,month, stationId)
    first_day_of_year = datetime.date.min.replace(year = year)
    last_day_of_year = datetime.date.max.replace(year = year)
    annual_temp = sparql_to_dataframe(endpoint, query_temp)
    annual_temp['groupDate'] = pd.to_datetime(annual_temp['groupDate'], format='%Y-%m-%d')
    annual_temp = annual_temp[(annual_temp.groupDate >= pd.to_datetime(first_day_of_year)) & (annual_temp.groupDate <= pd.to_datetime(last_day_of_year))].dropna(axis=1, how="all").reset_index(drop=True)
    return annual_temp


#Sum of precipitations collected every 3 hours
def getRain3H(year,month,stations):
  query = '''
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
  PREFIX sosa: <http://www.w3.org/ns/sosa/>
  PREFIX weo: <http://ns.inria.fr/meteo/ontology/>
  PREFIX wevp: <http://ns.inria.fr/meteo/vocab/weatherproperty/>
  PREFIX wep: <http://ns.inria.fr/meteo/ontology/property/>
  SELECT ?stationId  ?groupDate (sum(?vp)  as ?rainfall24hSum) where {
    SERVICE<http://weakg.i3s.unice.fr/sparql> {
  ?station weo:stationID ?stationId .
  filter(?stationId in (%s))

}
  {
  ?obs a weo:MeteorologicalObservation;
            sosa:observedProperty wevp:precipitationAmount;
            sosa:hasSimpleResult ?vp;
            sosa:phenomenonTime [ a weo:Interval3h ];
            sosa:resultTime ?date;
            wep:madeByStation ?station.
    bind (day(?date)   as ?day)
    bind (month(?date) as ?month)
    bind (year(?date)  as ?year)
    filter(?year in (%s,%s))
    bind (if (datatype(?year/4)=xsd:integer && ((?year/100)*100 != 0 || (?year/400)*400 = 0) , 1, 0) as ?bissexYear)

    bind (
    if (?day = 1,
        if (?month in (1, 2, 4, 6, 8, 9, 11), 31,
        if (?month in (5, 7, 10, 12), 30,
        if (?bissexYear = 1, 29, 28))),
        ?day - 1)
    as ?previousDay)

    bind (if (?day = 1, if (?month=1, 12, ?month - 1), ?month)   as ?previousMonth)

    bind (if (?day = 1 && ?month=1, ?year - 1, ?year) as ?previousYear)

    bind (xsd:date(if(hours(?date)<=6 && hours(?date) >=0 ,

            concat(?previousYear, "-", if (?previousMonth<10, concat("0", ?previousMonth), ?previousMonth), "-",
                if (?previousDay<10, concat("0", ?previousDay), ?previousDay)),

            concat(?year, "-", if (?month<10, concat("0", ?month), ?month), "-",
                if (?day<10, concat("0", ?day), ?day))))
    as ?groupDate)
    FILTER CONTAINS (STR(?groupDate) , '%s-%s' )
    }
    }
  group by ?groupDate ?stationId
  order by ?groupDate'''%(stations,year,year+1,year,month)
  return query


def queryPrecipitation(year,month,stations):
  query = '''
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX sosa: <http://www.w3.org/ns/sosa/>
PREFIX weo: <http://ns.inria.fr/meteo/ontology/>
PREFIX wevp: <http://ns.inria.fr/meteo/vocab/weatherproperty/>
PREFIX wep: <http://ns.inria.fr/meteo/ontology/property/>

SELECT ?groupDate ?stationId (SAMPLE(?precipitation24) as ?rainfall24) where{
  SERVICE<http://weakg.i3s.unice.fr/sparql> {
  ?station weo:stationID ?stationId .
  filter(?stationId in (%s))

}


{
    ?obs a weo:MeteorologicalObservation;
    sosa:observedProperty wevp:precipitationAmount;
    sosa:hasSimpleResult ?r;
    sosa:phenomenonTime [ a weo:Interval24h ];
    sosa:resultTime ?datetime;
    wep:madeByStation ?station.
    BIND(IF(?r > 0.0, ?r, 0.0) AS ?precipitation24)

    BIND (xsd:date(SUBSTR(STR(?datetime), 1,10)) as ?date)
    FILTER (CONTAINS (STR(?datetime), "T06:00:00" ))
    bind (day(?datetime)   as ?day)
    bind (month(?datetime) as ?month)
    bind (year(?datetime)  as ?year)
    filter(?year in (%s,%s))
    bind (if (datatype(?year/4)=xsd:integer && ((?year/100)*100 != 0 || (?year/400)*400 = 0) , 1, 0) as ?bissexYear)
    bind (if (?day = 1,
        if (?month in (1, 2, 4, 6, 8, 9, 11), 31,
        if (?month in (5, 7, 10, 12), 30,
        if (?bissexYear = 1, 29, 28))),
        ?day - 1) as ?previousDay)

    bind (if (?day = 1, if (?month=1, 12, ?month - 1), ?month)   as ?previousMonth)

    bind (if (?day = 1 && ?month=1, ?year - 1, ?year) as ?previousYear)

    bind (concat(?previousYear, "-", if (?previousMonth<10, concat("0", ?previousMonth), ?previousMonth), "-",
                if (?previousDay<10, concat("0", ?previousDay), ?previousDay)) as ?previousDate)

    BIND(xsd:date(?previousDate) as ?groupDate)
    FILTER CONTAINS (STR(?groupDate) , '%s-%s' )
    }
    }
    group by ?groupDate ?stationId
  order by ?groupDate
  '''%(stations,year,year+1,year,month)
  return query


def get_precipitation_24h(stations, year,month, endpoint):
    stationId = getStationId(stations)
    query_temp = queryPrecipitation( year,month,stationId)
    first_day_of_year = datetime.date.min.replace(year = year)
    last_day_of_year = datetime.date.max.replace(year = year)
    annual_temp = sparql_to_dataframe(endpoint, query_temp)
    annual_temp['groupDate'] = pd.to_datetime(annual_temp['groupDate'], format='%Y-%m-%d')
    annual_temp = annual_temp[(annual_temp.groupDate >= pd.to_datetime(first_day_of_year)) & (annual_temp.groupDate <= pd.to_datetime(last_day_of_year))].dropna(axis=1, how="all").reset_index(drop=True)
    return annual_temp


def get_precipitation_3h(stations, year,month, endpoint):
    stationId = getStationId(stations)
    query_temp = getRain3H( year,month,stationId)
    first_day_of_year = datetime.date.min.replace(year = year)
    last_day_of_year = datetime.date.max.replace(year = year)
    annual_temp = sparql_to_dataframe(endpoint, query_temp)
    annual_temp['groupDate'] = pd.to_datetime(annual_temp['groupDate'], format='%Y-%m-%d')
    annual_temp = annual_temp[(annual_temp.groupDate >= pd.to_datetime(first_day_of_year)) & (annual_temp.groupDate <= pd.to_datetime(last_day_of_year))].dropna(axis=1, how="all").reset_index(drop=True)
    return annual_temp

def getPreci(stations, year, month,endpoint):
  preci3 = get_precipitation_3h(stations,year, month, weakg_endpoint)
  preci = get_precipitation_24h(stations,year, month, weakg_endpoint)
  df = pd.merge(preci3,preci, on=['groupDate','stationId'],how='outer')
  df.fillna("Missing",inplace =True)
  df["rainfall24h"] = df['rainfall24']
  ind = list(df.loc[df["rainfall24h"]=="Missing"].index)
  for k in ind:
    df.loc[k,"rainfall24h"] = df.loc[k,"rainfall24hSum"]
  df.drop(["rainfall24","rainfall24hSum"],axis=1,inplace=True)
  return df

def get_aggregates_24h(stations, year,month, endpoint):
    preci = getPreci(stations,year,month,endpoint)
    avg = get_avg_24h(stations,year,month,endpoint)
    max = get_max_24h(stations,year,month,endpoint)
    min = get_min_24h(stations,year,month,endpoint)
    df = pd.merge(avg,preci, on=['groupDate','stationId'],how='outer')
    df = pd.merge(df,max, on=['groupDate','stationId'],how='outer')
    df = pd.merge(df,min, on=['groupDate','stationId'],how='outer')
    return df


def isBisextile(year):
  return year%4==0

def requestOpenMeteo(lon,lat,year,month):
  if month in ("01","03","05","07","08","10","12"):
    day = "31"
  elif month == "02" :
    day = "29" if isBisextile(year) else "28"
  else:
    day = "30"
  year=str(year)
  start = year + "-"+month+"-01"
  end = year + "-"+month+"-"+day
  params={"latitude":lat,"longitude":lon,"timezone":"GMT","start_date":start,"end_date":end,"daily":"et0_fao_evapotranspiration,shortwave_radiation_sum"}
  return requests.get("https://archive-api.open-meteo.com/v1/era5",params=params)

def createJson(station,year,month):
  request =  requestOpenMeteo(station["longitude"],station["latitude"],year,month)
  if request.status_code!=200:
    print("Erreur dans la requête")
    return
  response = request.json()
  dates = response["daily"]["time"]
  evapo = response["daily"]["et0_fao_evapotranspiration"]
  radiations= response["daily"]["shortwave_radiation_sum"]
  df = pd.DataFrame({"groupDate":dates,"evapotranspiration":evapo,"radiationSum":radiations,"stationId":station['stationID']})
  df['groupDate'] = pd.to_datetime(df['groupDate'], format='%Y-%m-%d')
  return df



def getOpenMeteo(stations,year,month):
  df = pd.DataFrame()
  for k in range(len(stations)):
    station = createJson(stations.iloc[k],year,month)
    df = pd.concat([df,station])
  return df

def computeSlice(year,month,endpoint):
  stations = retrieve_weatherStations(endpoint)
  aggregated = get_aggregates_24h(stations,year,month,endpoint)
  openMeteo = getOpenMeteo(stations,year,month)
  df = pd.merge(aggregated,openMeteo, on=['groupDate','stationId'],how='outer')
  df.fillna("Unknown",inplace=True)
  name = "slice" + str(year)+str(month)+".csv"
  df.to_csv("appli/raw-files/csv/"+name,sep=";")
  return df


computeSlice(int(sys.argv[1]),sys.argv[2],weakg_endpoint)
#print("year : " + sys.argv[1] +"\nmonth : " + sys.argv[2])