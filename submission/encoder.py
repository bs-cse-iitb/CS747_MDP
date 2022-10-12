import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("--states", required=False,type=str,help="Number of States", default=15)
parser.add_argument("--parameters")
parser.add_argument("--q")


args = parser.parse_args()


#print(args.states)
#print(args.parameters)

with open(args.states) as files:
    lines = files.readlines()
    #print(lines[1:])
    states = list(map(str.strip,lines))
    #states = list(map(int,lines))

#print(states)



with open(args.parameters) as files:
    lines = files.readlines()
    #print(lines[1:])
    lines = list(map(str.strip,lines[1:]))

    runs_prob = []
    for line in lines:
        runs_prob.append(list(map(float,line[1:].split())))
    
    #print(runs_prob)


states.append('loss')
states.append('win')
S = len(states)
A = 5
gamma= 1

mdptype = 'episodic'

T = np.zeros((S,A,S))
R = np.zeros((S,A,S))



def next_state(s,run,player):

    if s==states.index('loss') :
        return [states.index('loss'),player]
    if s==states.index('win'):
        return [states.index('win'),player]
    #print(states[s])
    bb = int(states[s][:2])
    rr = int(states[s][2:])

    bb-=1
    if run == -1:
        return [states.index('loss'),player]
    if run in [0,2,4,6]:
        rr-=run

        # mistake rr instead of bb
        if bb%6==0:
            player =1-player
    if run in [1,3]:
        rr-=run
        if bb%6!=0:
            player =1-player

    if rr<=0:
        return [states.index('win'),player]
    else:
        if bb == 0:
            return [states.index('loss'),player]
    if bb<10:
        bb = '0'+ str(bb)
    if rr<10:
        rr = '0'+ str(rr)

    #print (bb,rr)
    state = str(bb)+str(rr)
    #print(state)
    s_ = states.index(state)
    return [s_,player]
    pass


action = [0,1,2,4,6]
runs = [-1,0,1,2,3,4,6]
q=float(args.q)
prob1 = [q,(1-q)/2,(1-q)/2]
run1 = [-1,0,1]



# new = next_state(100,6,player)
# print(new)
def player1(s,a,old, p):
    p2  = [p,p,p]
    #print("probability",p2)
    for r in run1:
        #print(r)
        p2[runs.index(r)]*=prob1[runs.index(r)]
        new = next_state(old[0],r,old[1]) 
        #
        # print(new)

        if(new[0]==states.index('loss')):
            T[s][a][new[0]]+=p2[runs.index(r)]
            pass
        elif(new[0]==states.index('win')):
            T[s][a][new[0]]+=p2[runs.index(r)]
            R[s][a][new[0]]=1
            pass
        elif(new[1]==0):
            T[s][a][new[0]]+=p2[runs.index(r)]
            pass
        else:
            #print("test")
            player1(s,a,new,p2[runs.index(r)])
            pass


        # if new[0]==states.index('loss'):
        #     T[s][a][new[0]]+=p2[runs.index(r)]
        # if new[0]==states.index('win'):
        #     T[s][a][new[0]]+=p2[runs.index(r)]
        #     R[s][a][new[0]]=1
        # # if r==-1:
        # #     T[s][a][new[0]]+=p2[runs.index(r)]

        # if new[1]==0 and r != -1:
        #     T[s][a][new[0]]+=p2[runs.index(r)]

        # if (new[1]==1 and r != -1):
        #     #print("States ",states[new[0]])
        #     #print("value" , states[new[1]][:2])

        #     p2 = [p2[runs.index(r)]]*3
        #     if(states[new[1]][:2]=='01'):
        #         if(int(states[new[1]][2:])==1 and r==1):
        #             T[s][a][states.index('win')]=p2[runs.index(r)]
        #         else:
        #             T[s][a][states.index('loss')]=p2[runs.index(r)]
        #         break     
            
        
        #     #return (new,p2[runs.index(r)])



 
player = 0 

for s in range(S-2):
    for a in range(A):
        for run in runs:
            new = next_state(s,run,player)
            #print(new)

            if(new[1]==1 and new[0] not in [states.index('win'),states.index('loss')]):
                #print("prob",runs_prob[a][runs.index(run)])

                player1(s,a,new,runs_prob[a][runs.index(run)]) 
                pass
            else:
                T[s][a][new[0]]+=runs_prob[a][runs.index(run)]
                if(new[0]==states.index('win')):
                    R[s][a][new[0]]=1
            
            #print(T)


for outcome in [-1,0,1,2,3,4,6]:
    new=next_state(states.index('0110'),outcome,0)
    #print(states[new[0]],new[1])
    #print("\n")
# print(S)
# print(A)


def generateMDP(S,A,gamma,mdptype):
    print("numStates",S)
    print("numActions",A)
    print("end",states.index('loss'),states.index('win'))
    for s in range(S):
        for a in range(A):
            for s_ in range(S):
                if T[s][a][s_]!=0:
                    print("transition {} {} {} {} {}".format(s,a,s_,R[s][a][s_],T[s][a][s_]))
    print("mdptype",mdptype)
    print("discount ",gamma)

generateMDP(S,A,gamma,mdptype)
    

#print(states.index('0809'))
#print(states[104])