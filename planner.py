import numpy as np
import argparse


def vi(MDP):
    n = MDP[0] 
    a_len = MDP[1]
    T = MDP[2]
    R = MDP[3]
    #print(T)
    discount = MDP[4]
    Vold = np.zeros(n)
    Q = np.zeros((n,a_len))
    Vnew = 10000000000*(Vold+1)
    #print(Vnew)
    action=(np.zeros(n)-1)
    for s in range(n):
        while(abs(Vnew[s]-Vold[s])>1e-15):
            for s2 in range(n):
                for a in range(a_len):
                    sum1 = 0
                    for s3 in range(n):
                        #print(R[s2][a][s3])
                        sum1+= T[s2][a][s3]*(R[s2][a][s3]+ discount* Vold[s3])
                    Q[s2][a] = sum1

                max1 = max(Q[s2])
                action[s2] = np.argmax(Q[s2])
                #print (max1)
                Vold[s2] = Vnew[s2] 
                Vnew[s2] = max1
    

    return (Vnew,action)
    pass

parser = argparse.ArgumentParser()

parser.add_argument('--mdp')
parser.add_argument('--algorithm', default = 'vi')
parser.add_argument('--policy')

args = parser.parse_args()

# print(args.mdp)
# print(args.algorithm)
# print(args.policy)

with open (args.mdp) as mdpfile:

    # for line in mdpfile.readlines():
    #     print(line)

    lines = mdpfile.readlines()
    #print(lines)

    # for line in lines:
    #     print(line.strip())

    lines = list(map(str.strip,lines))
    #print(lines)

    numStates = int(lines[0].split()[1])
    numAction = int(lines[1].split()[1])
    end = list(map(int,lines[2].split()[1:]))
    #print(end)

    #transition = []
    transition = np.zeros((numStates,numAction,numStates))
    reward = np.zeros((numStates,numAction,numStates))
    i=3
    while(lines[i].split()[0]=="transition"):
        SAS = list(map(int, lines[i].split()[1:4]))
        TR = list(map(float, lines[i].split()[4:6]))
        #print(SAS)
        #print(TR)
        #SAS.append(TAR)
        #transition.append(SAS+TR)
        transition[SAS[0],SAS[1],SAS[2]] = TR[1]

        reward[SAS[0],SAS[1],SAS[2]] = TR[0]
        #reward[SAS[1],SAS[0],SAS[2]] = TR[0]
        i=i+1

    # print(transition)
    # print(reward)

    mdptype = lines[i].split()[1]
    i+=1
    discount = float(lines[i].split()[1])

    MDP = [numStates,numAction,transition,reward,discount,mdptype]

    output = vi(MDP)

    output = np.array(output)
    output = output.T

    for i in range(len(output)):
        for j in range(len(output[0])):
            print(output[i][j]," " ,end ="")
        print("")


    