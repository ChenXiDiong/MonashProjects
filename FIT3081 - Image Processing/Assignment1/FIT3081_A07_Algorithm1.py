import cv2
import imutils

for i in range (60):
    filename = "0"*(3-len(str(i)))+str(i) + '.jpg'
    image = cv2.imread("A2/set 1/" + filename)
    image = imutils.resize(image, width=500)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    gray_image = cv2.convertScaleAbs(gray_image, alpha=1.5, beta=0) 
    edged = cv2.Canny(gray_image, 100, 200) 
    cnts,new = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    for c in cnts:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
        x,y,w,h = cv2.boundingRect(c)
        if len(approx) == 4 and cv2.isContourConvex(approx) and cv2.contourArea(approx) > 1500 and w/h > 0.5 and w/h < 4.5:
            new_img=image[y:y+h,x:x+w]
            cv2.imwrite("A2/locs/"+filename,new_img)
            break