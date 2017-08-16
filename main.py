import json
from bittrex.bittrex import Bittrex
import time
import datetime

def printDict(dictionary):
    for i in dictionary.keys():
        print i, dictionary[i]

def getRankByValueInDesent(dictionay):
    desent = sorted(dictionay.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    rank = {}
    k = 0
    for i in desent:
        rank[i[0]] = k
        k += 1
    return rank

if __name__ == '__main__':
    bittrex = Bittrex(None, None)

    timeInterval = 5
    flag = True
    hourlyRank = {}
    while (1):
        t = time.time()
        if (int(t) % timeInterval == 0 and flag):
            wholemarket = bittrex.get_market_summaries()
            if wholemarket['success'] != True:
                print 'error loading'

            marketdata = wholemarket['result']
            volumes = {}

            for i in marketdata:
                if i['MarketName'].split('-')[0] == 'BTC':
                    volumes[i['MarketName']] = i['BaseVolume']

            rank = getRankByValueInDesent(volumes)

            
            for i in rank.keys():
                hourlyRank.setdefault(i, []).append(rank[i])
                
            flag = False
            print 'hour', len(hourlyRank['BTC-NEO'])
            if (len(hourlyRank['BTC-NEO']) > 11):
                break
        elif (int(t) % timeInterval != 0):
            flag = True
    #printDict(hourlyRank)
    for key, val in hourlyRank.items():
        if (max(val) - min(val) >= 1 and val.index(min(val)) > val.index(max(val))):
            print 'Rank of', key, 'has raised from', max(val), '(hour', val.index(max(val)), ')', 'to', min(val), '(hour', val.index(min(val)), ')'
