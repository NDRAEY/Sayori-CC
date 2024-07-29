# Code by NDRAEY (c) 2023

import shutil
import os
import subprocess as sp
from colorama import Fore

# internal
try:
    import colored_out as log
except:
    from . import colored_out as log

class CCompiler:
    def __init__(self, compiler=None):
        self.__supported = (
            'clang',
            *['clang-'+str(i) for i in range(12, 16)],
            'gcc',
            *['gcc-'+str(i) for i in range(10, 13)]
        )

        self.__path = None
        self.found = False

        if not compiler:
            for i in self.__supported:
                self.__path = shutil.which(i)
                if self.__path is not None:
                    break

            if self.__path is None:
                log.error("No suitable compiler found!")
                log.info("Tried: ")
                for i in self.__supported:
                    log.info("^-", i)
            else:
                self.found = True
                log.success("Found compiler:", self.__path.split("/")[-1], "["+self.__parse_compiler_version()+"]")
        else:
            if shutil.which(compiler):
                self.__path = shutil.which(compiler)
                log.success("Using compiler:", compiler, "["+self.__parse_compiler_version()+"]")
                self.found = True
            else:
                log.error(f"Compiler {compiler} was not found!")

    def __parse_compiler_version(self):
        # !!!: Not tested on GCC
        process = sp.Popen([
            self.__path, "--version"
        ], stdout=sp.PIPE)
        
        out = process.stdout.read().split(b"\n")[0]
        return out.split(b" ")[2].decode("utf-8")

    def compile_file(self, infile, outfile, flags=""):
        if not os.path.isfile(infile):
            log.error("File", infile, "was not found!")
            return 1

        log.check("Compiling", Fore.GREEN + infile + Fore.RESET)
        
        code = sp.call([
            self.__path, infile, *(flags.split(" ")), "-o", outfile
        ], stdout=sp.PIPE)

        if code:  # Non-zero code indicates an error
            log.error("Failed to compile:", infile)

        return code

'''
compiler = CCompiler()
compiler.compile_file("main.c", "main", "-O3")
'''
