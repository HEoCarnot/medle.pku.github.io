import shutil
from datetime import datetime

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