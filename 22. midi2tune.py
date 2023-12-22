from ruamel.yaml import YAML, CommentedMap
from ruamel.yaml.comments import CommentedSeq as CS
from getopt import getopt
from sys import argv, exit
from os import getcwd
from naming_mtds import *
from pathlib import Path
yaml=YAML()
yaml.default_flow_style = None
import music21


#plusminus: 当有两个八度时，倾向于+还是-？ 0：-，1：+
plusminus = 1
#firstBeat: 弱起小节的处理，0：第一个音同时或之前响第一下，第一拍非重拍；1：从弱起小节的开头响第一下；2：弱起小节后一小节再响第一下
#注意：打谱时，弱起的小节也要留够完整的时值，比如4/4拍，弱起小节也要留够4拍
firstBeat = 0
name = '001'
directory = Path("./puzzles/")
opts, args = getopt(argv[1:], "hp:f:n:d:", ["help", "plusminus=", "firstbeat=", "name=", "dir="])
helpdoc = """
midi2tune -n <name> [-p <plusminus>] [-f <firstbeat>] [-d <directory>]
or: midi2tune --name=<name> [--plusminus=<plusminus>] [--firstbeat=<firstbeat>] [-dir=<directory>]
    从 <directory>/midi/<name>.mid 读取midi文件，生成 <directory>/unhandled/<name>.yml
    -p, --plusminus: 1则优先使用+，
                     0则优先使用-，
        缺省优先使用+
    -f, --firstbeat: 0则第一个音同时或之前响第一下，第一拍非重拍；
                     1则从弱起小节的开头响第一下；
                     2则弱起小节后一小节再响第一下
        缺省为0
    -d, --dir: 指定目录，缺省为./puzzles/。请确保midi和unhandled文件夹存在
"""
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print(helpdoc)
        exit()
    elif opt in ("-p", "--plusminus"):
        plusminus = int(arg)
    elif opt in ("-f", "--firstbeat"):
        firstBeat = int(arg)
    elif opt in ("-n", "--name"):
        name = arg
    elif opt in ("-d", "--dir"):
        directory = Path(arg)

# music21.defaults.quantizationQuarterLengthDivisors = (8, 3)
mid_name = str(directory/'midi'/(name+'.mid'))
mid = music21.converter.parse(mid_name, quantizePost=False)
# music21.configure.run()
# print(dir(mid))

numerator = 4
denominator = 4
bpm = 120
key_signature = 'C'

def pitch2num(pitch):
    return music21.pitch.Pitch(pitch).pitchClass


info = mid.parts
notes = []
# measures = []
alterPitch = 0
tune = []
num2simp = {
    'C': '1',
    'D': '2',
    'E': '3',
    'F': '4',
    'G': '5',
    'A': '6',
    'B': '7'
}
octs = set()
# info.show('text')
# info.id = 'containingStream'
offset = 0
info = info.stream()
for el in info.recurse():
    if isinstance(el, music21.stream.Measure):
        offset = el.offset
        # continue
    # print(el)
    elif isinstance(el, music21.tempo.MetronomeMark):
        bpm = el.number
        print('bpm:', bpm)
    elif isinstance(el, music21.meter.TimeSignature):
        numerator = el.numerator
        denominator = el.denominator
        print('time signature:', numerator, '/', denominator)
    elif isinstance(el, music21.key.Key):
        key_signature = el.tonicPitchNameWithCase
        print('key signature:', key_signature)
    elif isinstance(el, music21.note.Note):
        alterPitch = pitch2num(key_signature)
        notes.append([el.pitch.transpose(-alterPitch).nameWithOctave, offset+el.offset])
        octs.add(int(notes[-1][0][-1]))
        # print(notes[-1])
    elif isinstance(el, music21.bar.Barline) and el.type == 'final':
        notes.append([0, offset+el.offset])

#first note too late
if notes[0][1] >= numerator:
    correction = notes[0][1] // numerator * numerator
    for x in notes:
        x[1] -= correction

# determine the metronome
delay = 0
strong = 0
if notes[0][1] != 0:
    if firstBeat == 0:
        early = numerator - notes[0][1]
        if early == int(early):
            strong = early
        else:
            delay = -(notes[0][1] % 1) * denominator
            strong = numerator - (notes[0][1] - notes[0][1] % 1)
    elif firstBeat == 1:
        delay = -notes[0][1] * denominator
    elif firstBeat == 2:
        delay = (numerator - notes[0][1]) * denominator
strong = int(strong)

metronome = [delay, int(16 / denominator), strong, numerator]


for i in range(len(notes)-1):
    notes[i][1] = (notes[i+1][1] - notes[i][1]) * denominator
notes.pop()

if len(key_signature) == 2:
    if key_signature[-1] == '+':
        # print('\'+\' used for sharp key_signature')
        key_signature = key_signature[0] + '#'
    elif key_signature[-1] == '-':
        # print('\'-\' used for flat key_signature')
        key_signature = key_signature[0] + 'b'

# print(notes)
# print(octs)
span = max(octs) - min(octs)
if span == 0:
    print('Only one octave! Cool')
# print(span)
oct4key = 0
if span > 2:
    print('error: too many octaves')
    exit(1)

for note in notes:
    simp = num2simp[note[0][0]]
    if len(note[0]) == 3:
        if note[0][1] == '#' or note[0][1] == '+':
            simp += '#'
        if note[0][1] == 'b' or note[0][1] == '-':
            simp += 'b'

    hilo = int(note[0][-1])
    if span == 0:
        hilo = ''
        oct4key = min(octs)
    elif span == 1:
        if plusminus == 0:
            oct4key = max(octs)
            hilo = '-' if hilo == min(octs) else ''
        else:
            oct4key = min(octs)
            hilo = '+' if hilo == max(octs) else ''
    else:
        oct4key = min(octs) + 1
        hilo = '-' if hilo == min(octs) else '+' if hilo == max(octs) else ''

    if hilo == '' and len(simp) == 1:
        simp = int(simp)
    else:
        simp = simp + hilo
    tune.append([simp, note[1]])

# print(oct4key)
# print(tune)
print('tune preview:')
[print(x) for x in tune]
print('metronome:', metronome)
result = CommentedMap()
result['tune'] = tune

result['tuneBeatDur'] = '15000/'+str(bpm)
# print(key_signature)
# print(oct4key)
result['tunePitchBase'] = key_signature+str(oct4key)
result['metronome'] = metronome

result['tuneRevealBeatDur'] = '15000/'+str(bpm)
result['tuneRevealOffset'] = '15000/'+str(bpm)+'*(0)'

# tunename = CommentedMap()
# tunename['title'] = ''
# tunename['author'] = ''
# tunename['desc'] = ''
# result['zh-Hans'] = tunename
# # result['en'] = tunename

# result['curator'] = None

result.yaml_set_comment_before_after_key('tuneBeatDur', before='\n')
result.yaml_set_comment_before_after_key('tuneRevealBeatDur', before='[等几拍敲第一下,每过几个时间单位敲一下,开头敲几下后是重拍,每几拍一个重拍]\n\n')
result.yaml_add_eol_comment('括号内填写多少个时间单位后开始钢琴窗第一个音','tuneRevealOffset', column=0)


tunename = """
zh-Hans:
  title:  （）
  author: ZUN
  desc:   《》。
# 示例：
# title: 门前的妖怪小姑娘（門前の妖怪小娘）
# desc:  《东方神灵庙》2面BOSS幽谷响子的主题曲。
en:
  title: a
  author: b
  desc: c


curator: zzz
"""

yml_file = directory/'unhandled'/(name+'.yml')
exist_rename(yml_file)
with open(yml_file, 'w', encoding='utf-8') as f:
    yaml.dump(result, f)
    f.write(tunename)
print('generated: '+str(yml_file))
