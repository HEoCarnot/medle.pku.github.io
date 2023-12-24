import paramiko
import os, sys
from pathlib import Path

# source_folder = Path('./puzzles/')
# source_folder_audio = source_folder / 'reveal'
target_folder = Path('/home/lighthouse/fantasyguide/medle/medle.pku.github.io-master/puzzles/')
target_folder_audio = target_folder / 'reveal'
name = sys.argv[1]

# yml_file = str(source_folder / (name + '.yml'))
# mp3_file = str(source_folder_audio / (name + '.mp3'))

target_yml_path = (target_folder / (name + '.yml')).as_posix()
target_mp3_path = (target_folder_audio / (name + '.mp3')).as_posix()

ssh = paramiko.SSHClient()

# 从环境变量中获取敏感信息
private_key_path = os.getenv('SSH_PRIVATE_KEY_PATH')
password = os.getenv('SSH_PASSWORD')
hostname = os.getenv('FANTASY_HOSTNAME')
print('connecting')
private_key = paramiko.RSAKey(filename=private_key_path, password=password)

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname, username='root', pkey=private_key)

def checkExistence(sftp, path):
    try:
        sftp.stat(path)
        return True
    except IOError:
        return False

# 使用SFTP传输文件

sftp = ssh.open_sftp()
if checkExistence(sftp, target_yml_path):
    print(f':){target_yml_path} exists')
else:
    print(f':({target_yml_path} does not exist')

if checkExistence(sftp, target_mp3_path):
    print(f':){target_mp3_path} exists')
else:
    print(f':({target_mp3_path} does not exist')
print('-----------------------')
sftp.close()

# 关闭SSH连接
ssh.close()
