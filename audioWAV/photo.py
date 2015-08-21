__author__ = 'eleanor.cui'
import Image
import mergePhoto
import getPhotoPath

# class Photo:
#     def __init__(self):
#         self.caseNum=''
#         self.sourcePath=''
#         self.markPath=''
def get_result():
    sourceFP='filePath.csv'
    resultPath='test/0TEST/result/'
    opacity = 0.5
    caseList = getPhotoPath.load_photo_path_inCSV(sourceFP)
    for case in caseList:
        if case['ExpectedPath']=='':
            continue
        else:
            print case['ExpectedPath']
            print case['ActualPath']
            print case['CaseNumber']
            eImg=Image.open(case['ExpectedPath'])
            aImg=Image.open(case['ActualPath'])
            nImg=mergePhoto.composite_img_with_opacity(eImg,aImg,opacity)
            mergePhoto.save_image(nImg,resultPath,case['CaseNumber'])
            print case['CaseNumber']+'Completed'
    print'Done'

if __name__ == '__main__':
    get_result()