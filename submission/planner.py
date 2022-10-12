from ast import main
import numpy as np
from pulp import * 
from pulp import PULP_CBC_CMD
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
    Vnew = Vold+1
    #print(Vnew)
    action=(np.zeros(n)-1)
    for s in range(n):
        while(abs(Vnew[s]-Vold[s])>1e-10):
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

def values(MDP,policy):
    S = MDP[0] 
    A = MDP[1]
    T = MDP[2]
    R = MDP[3]
    Y = MDP[4]
    
    
    # if (Y==1):
    #     Y=1-(1e-20)
    #print(T.shape)
    b = np.zeros((S))
    for s in range(S):
        sum1 = 0
        for s_ in range(S):
            sum1+=T[s][policy[s]][s_] * R[s][policy[s]][s_]
        b[s] = sum1

    identity = np.identity(S)
    #print(identity)

    A = np.zeros((S,S))

    for s in range(S):
        for s_ in range(S):
            A[s][s_]=T[s][policy[s]][s_]
    #print(A)


    A_ = identity - Y * A

    #print(A_)

    #print(b)
    V = np.dot(np.linalg.inv(A_), b)
    #print(V)
    return V
    pass

def hpi(MDP):
    S = MDP[0] 
    A = MDP[1]
    T = MDP[2]
    R = MDP[3]
    Y = MDP[4]

    Q = np.zeros((S,A))  

    #print(Q)

    # policy = np.zeros((S))
    # policy = policy.reshape((policy.shape[0],1))
    # print(policy.shape)
    policy = [0]* S

    while(True):
        V = values(MDP,policy)

        # for Q value
        for s in range(S):
            for a in range(A):
                sum = 0
                for s_ in range(S):
                    sum+= T[s][a][s_] * (R[s][a][s_] + Y * V[s_])
                Q[s][a] =sum
        
       #print(Q)

        flag = 0
        for s in range(S):
            if(np.argmax(Q[s])!= policy[s]):
                policy[s] = np.argmax(Q[s])
                flag = 1
        
        if (flag == 0 ) :
            break

    #print(policy)

    V = values(MDP,policy)
    return (V,policy)


def lp(MDP):
    S = MDP[0] 
    A = MDP[1]
    T = MDP[2]
    R = MDP[3]
    Y = MDP[4]
    problem = LpProblem('optimal_policy', LpMaximize)

    #Create Decision Variables:
    decision_variables = []
    for s in range(S):
        variable = str('s'+str(s))
        variable = LpVariable(str(variable))
        decision_variables.append(variable)       
    decision_variables = np.array(decision_variables)
    # wrong answer
    
    states = list(range(0, S))
    decision_variables = np.array(list(LpVariable.dicts("s",states).values()))
    
    #print(decision_variables)
    

    #Define Objective Function:
    total_value = ""
    for s in decision_variables:
    #for i, s in enumerate(decision_variables):
        total_value += s
    #print(total_value)

    #optamize functions
    problem+=(-1*total_value)


    #create constrains
    for i, s in enumerate(decision_variables):
        for a in range(A):

            # #for  in range(S):
            sum1=""
            for j, s_ in enumerate(decision_variables):
                TR = T[i][a][j] * R[i][a][j]
                TY = T[i][a][j] * Y
                #print(T[i][a][j] , R[s][a][j])
                #print(TY)
                sum1 += TR + TY * s_
                #print("Sum is ",sum1)
            #print("Total Sum is ",sum1)

            #bug take last value of s_
            problem+= s >= sum1

    #print(problem)
    #problem.writeLP("optimal_policy.lp" )

    #problem.solve()
    problem.solve(PULP_CBC_CMD(msg=0))
    #assert result == LpStatusOptimal

    #optimal values
    # V = []
    # for s in problem.variables():
    #     #print(s.varValue)
    #     V.append(s.varValue)

    V = np.zeros(len(decision_variables))
    for i in range(len(V)):
        V[i] = value(decision_variables[i])
    
    #Q Values
    Q = np.zeros((S,A))
    for s in range(S):
        for a in range(A):
            sum1 = 0
            for s_ in range(S):
                sum1+= T[s][a][s_] * (R[s][a][s_] + Y * V[s_])
            Q[s][a] =sum1
    
    policy = []
    for s in range(S):
        policy.append(int(np.argmax(Q[s])))
    
    return(V,policy)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('--mdp', required=True,type=str,help="MDP File", default=15)
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
        # if (discount==1):
        #     discount=1-(1e-10)
        MDP = [numStates,numAction,transition,reward,discount,mdptype]

    def print_output(output):
        for i in range(len(output[0])):
            print(output[0][i], int(output[1][i]))

        # output = np.array(output)
        # output = output.T

        # for i in range(len(output)):
        #     for j in range(len(output[0])):
        #         print(output[i][j]," " ,end ="")
        #     print("")
    #print(output)
    
    if args.algorithm == 'vi' and  not args.policy:
        print_output(vi(MDP))
    if args.algorithm == 'lp' and  not args.policy:
        print_output(lp(MDP))
    if args.algorithm == 'hpi' and  not args.policy:
        print_output(hpi(MDP))
    

    # change this
    policy_path = args.policy
    if(policy_path):
        with open(policy_path) as policy_file:
            lines = policy_file.readlines()
            #print(lines)
            lines = list(map(str.strip,lines))
            policy = list(map(int,lines))
            #print(policy)

        
        V = values(MDP,policy)
        for i in range(len(V)):
            print(V[i], policy[i])
            pass
