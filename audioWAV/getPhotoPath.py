__author__ = 'eleanor.cui'
import json
import csv

def write_photo_path_inJSON(testDict,filePath):
    fp= open(filePath,'w+')
    fp.write(testDict)
    fp.close()
def load_photo_path_inJSON(filePath):
    #fp=open(filePath,'r')
    #s=json.load(file(filePath))
    fp=open(filePath,'r')
    s=json.dumps(fp.read())
    fp.close()
    return s

def write_photo_path_inCSV(filePath,lineContents):
    fp=open(filePath,'a')
    csvWriter=csv.writer(fp,dialect='excel')
    csvWriter.writerow(lineContents)
    fp.close()

def load_photo_path_inCSV(filePath):
    fp=file(filePath,'rU')
    reader=csv.DictReader(fp)
    caseList=[]
    for row in reader:
        # print row['CaseNumber'],row['ExpectedPath'],row['ActualPath']
        # print row
        caseList.append(row)
    # print caseList[0]['CaseNumber']
    fp.close()
    return caseList

if __name__ == '__main__':
    testDict='{"case":001,"expected":"test/source/actual.JPG","actual":"test/source/actual.JPG"}'
    filePath='my.json'
    #write_photo_path_inJSON(testDict,filePath)
    #s=load_photo_path_inJSON(filePath)
    #print s
    caseList = load_photo_path_inCSV('filePath.csv')


