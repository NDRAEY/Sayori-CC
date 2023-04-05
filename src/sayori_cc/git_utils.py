# Code by NDRAEY (c) 2023

import subprocess as sp
import shutil
import os

class GIT:
    def __init__(self):
        self.__path = shutil.which("git")

        if not self.__path:
            error("Git was not found!")
            return

    def clone(self, remote_repo, destination=None, depth=None):
        commands = [
            self.__path, "clone", remote_repo
        ]
        if destination:
            commands.append(destination)
        
        if depth:
            commands.append("--depth="+str(depth))
        
        return sp.call(commands)

    def pull(self, local_repo, remote="origin", branch="main"):
        commands = [
            self.__path, "pull", remote, branch
        ]

        cwd = os.getcwd()
        os.chdir(local_repo)

        res = sp.call(commands)
        
        os.chdir(cwd)

        return res

'''
git = GIT()
git.clone("https://github.com/pimnik98/SayoriOS", depth=1)
'''
