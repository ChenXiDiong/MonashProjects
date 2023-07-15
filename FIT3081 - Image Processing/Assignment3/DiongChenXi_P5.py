"""
Name: Chen Xi Diong
Student ID: 32722656

S1 2023 FIT3081 Take Home Assessment - Program File for Experiment 5
"""
import numpy as np
from skimage.util import random_noise
from scipy.signal import convolve2d
import cv2

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


def Load_Weights_Bias(filename="DiongChenXi_Exp1_Weights.npz"):
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

Number_Dictionary = np.array(['1','2','4','7','8'])
Character_Dictionary = np.array(['D','G','J','L','P','S','T','U','X','Y'])
numbering = np.array(['i','j'])
numbers = np.array([i+j for j in numbering for i in Number_Dictionary])
numbering = np.array(['9','10'])
characters = np.array([i+j for j in numbering for i in Character_Dictionary])


if __name__ == "__main__":
    testing_dataset = []
    for i in range(0, len(characters)-1, 10):
        testing_dataset += [number for number in numbers[i//2:i//2+5]]
        testing_dataset += [char for char in characters[i:i+10]]

    # Load the weights and bias
    wji, wkj, bias_j, bias_k = Load_Weights_Bias()

    # Testing the Neural Network
    dictionary = [1,2,4,7,8,'D','G','J','L','P','S','T','U','X','Y']
    outputs = []
    for test in testing_dataset:
        #read file
        file = cv2.imread(test + ".jpg")

        #add Gaussian noise with standard deviation of 1.0
        file = random_noise(file, mode='gaussian', seed = 91, mean=0, var=1.0)
        file = file.astype(np.uint8)

        #convert to grayscale
        file = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)

        #Remove noise using mean filter
        file = cv2.blur(file, (3,3))

        #Prepare the kernels for Sobel
        Kx = np.matrix('-1, -2, -1; 0, 0, 0; 1, 2, 1')
        Ky = np.matrix('-1, 0, 1; -2, 0, 2; -1, 0, 1')

        #Apply the Sobel operator
        Gx = convolve2d(file, Kx, mode='same')
        Gy = convolve2d(file, Ky, mode='same')
        G = np.sqrt(Gx**2 + Gy**2)
                
        #Clip range to 0-255
        G = np.clip(G, 0, 255)

        #Set Threshold as the highest 10% value in the array G
        T = np.percentile(G, 90)

        #If more than threshold, set as 1, else 0
        G[G < T] = 0
        G[G >= T] = 1
        
        G = np.array(G).flatten()

        net_j, out_j = Forward_Input_Hidden(G, wji, bias_j)
        net_k, out_k = Forward_Hidden_Output(out_j, wkj, bias_k)

        for k in range(len(out_k)):
            if out_k[k] == max(out_k):
                outputs.append((dictionary[k], out_k[k]))

    ans = [1,2,4,7,8,'D','G','J','L','P','S','T','U','X','Y',1,2,4,7,8,'D','G','J','L','P','S','T','U','X','Y']
    res = [out[0] for out in outputs]
    print(res)
    count = 0
    correct = []
    for i in range(len(ans)):
        if ans[i] == outputs[i][0]:
            count += 1
            correct.append((testing_dataset[i], outputs[i][1]))

    print("Accuracy of Training: ", count/len(ans))
    print("Correctly identified images: " + str(count))
    for c in correct:
        print(c[0], " (" + str(round(c[1][0],2)) + ")" )




