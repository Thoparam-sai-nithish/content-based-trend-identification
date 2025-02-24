import os
import time
import shutil

def rmRecur(directory_path):
        if os.path.exists(directory_path):
            time.sleep(2) 
            shutil.rmtree(directory_path)
            print(f"🚮 Deleted directory: {directory_path}")
