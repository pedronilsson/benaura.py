#!/usr/bin/env python3

# File to read cities information from
# Format: http://download.geonames.org/export/dump/
CITIES = 'placenames.csv'

# Max number of cities to display on histogram
T = 10

import sys
import csv
import re
from collections import defaultdict
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # Read text input
    text = ""
    for pth in sys.argv[1:]:
        with open(pth, 'r') as f:
            text += f.read()
    #words = text.split()
    words = re.findall(r"[\w']+|[.,!?;]", text)
    words = list(filter(lambda x: x[0].isalpha(), words))
    
    if len(words) == 0:
        print('No input!')
        sys.exit(1)
    
    # Read geo names
    with open(CITIES, 'r', encoding='latin1') as f:
        reader = csv.reader(f)
        geolines = [line for line in reader]
    
    # name -> id
    geonames = { }
    cnt = 0
    geo = { }
    for elem in geolines:
        _id = cnt
        cnt += 1
        colB, colC, colD = elem[1].strip(), elem[2].strip(), elem[3].strip()
        geonames[colB.lower()] = _id
        geonames[colC.lower()] = _id
        for ver in colD.split(','):
            geonames[ver.lower().strip()] = _id
        geo[_id] = (elem[4].strip(), elem[5].strip(), elem[1].strip())
    
    #geo = {int(x[0]) : (x[4].strip(), x[5].strip(), x[1].strip()) for x in geolines}
    
    # counts[id] = <count matches>
    counts = defaultdict(int)
    
    # Load the stoplist from txt file (create empty one if not present)
    with open('stoplist.txt', 'a+') as f:
        f.seek(0, 0) # go to beginning
        stoplist = {word.strip().lower() for word in f.readlines()}
        
    # Search names in text
    for i in range(len(words)):
        # Look up 1-4 words in text
        # City name can include up to 4 words
        w1 = words[i]
        w2 = w1 + ' ' + words[i+1] if i + 1 < len(words) else ''
        w3 = w2 + ' ' + words[i+2] if i + 2 < len(words) else ''
        w4 = w3 + ' ' + words[i+3] if i + 3 < len(words) else ''
        for w in (w1,w2,w3,w4):
            w = w.lower().strip()
            if len(w) <= 3: continue # skip too short words
            if w in geonames and w not in stoplist:
                _id = geonames[w]
                counts[_id] += 1
    
    # Construct stats: [name, lat, long, count]
    stats = [(geo[i][2], geo[i][0], geo[i][1], counts[i]) for i in counts]
    
    # Sort it by count
    stats = sorted(stats, key=lambda x: x[3], reverse=True)

    # Plot top T with bars
    r = range(min(T, len(stats)))
    h = [x[3] for x in stats[:T]]
    names = [x[0] for x in stats[:T]]
    plt.bar(r, height=h)
    plt.xticks(r, names, rotation='vertical')
    # Pad margins so that markers don't get clipped by the axes
    plt.margins(0.05)
    # Tweak spacing to prevent clipping of tick-labels
    plt.subplots_adjust(bottom=0.3)
    plt.savefig('count_hist.png')
    
    # Draw heatmap
    lats = []
    lngs = []
    freqs = []
    for p in stats:
        lats.append(float(p[1]))
        lngs.append(float(p[2]))
        freqs.append(int(p[3]))
            
    with open('kepler.csv', 'w+') as f:
        f.write('cities_lat,cities_lng,freq\n')
        for lat, lng, freq in zip(lats, lngs, freqs):
            f.write(str(lat) + ',' + str(lng) + ',' + str(freq) + '\n')
    
    with open('stats.csv', 'w+') as f:
        f.write('city,lat,lng,freq\n')
        for city in stats:
            f.write(city[0]+','+str(city[1])+','+str(city[2])+','+str(city[3])+'\n')
