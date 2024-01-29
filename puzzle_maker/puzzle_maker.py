from ruamel.yaml import YAML
from getopt import getopt
from sys import argv
yaml=YAML()
yaml.default_flow_style = None
# import os

# mode=1: fold some of the notes
# mode=2: fold completely as guided by your guidance
# mode=3: 

mode = 1
name = '001'
directory = "./puzzles/"
opts, args = getopt(argv[1:], "hm:n:d:", ["help", "mode=", "name=", "dir="])
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print('puzzle_maker -n <name> [-m <mode>] [-d <directory>]')
        print('or: puzzle_maker --name=<name> [--mode=<mode>] [-dir=<directory>]')
        print('defaults:')
        print('  name: 001')
        print('  mode: 1')
        print('  directory: ./puzzles/')
        exit()
    elif opt in ("-m", "--mode"):
        mode = int(arg)
    elif opt in ("-n", "--name"):
        name = arg
    elif opt in ("-d", "--dir"):
        directory = arg

unhandled = directory+name+"u.yml"
handled = directory+name+".yml"

try:
    with open(unhandled, encoding='utf-8') as f:
        result = yaml.load(f.read().replace('\t', ' '))
        utune = result['tune']
except FileNotFoundError as f:
    print(f)
    exit(5)


def findEntry(register, x):
    for i in range(len(register)):
        if register[i][0] == x:
            return i
    return -1

def calcOffset(tune, i, j):
    # 要求i<j
    if i<j:
        return sum([tune[k][1] for k in range(i, j)])
    return -sum([tune[k][1] for k in range(j, i)])

def checkValid(tune):
    # 寄存器：register[i] 形如 [重复音符的标号,重复音符的音,第一个的下标,第二个...]
    register = []
    for i in range(len(tune)):
        x = tune[i]
        if len(x) > 3:
            # too long
            return 1, i
        if len(x) == 3:
            entry = findEntry(register, x[-1])
            if entry == -1:
                register.append([x[-1], x[0], i])
            else:
                if register[entry][1] != x[0]:
                    # conflict
                    return 3, (register[entry][2], i)
                register[entry].append(i)
                # tune[i].append(0) # 表明不是第一次出现
        if len(x) < 2:
            # too short
            return 2, i
            

    return 0, register

def getIndex(flag, x): #有可能这是最后一个音
    try:
        j = flag.index(x)
        return j
    except ValueError:
        return len(flag)


a = checkValid(utune)
if a[0] == 1:
    print('Too long at '+str(a[1]))
    exit(1)
if a[0] == 3:
    print('Conflict at '+str(a[1]))
    exit(3)
if a[0] == 2:
    print('Too short at '+str(a[1]))
    exit(2)

flag = [0] * len(utune) # 如果这个音符写过了，则置1
register = a[1]
tune = []
if mode == 1:
    entries = [x[2] for x in register] # 重复音符第一次出现的位置
    for i in range(len(utune)):
        if flag[i]:
            continue
        if i not in entries: #普通的无重复音符
            # 接到下一个，注意要跳过可能的重复音符
            flag[i] = 1
            # offset = tune[i][1]
            j = getIndex(flag, 0)

            offset = calcOffset(utune, i, j)

            tune.append([utune[i][0], offset])
        elif i in entries:
            # 重复音符的第一个入口
            flag[i] = 1
            posnotes = register[findEntry(register, utune[i][-1])]
            note = [utune[i][0]]
            # 先无脑多读几个
            for j in range(2, len(posnotes)-1):
                flag[posnotes[j]] = 1
                note.append(calcOffset(utune, posnotes[j], posnotes[j+1]))
            # 然后寻找之前这个该回到哪，可能要向前，也可能要向后
            flag[posnotes[-1]] = 1
            # print(i, flag)
            j = getIndex(flag, 0)
            if j != -1 and j < posnotes[-1]: #前面仍有未写音符，需向前
                offset = -calcOffset(utune, j, posnotes[-1])
                note.append(offset)
            else: #前面没有未写音符，应向后写
                offset = calcOffset(utune, posnotes[-1], j)
                note.append(offset)

            tune.append(note)

elif mode == 2:
    # print(utune)
    for x in utune:
        if len(x) != 3:
            # print(x)
            print('Length incorrect at '+str(utune.index(x)))
            exit(4)

    register.sort(key=lambda x: x[0])
    if register[0][2] != 0:
        print('First note not at first postion')
        exit(5)
    for i in range(len(register)):
        posnotes = register[i]
        note = [posnotes[1]]
        for j in range(2, len(posnotes)-1):
            note.append(calcOffset(utune, posnotes[j], posnotes[j+1]))
        if i != len(register)-1:
            note.append(calcOffset(utune, posnotes[-1], register[i+1][2]))
        else:
            # print(posnotes[-1], len(tune))
            note.append(calcOffset(utune, posnotes[-1], len(utune)))
            # print(note)
        tune.append(note)


            

# print(tune)

# strfyTune = [str(x) for x in tune]
# print(strfyTune)

# result['tune'] = strfyTune
# print(result['metronome'])
# print(type(result['tune']))

result['tune'] = tune
with open(handled, 'w', encoding='utf-8') as f:
    yaml.dump(result, f)
    
# print(utune)