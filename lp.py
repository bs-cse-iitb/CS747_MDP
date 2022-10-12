from pulp import * 
#import pulp
prob = LpProblem('GoingOnVacation', LpMaximize)

A = LpVariable('Car A', cat = LpInteger)
B = LpVariable('Car B', cat=LpInteger)

#Objective Function
prob += 20000*A + 45000*B , 'Objective Function'

print(prob)

prob += 4*A + 5*B <= 30 , 'Designer Constraint'
prob += 3*A + 6*B <=30, 'Engineer Constraint'
prob += 2*A + 7*B <=30, 'Machine Constraint'

print(prob)

print("Current Status: ", LpStatus[prob.status])
prob.solve()

print(A.varValue)
print(B.varValue)
print(value(prob.objective))

print("Current Status: ", LpStatus[prob.status])