#!/usr/bin/python3
import datetime
import argparse

import COVID19Py
import termplotlib as tpl

_MAX_WIDTH=150
_ASCII=False

def dict_sum(dict_list):
    sum_dict = {}
    for key in dict_list[0].keys():
        sum_dict[key] = sum(d[key] for d in dict_list)
    return sum_dict

def getTimeLinesByCountryCode(countryCode):
    covid19=COVID19Py.COVID19()
    location=covid19.getLocationByCountryCode(countryCode,timelines=True)
    provinces=[]
    confirmed_timeline=[]
    deaths_timeline=[]
    recovered_timeline=[]
    for province in location:
        confirmed_timeline.append(province['timelines']['confirmed']['timeline'])
        deaths_timeline.append(province['timelines']['deaths']['timeline'])
        recovered_timeline.append(province['timelines']['recovered']['timeline'])
        provinces.append(province['province'])
    sumConfirmed=dict_sum(confirmed_timeline)
    sumDeaths=dict_sum(deaths_timeline)
    sumRecovered=dict_sum(recovered_timeline)
    return {'countryName':location[0]['country'],'provinces':provinces, 'confirmed':sumConfirmed, 'deaths':sumDeaths, 'recovered':sumRecovered}

def plotBarhInTerminal(t,y):
  fig = tpl.figure()
  fig.barh(y,t,force_ascii=_ASCII,max_width=_MAX_WIDTH-25)
  fig.show()

def plotByCountryCode(countryCode, type):
  timelines=getTimeLinesByCountryCode(countryCode)
  t,y=[],[]
  if(type=='confirmed_new'):
    for key in timelines['confirmed']:
      t.append(datetime.datetime.strptime(key, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'))
      y.append(timelines['confirmed'][key])

    y_diff=[e1 - e2 for e1, e2 in zip(y+[0], [0]+y)][:-1]
    y=y_diff
  else:
    for key in timelines[type]:
      t.append(datetime.datetime.strptime(key, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'))
      y.append(timelines[type][key])

  print("="*_MAX_WIDTH)
  str=f"{timelines['countryName']} ({type})"
  print((4)*"="+str+((_MAX_WIDTH-4)-len(str))*"=")
  print("="*_MAX_WIDTH)
  plotBarhInTerminal(t,y)
  print("="*_MAX_WIDTH+"\n")


if __name__ == "__main__":
  #plotByCountryCode("NO","confirmed_new")
  parser = argparse.ArgumentParser()
  parser.add_argument("type")
  parser.add_argument("country",nargs='+')
  args = parser.parse_args()

  for country in args.country:
    plotByCountryCode(country.upper(),args.type)
  
  
  
    
