import cv2
import numpy as np

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


# Testing the Neural Network
dictionary = [0,1,2,3,4,5,6,7,8,9,'B','F','L','M','P','Q','T','U','V','W']
outputs = []
#Reads 40 testing images (20% of the dataset)
for i in range(1,41):
    #read file
    file = cv2.imread("Test/T" + "0" * (3-len(str(i))) + str(i) + ".jpg")
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

ans = [0,1,2,3,4,5,6,7,8,9,'B','F','L','M','P','Q','T','U','V','W',0,1,2,3,4,5,6,7,8,9,'B','F','L','M','P','Q','T','U','V','W']
print(outputs)
count = 0
for i in range(len(ans)):
    if ans[i] == outputs[i]:
        count += 1

print("Total correctly identified images: " + str(count))
print("Total number of testing images: " + str(len(ans)))
print("Accuracy of Training: ", count/len(ans))

#Saving the outputs of the training set
failed_count = 0 #counts the number of images that failed the criterion
for i in range(0,141,20):
    for j in range(i+1, i+21):
        #read file
        file = cv2.imread("Train/A" + "0" * (3-len(str(j))) + str(j) + ".jpg")
        #resize the file to 32x32
        file = cv2.resize(file, (32,32))
        #convert to grayscale
        file = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
        #binarize using Otsu's method
        _, file = cv2.threshold(file, 0, 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        file = np.array(file).flatten()

        net_j, out_j = Forward_Input_Hidden(file, wji, bias_j)
        net_k, out_k = Forward_Hidden_Output(out_j, wkj, bias_k)

        f = open("output.txt", "a")
        out_k = out_k.flatten()
        f.write(str(out_k) + "\n")

        #Checking if any of the outputs fail the criterion
        for k in range(len(out_k)):
            if k == (j-1) % 20:
                if out_k[k] < 0.9:
                    failed_count += 1
                    print("Image " + str(j) + " failed the criterion")
            elif out_k[k] > 0.1:
                failed_count += 1
                print("Image " + str(j) + " failed the criterion")

f.close()
print("Total number of images that failed the criterion: " + str(failed_count))