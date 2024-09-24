import time
import psutil
from git import Repo
import subprocess
import ctypes

PATH_OF_GIT_REPO = r'...\.git' # Your git repo path here.
PATH_OF_EXE = r'...\XXX.exe' # Your program to be executed here.
NAME_OF_PROCESS = 'Logseq' # The process name here.
COMMIT_MESSAGE = 'auto commit'

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
    pids = psutil.pids()
    while my_pid == -1:
        for pid in pids:
            try:
                proc = psutil.Process(pid)
            except Exception:
                continue
            if NAME_OF_PROCESS in proc.name():
                my_pid = pid
                print(proc.name())
                break

    # Loop until can't find this pid
    while True:
        try:
            proc = psutil.Process(my_pid)
        except Exception:
            break

    # print('Git pushing...')
    git_push()
