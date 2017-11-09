#!/usr/bin/python2.7
import json
from bittrex.bittrex import *
import time
import datetime

def printDict(dictionary):
    for i in dictionary.keys():
        print i, dictionary[i]

def getRankByValueInDesent(dictionary):
    desent = sorted(dictionary.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    rank = {}
    k = 1
    for i in desent:
        rank[i[0]] = k
        k += 1
    return rank

def writeRank2Raw(entry):
    t = time.time()
    with open("./data/rawdata/" + str(t), "a") as output_file:
        json.dump(rank, output_file)


if __name__ == '__main__':
    bittrex = Bittrex('', '')
    wholemarket = bittrex.get_market_summaries()
    if wholemarket['success'] != True:
        print 'error loading'

    marketdata = wholemarket['result']
    volumes = {}

    for i in marketdata:
        if i['MarketName'].split('-')[0] == 'BTC':
            volumes[i['MarketName']] = i['BaseVolume']

    rank = getRankByValueInDesent(volumes)
   
    writeRank2Raw(rank)
