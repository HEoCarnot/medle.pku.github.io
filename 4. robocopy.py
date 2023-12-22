import paramiko
from getopt import getopt
import os
from sys import argv
from os import getcwd
import subprocess
import shutil
import chardet
from pathlib import Path
from datetime import datetime

name = argv[1]
unzipflag = 0
directory = "./puzzles/"
opts, args = getopt(argv[2:], "um:d:r:", [])

zipexe = r'"D:\Program Files\7-Zip\7z.exe" '
ymlcom = r'e -ir!*.yml -o.\puzzles\ -y E:\Downloads\Compressed\069.zip'
mp3com = r'e -ir!*.mp3 -o.\puzzles\reveal -y E:\Downloads\Compressed\069.zip'
no_mp3 = 0

# 设置源文件路径和目标路径
source_folder = Path('./puzzles/')
source_folder_audio = source_folder / 'reveal'
target_folder = Path('/home/lighthouse/fantasyguide/medle/medle.pku.github.io-master/puzzles/')
target_folder_audio = target_folder / 'reveal'
yml_file = ''
mp3_file = ''

# 运行命令行命令，返回输出，如果返回值不为0，抛出异常
def runcom(com, mute=0):
    p = subprocess.Popen(com, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    stdout = p.stdout.read()
    encoding = chardet.detect(stdout)['encoding']
    stdout = stdout.decode(encoding)

    if not mute:
        print("DEBUG:\n"+stdout)
    if p.returncode != 0:
        raise Exception(stdout)
    return stdout

# def ok7z(out):
#     assert 'Everything is Ok' in out, out
# def okffmpeg(out):

# 如果文件存在，重命名
def exist_rename(old_file):
    if old_file.exists():
        # print('***********************')
        print('  *'+str(old_file) + ' exists!')
        now = datetime.now()
        new_name = old_file.stem + f".z{now.strftime('%Y%m%d_%H%M%S')}_{now.microsecond}"+old_file.suffix
        new_file = old_file.parent / new_name
        old_file.rename(new_file)
        print('  *  renamed as '+str(new_file))
        print('  *********************')
# 刷新文件名。
def refresh_name():
    global name
    global yml_file
    global mp3_file
    yml_file = source_folder / (name + '.yml')
    mp3_file = source_folder_audio / (name + '.mp3')


refresh_name()

# 获取命令行参数
for opt, arg in opts:
    if opt in ("-u", "--unzip"):
        unzipflag = 1
    elif opt in ("-d", "--dir"):
        directory = arg
    elif opt in ("-r", "--rename"):
        print('renaming')
        rename = arg
        new_yml_file = source_folder / (rename + '.yml')
        new_mp3_file = source_folder_audio / (rename + '.mp3')

        exist_rename(new_yml_file) #防止覆盖原文件
        exist_rename(new_mp3_file)
        yml_file.rename(new_yml_file)
        mp3_file.rename(new_mp3_file)
        shutil.copy2(new_yml_file, yml_file)
        shutil.copy2(new_mp3_file, mp3_file)
        name = rename
        print('  renamed as '+str(new_yml_file) + ' and ' + str(new_mp3_file))
        print('-----------------------')
        
        refresh_name()

# print(name)


        



# 解压文件
if unzipflag:
    print('unzipping')
    shortname = name.split('.')[0]
    old_yml_file = source_folder / (shortname + '.yml')
    old_mp3_file = source_folder_audio / (shortname + '.mp3')
    now = datetime.now()
    exist_rename(old_yml_file) #防止覆盖原文件
    # do the same for mp3
    exist_rename(old_mp3_file)

    zipcom = zipexe + ymlcom.replace('069.zip', name)
    runcom(zipcom, 1)
    zipcom = zipexe + mp3com.replace('069.zip', name)
    a = runcom(zipcom, 1)
    no_mp3 = "No files to process" in a
    zipcom = zipexe + mp3com.replace('069.zip', name).replace('mp3', 'wav') #可能使用wav
    
    runcom(zipcom, 1)
    name = name.split('.')[0]
    refresh_name()
    print('  unzipped')
    print('-----------------------')

# 如果解压存在wav，需要处理
wav_file = source_folder_audio / (name + '.wav')
if unzipflag and wav_file.exists():
    print('wav file found')
    if no_mp3:
        exist_rename(mp3_file)
        wav_file.rename(mp3_file)
        print('  wav file renamed')
    else: #如果存在mp3，则使用之
        print('  mp3 file exists, mp3 used instead')
    print('-----------------------')

# 查看MP3文件信息
mp3_path = str(mp3_file)
# print('audio info')
mp3info = runcom(['ffprobe', mp3_path, '-hide_banner'], 1)



mp3flag = 0
# print(mp3info)
streaminfo = [x for x in mp3info.split('\n') if "Stream" in x][0]
prompt = ['ffmpeg',
            '-y',
            '-i', mp3_path.replace('.mp3', 'u.mp3'),
            '-vn', 
            '-map_metadata',
            '-1', 
            '-c:a', 'libmp3lame',
            '-hide_banner',
            mp3_path]
print('normalizing')
# 检测是否需要转换格式、比特率
if "Audio: mp3" not in streaminfo:
    print('  *Not an mp3 file!')
    print('  *********************')

    mp3flag = 1
kbps = int([x for x in streaminfo.split(',') if "kb/s" in x][0].split(' ')[1])
if kbps > 128:
    print('  *bitrate > 128kbps!')
    print('  *********************')
    mp3flag = 1
if mp3flag:
    prompt.extend(['-b:a', '128k', '-f', 'mp3'])


shutil.move(mp3_path, mp3_path.replace('.mp3', 'u.mp3')) #先将源文件重命名
# print(subprocess.list2cmdline(['ffmpeg', '-i', mp3_path, '-vn', '-map-metadata','-1', '-ca', 'libmp3lame','-b:a128k', '-ext mp3', '-hide_banner',mp3_path]))
runcom(prompt, 1)
os.remove(mp3_path.replace('.mp3', 'u.mp3')) #删除源文件
print('  normalized')
print('-----------------------')
# exit()

# 文件上传
# 设置SSH连接参数
ssh = paramiko.SSHClient()

# 从环境变量中获取敏感信息
private_key_path = os.getenv('SSH_PRIVATE_KEY_PATH')
password = os.getenv('SSH_PASSWORD')
hostname = os.getenv('FANTASY_HOSTNAME')
print('uploading')
private_key = paramiko.RSAKey(filename=private_key_path, password=password)

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username='root', pkey=private_key)

target_yml_path = (target_folder / (name + '.yml')).as_posix()
target_mp3_path = (target_folder_audio / (name + '.mp3')).as_posix()
# 使用SFTP传输文件

sftp = ssh.open_sftp()
sftp.put(
    str(yml_file), 
    target_yml_path
)  # 目标文件名可以按需更改
sftp.put(
    str(mp3_file), 
    target_mp3_path
)  # 目标文件名可以按需更改
print('  uploaded succesfully')
print('    '+
    str(yml_file), 
    '\n---> ', target_yml_path,
)
print('    '+
    str(mp3_file), 
    '\n---> ', target_mp3_path
)
print('-----------------------')
sftp.close()

# 关闭SSH连接
ssh.close()
