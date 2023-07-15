import cv2
import numpy as np

"""
Segmenting the Characters in the Car Plate
"""
count=1
for image in range (1,11):
    
    filename = "Carplates/" + str(image)+ ".jpg"
    img = cv2.imread(filename)

    img = cv2.resize(img, (1000, int(1000*img.shape[0]/img.shape[1])))

    #Converting image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # gray=cv2.equalizeHist(gray)
    # erosion = cv2.erode(gray, None, iterations=2)
    # dilation = cv2.dilate(erosion, None, iterations=1)

    thresh = cv2.threshold(gray, 115, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    thresh=cv2.bitwise_not(thresh, thresh)
    analysis = cv2.connectedComponentsWithStats(thresh,4,cv2.CV_32S)
    (numLabels, labels, stats, centroids) = analysis

    # loop over the number of unique connected component labels
    lst_state=[]
    for i in range(0, numLabels):

        # extract the connected component statistics and centroid for
        # the current label
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]


        # ensure the width, height, and area are all neither too small
        # nor too big

        keepArea = h/w >1.2 and area > 100
        	# construct a mask for the current connected component by
        # finding a pixels in the labels array that have the current
        # connected component ID
        # ensure the connected component we are examining passes all
        # three tests
        if keepArea:
            lst_state.append((x,y,h,w))
    # print(lst_state)
    lst_state=sorted(lst_state, key=lambda x: x[0])
    
    
    for i in lst_state:
        newfile_name=str(count)+".jpg"
        x,y,h,w=i
        char=img[y:y+h,x:x+w]
        
        cv2.imwrite("Chars/" + newfile_name , char)
        count+=1


"""
Recognizing the Characters using the Neural Network
"""
def Forward_Input_Hidden(input_layer, wji, bias_j):
    # Forward Propagation from Input -> Hidden Layer.
    # Obtain the results at each neuron in the hidden layer.
    # Calculate 𝑁𝑒𝑡_𝑗 and 𝑂𝑢𝑡_𝑗
    net_j = np.zeros_like(bias_j)
    out_j = np.zeros_like(bias_j)

    for j in range(len(net_j)):
        for i in range(len(input_layer)):
            net_j[j] += wji[j][i] * input_layer[i]

    out_j = 1 / (1 + np.exp(-(net_j + bias_j)))

    return net_j, out_j

def Forward_Hidden_Output(out_j, wkj, bias_k):
    # Forward Propagation from Hidden -> Output Layer.
    # Calculate 𝑁𝑒𝑡_𝑘 and 𝑂𝑢𝑡_𝑘
    net_k = np.zeros_like(bias_k)
    out_k = np.zeros_like(bias_k)

    for k in range(len(net_k)):
        for j in range(len(out_j)):
            net_k[k] += wkj[k][j] * out_j[j]

    out_k = 1 / (1 + np.exp(-(net_k + bias_k)))

    return net_k, out_k

def Load_Weights_Bias(filename="weights.npz"):
    # Load the weights and bias from the file
    # The weights and bias are saved in a dictionary
    # The dictionary is saved in a .npz file
    # The dictionary contains the following keys:
    # wji, wkj, bias_j, bias_k
    # The values of each key is a numpy array
    data = np.load(filename)
    wji = data['wji']
    wkj = data['wkj']
    bias_j = data['bias_j']
    bias_k = data['bias_k']

    return wji, wkj, bias_j, bias_k

# Load the weights and bias
wji, wkj, bias_j, bias_k = Load_Weights_Bias()


# Testing the 10 Car Plates
dictionary = [0,1,2,3,4,5,6,7,8,9,'B','F','L','M','P','Q','T','U','V','W']
outputs = []
for i in range(1,70):
    #read file
    file = cv2.imread("Chars/" + str(i) + ".jpg")
    #resize file
    file = cv2.resize(file, (32,32))
    #convert to grayscale
    file = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
    #binarize using Otsu's method
    _, file = cv2.threshold(file, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    file = np.array(file).flatten()

    net_j, out_j = Forward_Input_Hidden(file, wji, bias_j)
    net_k, out_k = Forward_Hidden_Output(out_j, wkj, bias_k)

    for k in range(len(out_k)):
        if out_k[k] == max(out_k):
            outputs.append(dictionary[k])

ans = ['V','B','U',3,8,7,8,'V','B','T',2,5,9,7,'W','T','F',6,8,6,8,'P','L','W',7,9,6,9,'B','P','U',9,8,5,9,'B','M','T',8,6,2,8,'B','M','B',8,2,6,2,'P','P','V',7,4,2,2,'B','Q','P',8,1,8,9,'W','U','M',2,0,7]
print("Results from Neural Network: " + str(outputs))

# Calculate the accuracy
count = 0
for i in range(len(ans)):
    if ans[i] == outputs[i]:
        count += 1

print("Total correctly recognised characters: " + str(count))
print("Total number of car plate characters: " + str(len(ans)))
print("Accuracy of Car Plate Character Recognition: ", count/len(ans))