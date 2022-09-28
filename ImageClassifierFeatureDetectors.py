import numpy as np
import cv2
import os

#Import Imaages
path = 'ImageQuery'
orb = cv2.ORB_create(nfeatures = 1000)
images = []
classNames = []
myList = os.listdir(path)
print(myList)
print('Total Classes Detected', len(myList))

for cl in myList:
    #Use 0 for gray scale images
    imgCur = cv2.imread(f'{path}/{cl}',0)
    images.append(imgCur)
    classNames.append(os.path.splittext(cl[0]))
print(classNames)

def findDes(images):
    desList = []
    for img in images:
        kp,des = orb.detectAndCompute(img,None)
        desList.append(des)
    return desList

def findID(img, des, thres=15):
    kp2,des2 = orb.detectAndCompute(img, None)
    bf = cv2.BDMatcher()
    matchList = []
    finalVal = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m,n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    #print(matchList)
    if len(matchList)!=0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))
    return finalVal

desList = findDes(images)
#Should print 2
print(len(desList))

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgOriginal = img2.copy()
    img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    id = indID(img2,desList)
    if id != -1:
        cv2.putText(imgOriginal, classNames[id], (50,50), cv2.FONT_hERSHEY_COMPLEX,1,(0,0,255),2)
    cv2.imshow('img2', imgOriginal)
    cv2.waitKey(1)



