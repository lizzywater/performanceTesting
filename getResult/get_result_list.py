# -*- coding: utf-8 -*-
__author__ = 'Eleanor.cui'

import math
import os


def get_result_list_toTXT(fName):
    # os.system('get_result.bat 20150820154544 20150820154544.txt')
    # os.system('get_result.bat 20150821102632 20150821102632.txt')
    os.system('get_result.bat '+fName+' '+fName+'.txt')

def get_roomInfo_fromTXT(fPath,fName):
    f=open(fPath+fileName+'.txt','r')
    lines=f.readlines()
    f.close()
    tf=open(fPath+'re_'+fileName+'.csv','w+')
    i=0
    roomNum=0
    rooms=[]
    tf.write('Client Name, Data Category, Room, UserOfRoom\n')
    for line in lines:
        #print line
        #line.decode('gb2312').encode('utf-8')
        a='CNS'
        b='Incoming'
        c='Outgoing'
        if a in line and 'FILESERVER'not in line:
            index=line.find(a)
            #print line[index:]
            i+=1
            tf.write(line[index:])
        elif b in line:
            index=line.find(b)
            tf.write(' , '+line[index:])
        elif c in line:
            index=line.find(c)
            tf.write(' , '+line[index:])
        elif '.ogg' in line:
            # Verify file is belongs to current testing
            if line[line.find('2015'):line.rfind('-room')]==fName:
                # get room name
                start=line.rfind('room-')
                end=line.rfind('-user')
                start=line.find('-',start,end)
                #print line[start:end].lstrip('-')
                room=line[start:end].lstrip('-')
                # add room name to list
                rooms.append(room)
                # get participant name
                user=line[line.rfind('-'):line.rfind('.ogg')].lstrip('-')
                #print user
                if roomNum<int(room):
                    roomNum=int(room)
                tf.write(' , '+(fName[0:8]+'-'+fName[8:14])+' , '+room+', '+user+'\n')
            else:
                 continue
    tf.close()
    # caculate max participant number in one room
    maxParticipantNum=0
    for room in rooms:
        print 'roomName'+room
        print rooms.count(room)
        a=math.ceil(rooms.count(room)/2)
        if maxParticipantNum<a:
            maxParticipantNum=a
            print 'participantNumber:'
            print maxParticipantNum

    # return total num of tester and rooms
    print maxParticipantNum
    return i,(roomNum+1),maxParticipantNum

def get_result_report(filePath,caseID,testerNum,roomNum,testDetails):
    title = 'CaseID, #ofTester, #ofRoom, RoomType, Result, TestSummary, ManualTest, ServerCPU, ServerMemory\n'
    caseID=caseID[0:8]+'-'+caseID[8:14]
    f=open(filePath+'testingReport.csv','a+')
    lines=f.readlines()
    if len(lines)==0:
        f.write(title)

    f.write(caseID+', '+str(testerNum)+', '+str(roomNum)+', '+testDetails+'\n')
    f.close()

if __name__ == '__main__':
    fileName='20150831171920'
    filePath='D:/EF/EVC/performance testing/Testing result/'
    # get file info from sharing folder
    get_result_list_toTXT(fileName)
    # get details result
    testerNum,roomNum,participantNum=get_roomInfo_fromTXT(filePath,fileName)

    testRoomType='%d person/room'%participantNum
    testResult='Pass'
    testSummary='Audio:'+'accepted'\
    #             +';Video:'+'acceptable'
    #testSummary=''
    testManually='Reconnect: '+'never'\
                 +';Audio: '+'accepted'\
                 +';Video: '+'none'
    testServerCPU='50%'
    testServerMemory='6%'
    testDetails=testRoomType+', '+testResult+', '+testSummary+', '+testManually+', '+testServerCPU+', '+testServerMemory
    # get test summary result
    get_result_report(filePath,fileName,testerNum,roomNum,testDetails)
