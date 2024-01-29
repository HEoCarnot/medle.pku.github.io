with open(r'puzzles\unhandled\ed.html','r', encoding='utf-8') as f1: 
    a = [x for x in f1.readlines()]

a = [x.rstrip('\n') for x in a]
out = ''.join(a)
out = "\"" + out.replace('\"','\\\"') + "\""

with open('./ed.html','w', encoding='utf-8') as f2:
    f2.write(out)