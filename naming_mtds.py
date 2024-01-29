import shutil
from datetime import datetime
import os
import paramiko

def fmtedtime():
    now = datetime.now()
    return f"{now.strftime('%Y%m%d_%H%M%S')}_{now.microsecond:06d}"

def exist_rename(old_file, keep=''):
    if old_file.exists():
        # print('***********************')
        print('  *'+str(old_file) + ' exists!')
        now = datetime.now()
        new_name = old_file.stem + f".z{keep}{fmtedtime()}"+old_file.suffix
        new_file = old_file.parent/ '.backup' / new_name
        new_file.parent.mkdir(parents=True, exist_ok=True)
        old_file.rename(new_file)
        if keep:
            shutil.copy2(new_file, old_file)
        print('  *  renamed as '+str(new_file))
        print('  *********************')

class SFTPConnection:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        # 从环境变量中获取敏感信息
        private_key_path = os.getenv('SSH_PRIVATE_KEY_PATH')
        password = os.getenv('SSH_PASSWORD')
        hostname = os.getenv('FANTASY_HOSTNAME')

        print('connecting...')
        private_key = paramiko.RSAKey(filename=private_key_path, password=password)

        self.ssh.connect(hostname=hostname, username='root', pkey=private_key)
        self.sftp = self.ssh.open_sftp()
        print('  connected')

        return self.sftp

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sftp.close()
        self.ssh.close()
        print('disconnected')
        print('-----------------------')