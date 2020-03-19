#!/usr/bin/python3
import datetime
import argparse

import COVID19Py
import termplotlib as tpl

_MAX_WIDTH=100

def getTimeLinesByCountryCode(countryCode):
  covid19=COVID19Py.COVID19()
  location=covid19.getLocationByCountryCode(countryCode,timelines=True)
  confirmed_timeline=location[0]['timelines']['confirmed']['timeline']
  death_timeline=location[0]['timelines']['deaths']['timeline']
  recovered_timeline=location[0]['timelines']['recovered']['timeline']
  return {'location':location, 'confirmed':confirmed_timeline, 'deaths':death_timeline, 'recovered':recovered_timeline}

def plotBarhInTerminal(t,y):
  fig = tpl.figure()
  fig.barh(y,t,force_ascii=True,max_width=_MAX_WIDTH-25)
  #fig.barh(y,t)
  fig.show()

def plotByCountryCode(countryCode, type):
  timelines=getTimeLinesByCountryCode(countryCode)
  t,y=[],[]
  for key in timelines[type]:
    t.append(datetime.datetime.strptime(key, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d'))
    y.append(timelines[type][key])
  print("="*_MAX_WIDTH)
  str=f"{timelines['location'][0]['country']} ({type})"
  print((4)*"="+str+((_MAX_WIDTH-4)-len(str))*"=")
  print("="*_MAX_WIDTH)
  plotBarhInTerminal(t,y)
  print("="*_MAX_WIDTH+"\n")

if __name__ == "__main__":
  #plotByCountryCode("NO","confirmed")
  parser = argparse.ArgumentParser()
  parser.add_argument("type")
  parser.add_argument("country",nargs='+')
  args = parser.parse_args()

  for country in args.country:
    plotByCountryCode(country,args.type)
  
  
  
    