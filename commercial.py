from __future__ import print_function

import re

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
            try:
                v = int(r.group(2))
            except:
                v = vars[r.group(2)]
            vars[r.group(1)] = v
        elif i == 1:
            vars[r.group(2)] = r.group(1)
        elif i == 2:
            vars[r.group(1)] = int(input())
        elif i == 3:
            vars[r.group(1)] = input()
        elif i == 4:
            v = vars[r.group(1)]
            if isinstance(v, str):
                vars[r.group(1)] = chr(ord(vars[r.group(1)][0]) + ord(vars[r.group(2)][0]))
            else:
                vars[r.group(1)] += vars[r.group(2)]
        elif i == 5:
            v = vars[r.group(1)]
            if isinstance(v, str):
                vars[r.group(1)] = chr(ord(vars[r.group(1)][0]) - ord(vars[r.group(2)][0]))
            else:
                vars[r.group(1)] -= vars[r.group(2)]
        elif i == 6:
            print(vars[r.group(1)])
        elif i == 7:
            index = rindex(jumps, ln)
            if vars[r.group(1)] == 0:
                ln = jumps[index - 1] - 1
            else:
                ln = jumps[index + 1] - 1
        elif i == 8:
            break

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        s = f.read()
    com(s)
