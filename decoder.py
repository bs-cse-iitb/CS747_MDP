import argparse
from email import policy
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("--value-policy")
parser.add_argument("--states")



args = parser.parse_args()



#print(args.value_policy)
with open(args.value_policy) as files:
    lines = files.readlines()
    #print(lines[1:])
    lines = list(map(str.strip,lines))

    value = []
    action = []
    for line in lines:
        line2 = line.split()
        value.append(float(line2[0]))
        action.append(int(line2[1]))

#print(value)
#print(action)


#print(args.states)
with open(args.states) as files:
    lines = files.readlines()
    #print(lines[1:])
    states = list(map(str.strip,lines))
    #states = list(map(int,lines))
#print(states)

#print(len(states))
#print(len(value))
#print(len(action))

runs = [0,1,2,4,6] 
for s in range(len(states)):
    print("{} {} {}".format(states[s],runs[action[s]],round(value[s],6)))