__author__ = 'Eleanor.cui'
import os
import shutil
def get_fileList(fPath,caseName):

    for root,dirs,files in os.walk(fPath+'\\'+caseName):
        print 'root:'
        print root
        print 'dirs:'
        print dirs
        for filespath in files:
            fileID=filespath[0:filespath.find('-')]
            if fileID!=caseName:
                file1=os.path.join(root,filespath)
                print file1
                newRoot=fPath+'\\'+fileID+root[root.rfind(caseName):].lstrip(caseName)
                newFile= os.path.join(newRoot,filespath)
                print newFile
                if os.path.isdir(newRoot):
                    shutil.copy(file1,newFile)
                    os.remove(file1)
                else:
                    os.makedirs(newRoot)
                    shutil.copy(file1,newFile)
                    os.remove(file1)

def get_incomingFileList(fPath,casName):
    for root,dirs,files in os.walk(os.path.join(fPath,caseName)):
        if 'Incoming' in root:
            for filespath in files:
                print filespath
                if '.ogg' in filespath:
                    #size=os.path.getsize(filespath)
                   # print size
                    print filespath


if __name__ == '__main__':
    fPath='\\\\cns-fileserver1\\Departments\\03 Englishtown WW\Blue Team\evc15loadtest\\testresult\\'
    caseName='20150831171920'
    #get_fileList(fPath,caseName)
    get_incomingFileList(fPath,caseName)