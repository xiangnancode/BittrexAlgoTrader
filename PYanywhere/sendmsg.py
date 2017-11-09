#!/usr/bin/python2.7
import json
from bittrex.bittrex import *
import time
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import collections
import os
import shutil



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
    toaddr = ['algotrader.automsg@gmail.com'] + sendto
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
    rawfilelist = os.listdir("./data/rawdata/")
    hourlyRank = {}
    timeline = []
    for rawfile in rawfilelist:
        timestamp = datetime.datetime.fromtimestamp(float(rawfile)).strftime('%Y-%m-%d %H:%M:%S')
        timeline.append(timestamp)
        with open("./data/rawdata/" + rawfile, "r") as f:
            rank = json.load(f)
        for i in rank.keys():
                hourlyRank.setdefault(i, []).append(rank[i])
    
    msg = ''
    for key, val in hourlyRank.items():
        keymax = max(val)
        keymin = min(val)
        maxi = val.index(max(val))
        mini = val.index(min(val))
        if (keymax - keymin >= 20 and mini > maxi and timestamp == timeline[mini]):
            msg += 'Rank of '+key+' has raised from '+str(keymax)+' ('+timeline[maxi]+') to '+str(keymin)+' ('+timeline[mini]+')\n'
    if (msg != ''):
        sendEmail2(['xiangnan.g12@gmail.com'], msg)
        #print msg
    shutil.rmtree("./data/rawdata/")
    os.makedirs("./data/rawdata/")
