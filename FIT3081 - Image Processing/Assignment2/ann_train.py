import numpy as np
import cv2

class Neural_Network:
    def __init__(self,Input_Neurons, Hidden_Neurons, Output_Neurons):
        """
        Step 1: Initialization of the Weights and Biases
        Initializing of the Weights. Random float number between -0.5 to 0.5 for weights.
        """
        np.random.seed(1)
        self.wji= np.random.uniform(-0.5, 0.5, size=(Hidden_Neurons, Input_Neurons))
        self.wkj = np.random.uniform(-0.5, 0.5, size=(Output_Neurons, Hidden_Neurons))
        self.bias_j = np.random.uniform(0, 1, size=(Hidden_Neurons, 1))
        self.bias_k = np.random.uniform(0, 1, size=(Output_Neurons, 1))

    
    def Read_Files(self):
        """
        Step 2: Reading of Training Files, and Target Files
        """
        training_files = []
        outputs = []
        #Reads 160 training images (80% of the dataset)
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
                training_files.append(np.array(file).flatten())
                #one hot encode the outputs
                outputs.append(np.eye(20)[(j-1)%20])

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


    def Saving_Weights_Bias(self,filename="weights"):
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

if __name__ == "__main__":
    nn=Neural_Network(1024,100,20)
    inputs, outputs = nn.Read_Files()
    epochs = 5000
    threshold = 0.001
    for i in range(epochs):
        E_total = nn.Training_Neural_Network(inputs, outputs,learn_rate=0.5)
        print("Total Error: " + str(E_total) + " | Epoch: " + str(i))
        if E_total < threshold:
            print("Complete")
            break

    print("Global Error: " + str(E_total)) 