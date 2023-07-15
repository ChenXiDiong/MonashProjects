"""
Name: Chen Xi Diong
Student ID: 32722656

FIT3155 S1 2023 Assignment 3 - Question 2
"""
import sys
import numpy as np
import math

def simplex(numDecisionVariables, numConstraints, objective, lhs, rhs):
    #Vector of Cj
    Cj = np.concatenate([objective,np.zeros(numConstraints)])
    #Vector used for Dot Product
    dot_Cj = np.zeros(numConstraints)
    #Vector of Cj-Zj
    Cj_Zj = np.zeros(numDecisionVariables + numConstraints)
    #Vector of theta
    theta = np.zeros(len(rhs))
    #z value - to be returned
    z = 0
    #Optimal values of the decision variables - to be returned
    dv_vals = [0]*numDecisionVariables
    #Keeping track of which variables are currently in the LHS Matrix
    lhs_variables = [i for i in range(numDecisionVariables, numDecisionVariables+numConstraints)]

    while True:

        # print("Cj: " + str(Cj))
        # print("LHS: " + str(lhs))
        # print("RHS: " + str(rhs))

        #Calculating the z value
        z = np.dot(dot_Cj,rhs)

        # print("z value: " + str(z))

        #Variables for determining the maximum of Cj-Zj and its pointer
        CZ_max = -math.inf
        CZ_maxindex = 0
        #Computing Cj-Zj
        for j in range(numDecisionVariables + numConstraints):
            col_sum = 0
            for i in range(numConstraints):
                col_sum += dot_Cj[i] * lhs[i][j]

            Cj_Zj[j] = Cj[j] - col_sum
            if Cj_Zj[j] > CZ_max:
                CZ_max = Cj_Zj[j]
                CZ_maxindex = j

        # print("Cj - Zj: " + str(Cj_Zj))
        # print("max index: " + str(CZ_maxindex))

        if CZ_max <= 0:
            optimaldecisions = []
            for val in dv_vals:
                optimaldecisions.append(str(val))
            for i in range(len(lhs_variables)):
                index = lhs_variables[i]
                if index < numDecisionVariables:
                    optimaldecisions[index] = str(rhs[i])
            return optimaldecisions, z

        #Variables for determining the minimum of theta and its pointer
        theta_min = math.inf
        theta_minindex = 0
        #Computing theta
        for i in range(numConstraints):
            if lhs[i][CZ_maxindex] == 0:
                theta[i] = math.inf
            else:
                theta[i] = rhs[i]/lhs[i][CZ_maxindex]
                
            if theta[i] < theta_min and theta[i] > 0:
                theta_min = theta[i]
                theta_minindex = i

        # print("Theta: " + str(theta))
        # print("min index: " + str(theta_minindex))

        #Updating decision variables
        if CZ_maxindex < numDecisionVariables:
            dv_vals[CZ_maxindex] = rhs[theta_minindex]

        # print("Current decision variables: " + str(dv_vals))

        #Update the row of leaving variable into entering variable
        lhs_variables[theta_minindex] = CZ_maxindex
        rhs[theta_minindex] /= lhs[theta_minindex][CZ_maxindex]
        lhs[theta_minindex] /= lhs[theta_minindex][CZ_maxindex]

        # print("Non-basic variables: " + str(lhs_variables))

        # print("LHS after swap: " + str(lhs))
        # print("RHS after swap: " + str(rhs))

        #Update the remaining rows of LHSMatrix and RHSVector
        for i in range(numConstraints):
            if i == theta_minindex:
                continue
            rhs[i] -= lhs[i][CZ_maxindex]*rhs[theta_minindex]
            lhs[i] -= lhs[i][CZ_maxindex]*lhs[theta_minindex]

        # print("updated LHS: " + str(lhs))
        # print("updated RHS: " + str(rhs))

        #Update dot product vector
        dot_Cj[theta_minindex] = Cj[CZ_maxindex]

        # print("updated dot cj: " + str(dot_Cj))

        

if __name__ == "__main__":
    _, filename = sys.argv
    f = open(filename,"r")

    #numDecisionVariables
    f.readline() 
    numDecisionVariables = int(f.readline())

    #numConstraints
    f.readline()
    numConstraints = int(f.readline())

    #objective
    f.readline()
    objectiveCoefs = np.zeros(numDecisionVariables)
    nums = f.readline().split(", ", maxsplit=numDecisionVariables-1)
    for i in range(numDecisionVariables):
        objectiveCoefs[i] = int(nums[i])

    #constraintsLHSMatrix
    f.readline()
    LHSMatrix = np.zeros((numConstraints,numDecisionVariables+numConstraints))
    for i in range(numConstraints):
        nums = f.readline().split(", ", maxsplit=numDecisionVariables-1)
        for j in range(len(nums)):
            LHSMatrix[i][j] = nums[j]
        LHSMatrix[i][i+numDecisionVariables] = 1
        
    #constraintsRHSVector
    f.readline()
    RHSVector = np.zeros(numConstraints)
    for i in range(numConstraints):
        RHSVector[i] = int(f.readline())

    f.close()

    dv, res = simplex(numDecisionVariables, numConstraints, objectiveCoefs, LHSMatrix, RHSVector)

    f = open("lpsolution.txt", "w")
    f.write("# optimalDecisions\n")
    s = ", "
    f.write(s.join(dv))
    f.write("\n# optimalObjective\n")
    f.write(str(res))



        
