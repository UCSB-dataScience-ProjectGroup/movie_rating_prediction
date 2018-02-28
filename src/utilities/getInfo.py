import json
from utilities.SaveLoadJson import SaveLoadJson as SLJ
from utilities.LineCount import LineCount as LC

import subprocess

from geolite2 import geolite2

class getData:
    #Get Data Functions ------------------------------------------------------
    def getDATA(self):
        data = (self.getRequests()+'\t'+
                self.getTime()+'\t'+
                self.getUptime()+'\t'+
                self.getTemp()+'\t'+
                self.getIP())
        return data

    @staticmethod
    def getRequests():
        data = SLJ.load('dataStore.txt')
        return (str(data["totalRequests"])+'\t'+
                str(data["totalQueries"])+'\t'+
                str(data["totalAdjusts"]))
    
    @staticmethod
    def getTime():
        proc = subprocess.Popen(['uptime'],stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()
        return (str(out)[2:11] + '\t' +
                str(float(str(out).split(',')[4][:-3])*100)+'%')

    @staticmethod
    def getUptime():
        proc = subprocess.Popen(['uptime', '-p'],stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()
        return str(out)[2:-3]

    @staticmethod
    def getTemp():
        proc = subprocess.Popen(['vcgencmd', 'measure_temp'],stdout=subprocess.PIPE, shell=False)
        (out,err) = proc.communicate()
        return str(out)[7:-3]

    @staticmethod
    def getIP():
        proc = subprocess.Popen(['hostname', '-I'],stdout=subprocess.PIPE, shell=False)
        (out, err) = proc.communicate()
        return str(out)[2:-3]

    #Get Access Functions ---------------------------------------------------
    def getAccess(self):
        mostRecentIP = '0.0.0.0'
        mostRecentAcc = '[01/Jan/2000:00:00:00 -0800]'
        mostRecentSearch = 'NONE'        

        locations={"total":0}
        usLoc=dict()
        ips=dict()
        
        logFile = 'utilities/access.log'
        with open(logFile) as fp:
            for item in fp:
                line = item.split(';')
                if(len(line)>1):
                    if(line[2] == '200'):
                        if('GET /find' in line[3]):
                            reader = geolite2.reader()
                            match = reader.get(line[0])
                            if match['country']['iso_code'] not in locations:
                                locations[match['country']['iso_code']] = 1
                            else:
                                locations[match['country']['iso_code']]+=1
                            locations["total"]+=1
                            ips[line[0]]=1
                            if match['country']['iso_code'] == 'US':
                                usLoc[match['subdivisions'][0]['names']['en']]=1
                            mostRecentIP = line[0]
                            mostRecentAcc = str(line[1])
                            mostRecentSearch = (line[3].split(' ')[1][6:]).replace("%20"," ")
        #Format data
        locStr = ''
        usStr = ''
        totStr = 0
        for key, value in ips.items():
            totStr+=1
        totStr = str(totStr)
        for key, value in locations.items():
            if key != 'total':
                avg = (value/locations['total'])*100
                avg = '{0:0.2f}'.format(avg)
                locStr+=key+':'+str(avg)+';'
        for key, value in usLoc.items():
            usStr += key + ','
        result = str(mostRecentIP)+'\t'
        result+= str(mostRecentSearch)+'\t'
        result+= str(mostRecentAcc)+'\t'
        result+= str(totStr)+'\t'
        result+= str(locStr)[:-1]+'\t'
        result+= str(usStr)[:-1]
        return result
