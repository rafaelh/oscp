import re

file = open('access_log.txt')
for line in file:
    line = line.rstrip()
    x = re.findall(r'[^/]*.js\b',line)
if len(x) > 0:
    print(x)