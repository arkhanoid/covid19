# pega os dados mundiais
import urllib, json, re, sys
from datetime import date
url = "https://pomber.github.io/covid19/timeseries.json"
response = urllib.urlopen(url)
data = json.loads(response.read())
lfd = date(2020, 1, 22) 
print "Dias,casos,recuperados,mortos"
for l in  data[sys.argv[1]]:
    if l['confirmed'] > 0: 
        dd = re.findall(r'(\d{4})-(\d+)-(\d+)', l['date'])[0]
        dias = date(int(dd[0]), int(dd[1]), int(dd[2])) - lfd 
        print "%s, %d,%d,%d" % ( dias.days, l['confirmed'], l['recovered'], l['deaths'] )
    else:
        dd = re.findall(r'(\d{4})-(\d+)-(\d+)', l['date'])[0]
        lfd =  date(int(dd[0]), int(dd[1]), int(dd[2])) 


