import time
import psutil
from git import Repo
import subprocess
import ctypes

import json
import os

# Default values
default_config = {
    'PATH_OF_GIT_REPO': r'...\.git',  # Your git repo path here.
    'PATH_OF_EXE': r'...\XXX.exe',  # Your program to be executed here.
    'NAME_OF_PROCESS': 'Logseq',  # The process name here.
    'COMMIT_MESSAGE': 'auto commit'
}

# Try to load from JSON, use defaults if file doesn't exist or is invalid
config_file = 'config.json'
if os.path.exists(config_file):
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError:
        config = default_config
else:
    config = default_config

PATH_OF_GIT_REPO = config.get('PATH_OF_GIT_REPO', default_config['PATH_OF_GIT_REPO'])
PATH_OF_EXE = config.get('PATH_OF_EXE', default_config['PATH_OF_EXE'])
NAME_OF_PROCESS = config.get('NAME_OF_PROCESS', default_config['NAME_OF_PROCESS'])
COMMIT_MESSAGE = config.get('COMMIT_MESSAGE', default_config['COMMIT_MESSAGE'])

def git_pull():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.pull()
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, str(e), "Warning: Git Pull Failed", 1)

def git_push():
    try:
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(all=True)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, str(e), "Error: Git Push Failed", 1)


if __name__ == '__main__':
    # print('Git pulling...')
    git_pull()
    try:
        subprocess.Popen(PATH_OF_EXE)
    except Exception as e:
        ctypes.windll.user32.MessageBoxW(0, str(e), "Launch Logseq Failed", 1)
        exit(0)

    # Wait for logseq to quit
    my_pid = -1
    trial_count = 0
    max_trials = 10  # Set a limit for the number of trials
    while my_pid == -1 and trial_count < max_trials:
        time.sleep(1) # Add a small delay to avoid busy waiting
        pids = psutil.pids()
        for pid in pids:
            try:
                proc = psutil.Process(pid)
            except Exception:
                continue
            if NAME_OF_PROCESS in proc.name():
                my_pid = pid
                print(proc.name())
                break
        trial_count += 1

    if my_pid == -1:
        ctypes.windll.user32.MessageBoxW(0, "Process not found after too many trials.", "Warning: Process Not Found", 1)
        exit(0)
        

    # Loop until can't find this pid
    while True:
        try:
            proc = psutil.Process(my_pid)
            time.sleep(1)
        except Exception:
            break

    # print('Git pushing...')
    git_push()
