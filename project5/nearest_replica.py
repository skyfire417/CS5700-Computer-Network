import re
import json
import urllib2
import sys
import math

SERVERS = ['54.186.185.27','54.199.204.174','54.72.143.213','54.84.248.26']
PUBLIC_IP = sys.argv[1]

def get_distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c
    return d

def get_location(ipaddr):
    url = 'http://ipinfo.io/%s' % ipaddr
    response = urllib2.urlopen(url)
    data = json.load(response)
    loc = data['loc'].split(',')
    lat = float(loc[0])
    lon = float(loc[1])
    # print data['country']
    return (lat,lon)


if __name__ == '__main__':
    # print 'public ip:', PUBLIC_IP
    public_loc = get_location(PUBLIC_IP)
    distances = {}
    for s in SERVERS:
        server_loc = get_location(s)
        distances[s] = get_distance(public_loc, server_loc)
    # print distances
    res = min(distances, key=distances.get)
    print res
    