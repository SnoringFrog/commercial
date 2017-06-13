from __future__ import print_function

#TODO: 
#better debugging options
#   more info for other functions
#       variables/values being operated on/examined
#   line numbers with each command
#   toggle debug via arg, not changing the interpreter

import re

debug = True # print debugging info
dp = "debug:" # debugging prefix

try:
    input = raw_input
except: pass

regexs = [
    re.compile(r"^\s*(\S+) now (\S+) dollars? off!\s*$"),
    re.compile(r'^\s*"([^"]*)" - Satisfied Consumer of (\S+)\s*$'),
    re.compile(r"^\s*(\S+) now sold at your local grocery store!\s*$"),
    re.compile(r"^\s*(\S+) now sold at your local drug store!\s*$"),
    re.compile(r"^\s*(\S+): made by the makers of (\S+)\s*$"),
    re.compile(r"^\s*(\S+) has shown much more positive feedback than other products, like (\S+)\s*$"),
    re.compile(r"^\s*(\S+) has been selling out worldwide!\s*$"),
    re.compile(r"^\s*Customers are jumping for joy for (\S+)!\s*$"),
    re.compile(r"^\s*HeadOn - Apply directly to the forehead\s*$"),
]

def rindex(l, e):
    last = -1
    for i, x in enumerate(l):
        if x == e:
            last = i
    return last

def com(code):
    code = code.split("\n")
    vars = {}
    jumps = [0]
    for ln, l in enumerate(code):
        if regexs[7].search(l):
            jumps.append(ln)
    jumps += [len(code) - 1]
    
    if debug:
        print("Jump locations:" + str(map(lambda x: x+1, jumps)))

    ln = -1
    while ln < len(code) - 1:
        ln += 1
        l = code[ln]
        last = None
        for i, r in enumerate(regexs):
            last = r.search(l)
            if last: break
        if not last:
            continue
        r = last
        if i == 0:
            if debug:
                print(dp+"assign int")

            try:
                v = int(r.group(2))
            except:
                v = vars[r.group(2)]
            vars[r.group(1)] = v
        elif i == 1:
            if debug:
                print(dp+"assign string")

            vars[r.group(2)] = r.group(1)
        elif i == 2:
            if debug:
                print(dp+"input int")

            vars[r.group(1)] = int(input())
        elif i == 3:
            if debug:
                print(dp+"input string")

            vars[r.group(1)] = input()
        elif i == 4:
            if debug:
                print(dp+"add")

            v = vars[r.group(1)]
            if isinstance(v, str):
                vars[r.group(1)] = chr(ord(vars[r.group(1)][0]) + ord(vars[r.group(2)][0]))
            else:
                vars[r.group(1)] += vars[r.group(2)]
        elif i == 5:
            if debug:
                print(dp+"subtract")

            v = vars[r.group(1)]
            if isinstance(v, str):
                vars[r.group(1)] = chr(ord(vars[r.group(1)][0]) - ord(vars[r.group(2)][0]))
            else:
                vars[r.group(1)] -= vars[r.group(2)]
        elif i == 6:
            if debug:
                print(dp+"output")

            print(vars[r.group(1)])
        elif i == 7:
            index = rindex(jumps, ln)
            if vars[r.group(1)] == 0:
                if debug:
                    print(dp+"jump back:"+str(jumps[index-1]+1)) #add one bc python's line numbers are 0-indexed

                ln = jumps[index - 1] - 1
            elif vars[r.group(1)] == 1:
                if debug:
                    print(dp+"jump forward:"+str(jumps[index+1]+1)) #add one bc python's line numbers are 0-indexed

                ln = jumps[index + 1] + 1
            else:
                if debug:
                    print(dp+"jump - no jump")
        elif i == 8:
            if debug:
                print("exit")
            break

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        s = f.read()
    com(s)
