# -*- coding: utf-8 -*-
__author__ = 'Eleanor.cui'


import os
import codecs

def get_result_list_toTXT(fName):
    # os.system('get_result.bat 20150820154544 20150820154544.txt')
    # os.system('get_result.bat 20150821102632 20150821102632.txt')
    os.system('get_result.bat '+fName+' '+fName+'.txt')

def get_roomInfo_fromTXT(fPath,fName):
    f=open(fPath,'r')
    lines=f.readlines()
    for line in lines:
        #line.encode('utf-8')
        print line
        if 'CNSHHQ' in line:
            index=line.find('CNSHHQ')
            print line[index:]
        elif '.ogg' in line:
            start=line.find('room-')
            end=line.rfind('-user')
            print line[start:end]
    f.close()



if __name__ == '__main__':
    fileName='20150821152000'
    filePath='D:/EF/EVC/performance testing/Testing result/'+fileName+'.txt'
    # get_result_list_toTXT(fileName)
    get_roomInfo_fromTXT(filePath,fileName)