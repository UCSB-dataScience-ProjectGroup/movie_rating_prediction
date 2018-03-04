import json
import os
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from utilities.LineCount import LineCount as LC

import subprocess

from geolite2 import geolite2

class getData:
    #Get Data Functions ------------------------------------------------------
    @staticmethod
    def getDATA():

        result = {"requests":{},
                  "time":'',
                  "cpuload":'',
                  "uptime":'',
                  "temp":'',
                  "ip":''}

        result["requests"]=getData.getRequests()
        time = getData.getTime().split('\t')
        result["time"] = time[0]
        result["cpuload"]=time[1]
        result["uptime"]=getData.getUptime()
        result["temp"]=getData.getTemp()
        result["ip"]=getData.getIP()
        return json.dumps(result)

    @staticmethod
    def getRequests():
        data = SLJ.load('dataStore.txt')
        return {"totalRequests":str(data["totalRequests"]),
                "totalQueries":str(data["totalQueries"]),
                "totalAdjusts":str(data["totalAdjusts"])}
    
    @staticmethod
    def getTime():
        proc = subprocess.Popen(['uptime'],stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()
        return (str(out)[1:9] + '\t' +
                str(float(str(out).split(',')[4])*100)+'%')

    @staticmethod
    def getUptime():
        proc = subprocess.Popen(['uptime', '-p'],stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()
        return str(out)

    @staticmethod
    def getTemp():
        proc = subprocess.Popen(['vcgencmd', 'measure_temp'],stdout=subprocess.PIPE, shell=False)
        (out,err) = proc.communicate()
        return str(out)[5:-1]

    @staticmethod
    def getIP():
        proc = subprocess.Popen(['hostname', '-I'],stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()
        return str(out)

    #Get Access Functions ---------------------------------------------------
    @staticmethod
    def getAccess():

        result={"Countries":dict(),
                "CountrySrs":dict(),
                "devices":dict(),
                "mostRecentSearch":'',
                "mostRecentAcc":'',
                "mostRecentIP":'',
                "recentSearches":[],
                "Users":0}

        lastNum = 200

        total=0
        mostRecentIP = ''
        mostRecentAcc = ''
        mostRecentSearch = ''
        Cname='Unknown'
        Sname='Unknown'
        Ctyname='Unknown'
        ips=dict()

        logFile = 'utilities/access.log'
        newFile='utilities/new.log'

        #f = open(newFile, 'w')
        with open(logFile, 'r') as lf:
            for temp in lf:
                line = temp.split(';')
                if len(line) > 1:
                    if line[2] == '200':
                        if 'GET /find' in line[3]:
                            #f.write(temp)
                            mostRecentIP=line[0]
                            mostRecentAcc=line[1]
                            
                            reader = geolite2.reader()
                            loc = reader.get(line[0])

                            Cname = loc['country']['names']['en']
                            if 'subdivisions' in loc:
                                Sname = loc['subdivisions'][0]['names']['en']
                            else:
                                Sname='Unknown'
                            if 'city' in loc:
                                Ctyname = loc['city']['names']['en']
                            else:
                                Ctyname='Unknown'
                            
                            if Cname not in result["Countries"]:
                                result["Countries"][Cname]=dict()
                                result["CountrySrs"][Cname]=0
                            if Sname not in result["Countries"][Cname]:
                                result["Countries"][Cname][Sname]=dict()
                            if Ctyname not in result["Countries"][Cname][Sname]:
                                result["Countries"][Cname][Sname][Ctyname] = []
                            result["CountrySrs"][Cname]+=1
                            total+=1

                            search = (line[3].split(' ')[1][6:]).replace('%20',' ')
                            mostRecentSearch=search
                            if search not in result["Countries"][Cname][Sname][Ctyname]:
                                result["Countries"][Cname][Sname][Ctyname].append(search)
                                if len(result["Countries"][Cname][Sname][Ctyname]) >= lastNum:
                                    result["Countries"][Cname][Sname][Ctyname].pop(0)

                            if search not in result["recentSearches"]:
                                result["recentSearches"].insert(0,search)
                                if len(result["recentSearches"]) >= lastNum:
                                    result["recentSearches"].pop(-1)

                            ips[line[0]]=1
                            device=(line[4].split('('))
                            if len(device)>1:
                                device=device[1]
                            else:
                                device="Unknown"
                            if device not in result["devices"]:
                                result["devices"][device]=0
                            result["devices"][device]+=1

        #f.close()

        #Most recent stuff
        result["mostRecentIP"]=mostRecentIP
        result["mostRecentAcc"]=mostRecentAcc
        result["mostRecentSearch"]=mostRecentSearch
        result["mostRecentLoc"]=str(Ctyname+', '+Sname+', '+Cname)

        #Unique Users
        for key, value in ips.items():
            result["Users"]+=1

        #Device percents
        for key, value in result["devices"].items():
            percnt = (float(value)/float(total))*100
            result["devices"][key]=format(percnt, '.2f')

        #Country percents
        for key, value in result["CountrySrs"].items():
            percnt = (float(value)/float(total))*100
            result["CountrySrs"][key]=format(percnt,'.2f')
            
        #os.system("sudo mv -f "+newFile+" "+logFile)
        return json.dumps(result)
