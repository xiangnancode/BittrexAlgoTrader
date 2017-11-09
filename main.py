import json
from bittrex.bittrex import *
import time
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import collections

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

def writeRank2CSV(entry, output_filename):
    with open("./data/" + output_filename + ".csv", "r") as input_file:
        header = input_file.readline().strip('\n').split(',')
    t = time.time()
    timestamp = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
    line = timestamp
    for i in range(1, len(header)):
        line += "," + str(entry[header[i]])
    line += '\n'
    with open("./data/" + output_filename + ".csv", "a") as output_file:
        output_file.write(line)

def sendEmail2(sendto, text):
    fromaddr = "algotrader.automsg@gmail.com"
    toaddr = ['algotrader.automsg@gmail.com']# + sendto
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddr)
    msg['Subject'] = "Sending Email Alert Test"
     
    body = text
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "algotrader123698745")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    
if __name__ == '__main__':
    with open("secrets.json") as secrets_file:
        secrets = json.load(secrets_file)
        secrets_file.close()
    bittrex = Bittrex(secrets['key'], secrets['secret'])

    timeInterval = 60*30
    flag = True
    hourlyRank = {}
    timeline = []#collections.deque(maxlen = 12)
    while (1):
        t = time.time()
        if (int(t) % timeInterval == 0 and flag):
            timestamp = datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S')
            timeline.append(timestamp)
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
            print timestamp
            writeRank2CSV(rank, 'HourlyRank')
            msg = ''
            for key, val in hourlyRank.items():
                keymax = max(val)
                keymin = min(val)
                maxi = val.index(max(val))
                mini = val.index(min(val))
                if (keymax - keymin >= 20 and mini > maxi and timestamp == timeline[mini]):
                    msg += 'Rank of '+key+' has raised from '+str(keymax)+'('+timeline[maxi]+') to '+str(keymin)+'('+timeline[mini]+')\n'
            if (msg != ''):
                sendEmail2('test', msg)
                print msg
                    
            if (len(hourlyRank['BTC-NEO']) > 30):
                break
        elif (int(t) % timeInterval != 0):
            flag = True
            
        
