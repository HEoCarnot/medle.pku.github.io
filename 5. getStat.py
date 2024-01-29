from naming_mtds import *
from pathlib import Path
import stat

local_folder = Path('./puzzles/server/')
remote_folder = Path('/home/lighthouse/fantasyguide/medle/medle.pku.github.io-master/puzzles/')

with SFTPConnection() as sftp:
    files = sftp.listdir_attr(remote_folder.as_posix())
    for f in files:
        if stat.S_ISDIR(f.st_mode) or ".yml" not in f.filename:
            continue
        remote_file = remote_folder / f.filename
        local_file = local_folder / f.filename
        print(f'Downloading {f.filename}')
        sftp.get(remote_file.as_posix(), str(local_file))