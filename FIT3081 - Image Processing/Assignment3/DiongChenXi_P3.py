"""
Name: Chen Xi Diong
Student ID: 32722656

S1 2023 FIT3081 Take Home Assessment - Program File for Experiment 2
"""
import numpy as np
import cv2
from scipy.signal import convolve2d

class Neural_Network:
    def __init__(self,Input_Neurons, Hidden_Neurons, Output_Neurons):
        """
        Step 1: Initialization of the Weights and Biases
        Initializing of the Weights. Random float number between -0.5 to 0.5 for weights.
        """
        seed_file = open("Seed Number.txt", "r")
        seed_value = seed_file.read()
        np.random.seed(int(seed_value))
        self.wji= np.random.uniform(-0.5, 0.5, size=(Hidden_Neurons, Input_Neurons))
        self.wkj = np.random.uniform(-0.5, 0.5, size=(Output_Neurons, Hidden_Neurons))
        self.bias_j = np.random.uniform(0, 1, size=(Hidden_Neurons, 1))
        self.bias_k = np.random.uniform(0, 1, size=(Output_Neurons, 1))

    
    def Read_Files(self, labels):
        """
        Step 2: Reading of Training Files, and Target Files
        """
        training_files = []
        outputs = []
        count = 0
        #Reads training images (80% of the dataset)
        for label in labels:
            #read file
            file = cv2.imread(label + ".jpg")
            
            #convert to grayscale
            file = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)

            #Prepare the kernels for Sobel
            Kx = np.matrix('-1, -2, -1; 0, 0, 0; 1, 2, 1')
            Ky = np.matrix('-1, 0, 1; -2, 0, 2; -1, 0, 1')

            #Apply the Sobel operator
            Gx = convolve2d(file, Kx, mode='same')
            Gy = convolve2d(file, Ky, mode='same')
            G = np.sqrt(Gx**2 + Gy**2)
                
            #Clip range to 0-255
            G = np.clip(G, 0, 255)

            #Resize the image from 784 pixels to 16 pixels
            G = resize_to_16(G)

            #Set Threshold as the highest 10% value in the array G
            T = np.percentile(G, 90)

            #If more than threshold, set as 1, else 0
            G[G < T] = 0
            G[G >= T] = 1
            
            # cv2.imwrite("image of " + label + ".jpg", G)

            training_files.append(np.array(G).flatten())

            #one hot encode the outputs
            outputs.append(np.eye(15)[count%15])

            count += 1

        return training_files, outputs

   
    def Forward_Input_Hidden(self,input_layer):
        """
        Step 3: Forward Propagation from Input -> Hidden Layer.
        Obtain the results at each neuron in the hidden layer.
        Calculate 𝑁𝑒𝑡_𝑗 and 𝑂𝑢𝑡_𝑗
        """
        # Calculate Net_j
        self.net_j = np.dot(self.wji, input_layer)
        # Calculate Out_j using an activation function like sigmoid
        self.out_j = 1/(1 + np.exp(-self.net_j - self.bias_j))

    
    def Forward_Hidden_Output(self):
        """
        Step 4: Forward Propagation from Hidden -> Output Layer.
        Forward Propagation from Hidden -> Output Layer.
        Calculate 𝑁𝑒𝑡_𝑘 and 𝑂𝑢𝑡_𝑘
        """
        # Calculate Net_k
        self.net_k = np.dot(self.wkj, self.out_j)
        # Calculate Out_k using an activation function like sigmoid
        self.out_k = 1/(1 + np.exp(-self.net_k - self.bias_k))

    
    def Error_Function(self,outputs):
        """
        Calculates the global error of the network.
        """
        out_k = self.out_k.flatten()
        outputs = outputs.flatten()
        # Calculate the total error.
        Error = 0.5 * (outputs - out_k) ** 2
        return np.sum(Error)

    
    def Check_for_End(E_total, num_iterations, threshold=0.001, max_iterations=1000):
        """
        Step 5: Check whether the total error is less than the error set by the user or the number of iterations is reached.
        returns true or false
        """
        return E_total < threshold or num_iterations > max_iterations

   
    def Weight_Bias_Correction_Output(self, outputs, learning_rate=0.01):
        """
        Step 6: Correction of Weights and Biases between Hidden and Output Layer.
        Calculate 𝑑𝑤𝑘𝑘𝑗 and 𝑑𝑏𝑘𝑘𝑗
        """
        # Calculating Correction of Weights between Hidden and Output Layer.
        self.delta_Etotal_Outk = -(outputs - self.out_k)
        self.delta_outk_Netk = self.out_k * (1 - self.out_k)
        self.delta_Netk_Wkj = np.tile(self.out_j.T, (len(self.wkj), 1))  # repeat out_j along rows
        self.dw_kj = learning_rate * self.delta_Etotal_Outk * self.delta_outk_Netk * self.delta_Netk_Wkj

        #To be used for calculation in the next step
        self.delta_k = self.delta_Etotal_Outk * self.delta_outk_Netk

        # Calculating Correction of Bias between Hidden and Output Layer
        self.db_k = learning_rate * self.delta_k

    
    def Weight_Bias_Correction_Hidden(self, inputs, learning_rate=0.01):
        """
        Step 7: Correction of Weights and Biases between Input and Hidden Layer.
        Calculate 𝑑𝑤𝑗𝑗𝑖 and 𝑑𝑏𝑗𝑗𝑖
        """
        # Calculating Correction of Weights and Bias between Input and Hidden Layer.
        self.delta_Etotal_Outj = np.dot(self.wkj.T, self.delta_k)
        self.delta_outj_Netj = self.out_j * (1 - self.out_j)
        self.delta_Netj_Wji = np.tile(inputs.T, (len(self.wji), 1))  # repeat inputs along rows
        self.dw_ji = learning_rate * self.delta_Etotal_Outj * self.delta_outj_Netj * self.delta_Netj_Wji

        # Calculating Correction of Bias between Hidden and Output Layer
        self.db_j = learning_rate * self.delta_Etotal_Outj * self.delta_outj_Netj

    
    def Weight_Bias_Update(self):
        """
        Step 8: Update the Weights and Biases
        Calculate 𝑤𝑘𝑘𝑗+ and 𝑏𝑘𝑘𝑗+
        Calculate 𝑤𝑗𝑗𝑖+ and 𝑏𝑗𝑗𝑖+
        """
        # Calculate 𝑤𝑘_𝑘𝑗+ and 𝑏𝑘_𝑘𝑗+
        self.wkj -= self.dw_kj
        self.bias_k -= self.db_k

        # Calculate 𝑤𝑗_𝑗𝑖+ and 𝑏𝑗_𝑗𝑖+
        self.wji -= self.dw_ji
        self.bias_j -= self.db_j


    def Saving_Weights_Bias(self,filename="DiongChenXi_Exp3_Weights"):
        """
        Step 10: Save the Weights and Biases
        Save 𝑤𝑘_𝑘𝑗 and 𝑏𝑘_𝑘𝑗
        Save 𝑤𝑗_𝑗𝑖 and 𝑏𝑗_𝑗𝑖
        """
        np.savez(filename, wji=self.wji, wkj=self.wkj, bias_j=self.bias_j, bias_k=self.bias_k)


    """
    Training the Neural Network
    """
    def Training_Neural_Network(self, inputs, outputs,learn_rate=0.01):
        E_total = 0
        for i in range(len(inputs)):
            inp=np.reshape(inputs[i],(len(inputs[i]),1))
            out=np.reshape(outputs[i],(len(outputs[i]),1))
            
            self.Forward_Input_Hidden(inp)
            self.Forward_Hidden_Output()
            E_total += self.Error_Function(out)
                
            self.Weight_Bias_Correction_Output(out, learn_rate)
            self.Weight_Bias_Correction_Hidden(inp, learn_rate)
            self.Weight_Bias_Update() 
        self.Saving_Weights_Bias()

        return E_total

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


def Load_Weights_Bias(filename="DiongChenXi_Exp3_Weights.npz"):
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

def resize_to_16(original):
    #784 = 28 x 28 and we want to resize to 16 = 4x4
    #Scan the image with a 7 x 7 window, and select the max value (max pooling)
    resized = np.zeros((4, 4))
    for i in range(0, 28, 7):
        for j in range(0, 28, 7):
            resized[int(i/7)][int(j/7)] = np.max(original[i:i+7, j:j+7])
    return resized

if __name__ == "__main__":
    #Prepare the training dataset
    Number_Dictionary = np.array(['1','2','4','7','8'])
    numbering = np.array(['a','b','c','d','e','f','g','h'])
    # #cross the two arrays to get 1a, 2a, 4c, ...
    numbers = np.array([i+j for j in numbering for i in Number_Dictionary])

    Character_Dictionary = np.array(['D','G','J','L','P','S','T','U','X','Y'])
    numbering = np.array(['1','2','3','4','5','6','7','8'])
    # #cross the two arrays to get D1, G1, J1, ...
    characters = np.array([i+j for j in numbering for i in Character_Dictionary])
    
    training_dataset = []
    for i in range(0, len(characters)-1, 10):
        training_dataset += [number for number in numbers[i//2:i//2+5]]
        training_dataset += [char for char in characters[i:i+10]]

    nn = Neural_Network(16, 100, 15)
    inputs, outputs = nn.Read_Files(training_dataset)

    # #Train the Neural Network
    epochs = 1000
    threshold = 0.001
    for i in range(epochs):
        E_total = nn.Training_Neural_Network(inputs, outputs,learn_rate=0.5)
        print("Total Error: " + str(E_total) + " | Epoch: " + str(i))
        if E_total < threshold:
            print("Complete")
            break

    print("Global Error: " + str(E_total)) 

    #Preparing the testing dataset
    numbering = np.array(['i','j'])
    numbers = np.array([i+j for j in numbering for i in Number_Dictionary])
    numbering = np.array(['9','10'])
    characters = np.array([i+j for j in numbering for i in Character_Dictionary])

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

        #convert to grayscale
        file = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)

        #Prepare the kernels for Sobel
        Kx = np.matrix('-1, -2, -1; 0, 0, 0; 1, 2, 1')
        Ky = np.matrix('-1, 0, 1; -2, 0, 2; -1, 0, 1')

        #Apply the Sobel operator
        Gx = convolve2d(file, Kx, mode='same')
        Gy = convolve2d(file, Ky, mode='same')
        G = np.sqrt(Gx**2 + Gy**2)
                
        #Clip range to 0-255
        G = np.clip(G, 0, 255)

        #Resize the image from 784 to 16 pixels
        G = resize_to_16(G)

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
        






        

    





