import cv2
import numpy as np
import matplotlib.pyplot as plt

for image in range (60):
    
    filename = "0"*(3-len(str(image)))+str(image) + '.jpg'
    img = cv2.imread("A2/set 1/" + filename)

    img = cv2.resize(img, (1000, int(1000*img.shape[0]/img.shape[1])))

    #Converting image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Calculating threshold value for binarization
    max_val, min_val = np.max(gray), np.min(gray)
    T = (max_val - (max_val - min_val)/1.35)//255

    #Applying Otsu's thresholding method to binarize the image
    thresh = cv2.threshold(gray, T, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = cv2.bitwise_not(thresh, thresh)

    #Connected Components Analysis
    (numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(thresh,4,cv2.CV_32S)
    mask = np.zeros(gray.shape, dtype="uint8")

    # loop over the number of unique connected component labels
    lst_state=[]
    for i in range(0, numLabels):

        # extract the connected component statistics and centroid for the current label
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]

        # ensure the width, height, and area are all neither too small nor too big
        keepArea = area>40 and area < 6100 \
                and h>12 and w>3 and h<150 and w<100 and x>130 \
                and x<mask.shape[1]-100 and y>20 and y<mask.shape[0]-150
        # construct a mask for the current connected component by finding a pixels in the labels array that have the current connected component ID
        if keepArea:
            lst_state.append((x,y,h))
            # construct a mask for the current connected component and then take the bitwise OR with the mask
            componentMask = (labels == i).astype("uint8") * 255
            mask = cv2.bitwise_xor(mask, componentMask)
    
    cv2.imwrite("A2/diff/" + filename, mask)

    """
    Segmenting possible car plate areas using Horizontal projection
    """
    #Summing up the pixels in each row of the mask
    horizontal=np.sum(mask,axis=1)
    is_start = False
    horizontal_block = []
    start_x = 0
    end_x = 0
    i = 0
    while i < len(horizontal):
        if not is_start and horizontal[i]>0:
            is_start = True
            start_x = i
        elif is_start and horizontal[i]==0:
            is_start = False
            end_x = i
            horizontal_block.append((start_x,end_x))
        i+=1

    #Segments of the image obtained from horizontal projection
    horizontal_segments=[]
    #Coordinates of the segments
    horizontal_seg_coors=[]

    for block in horizontal_block:
        segment = mask[block[0]:block[1],:]
        horizontal_segments.append(segment)
        horizontal_seg_coors.append((block[0],block[1]))

    # # plot histogram with the mask and horizontal projection
    # fig, ax = plt.subplots(1, 2, figsize=(15, 5))
    # ax[0].imshow(mask, cmap="gray")
    # ax[1].plot(horizontal, range(len(horizontal)-1,-1,-1))
    # plt.show()

        
    """
    Segmenting possible car plate areas using Vertical projection on each segment obtained from horizontal projection
    """
    verticals=[]
    for segment in horizontal_segments:
        vertical_block = []
        vertical = np.sum(segment,axis=0)
        verticals.append(vertical)

    # # plot histograms with the segment and the vertical projection
    # fig, ax = plt.subplots(len(horizontal_segments), 2, figsize=(15, 5))
    # for k, segment in enumerate(horizontal_segments):
    #     ax[k][0].imshow(horizontal_segments[k], cmap="gray")
    #     ax[k][1].plot(verticals[k])
    # plt.show()

    #List of lists of tuples of start and end of each block in vertical projection
    all_ver = []

    for vertical in verticals:
        is_start = False
        vertical_block = []
        start_y = 0
        end_y = 0
        i = 0
        while i < len(vertical):
            if not is_start and vertical[i]>0:
                is_start = True
                start_y = i
            elif is_start and vertical[i]==0:
                is_start = False
                end_y = i
                vertical_block.append((start_y,end_y))
            i+=1
        all_ver.append(vertical_block)
    
    def join_blocks(block):
        """
        Joins vertical blocks that are close to each other
        """
        t = 90
        res = []
        i = 0
        start = block[0][0]
        end = block[0][1]
        #Keeps track of the number of troughs in the current detected interval
        count = 0
        while i < len(block)-1:
            if (block[i+1][0] - end) < t:
                end = block[i+1][1]
                count+=1
            else:
                res.append((count,start,end))
                start = block[i+1][0]
                end = block[i+1][1]
                count = 0
            i+=1
        res.append((count,start,end))
        return res
    
    """
    Determining the most probable car plate area
    """
    #Keeps track of the segment with the most number of troughs
    
    possible_car_plate = None
    for ver in range (len(all_ver)):
        #sort block based on number of troughs in the interval
        sorted_blck = sorted(join_blocks(all_ver[ver]),key=lambda x:x[0], reverse=True)
        
        if len(sorted_blck) > 0:
            for block in sorted_blck:
                #If we have not found a possible candidate yet, or the current segment has more troughs than the previous candidate and WHR is between 1 and 3.5
                if possible_car_plate == None \
                    or (possible_car_plate[0][0] < block[0] and block[0] < 10 and 1 < block[2]/block[1] < 3.5):
                    possible_car_plate = (block,horizontal_seg_coors[ver])
        
    
    localised = img[possible_car_plate[1][0]:possible_car_plate[1][1],possible_car_plate[0][1]:possible_car_plate[0][2]]
    # cv2.imwrite("A2/locs/" + filename, localised)



    