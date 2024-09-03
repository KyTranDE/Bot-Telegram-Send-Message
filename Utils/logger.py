import os
import sys
from datetime import datetime
sys.path.append('../')
def get_time_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
def logger(path_log, text):
    os.makedirs(f'{"/".join(path_log.split("/")[:-1])}', exist_ok=True)
    with open(f'{path_log}', 'a+', encoding='utf-8') as f:
        f.write(str(text)+' - '+str(get_time_now()) + '\n')
        f.close()