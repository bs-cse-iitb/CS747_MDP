policy_path = "policy.txt"
with open(policy_path) as policy_file:
    lines = policy_file.readlines()
    print(lines)
    lines = list(map(str.strip,lines))
    policy = list(map(int,lines))
    print(policy)
