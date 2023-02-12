# Code by NDRAEY (c) 2023

import colored_out as log
import subprocess as sp
import shutil
import os
from colorama import Fore

class Linker:
    def __init__(self, linker=None):
        self.__supported = (
            "ld.lld",  # Clang LLD
            *["ld.lld-"+str(i) for i in range(12, 16)],
            "ld",  # GNU LD
            *["ld-"+str(i) for i in range(10, 13)],
        )

        self.__path = None
        self.found = False

        if linker and shutil.which(linker):
            log.success("Using linker:", linker)
            self.found = True
        else:
            for i in self.__supported:
                if shutil.which(i):
                    self.found = True
                    self.__path = shutil.which(i)
                    log.success("Found linker:", i)
                    break

            if not self.found:
                log.error("Not suitable linker was found!")
                log.info("Tried:")
                for i in self.__supported:
                    log.info("^-", i)
                
    def link(self, inputs, output, flags=""):
        for i in inputs:
            if not os.path.isfile(i):
                log.error("File", i, "was not found!")
                return

        log.check("Linking to", Fore.GREEN+(output.split("/")[-1])+Fore.RESET)

        code = sp.call([
            self.__path, *(flags.split(" ")), "-o", output, *inputs
        ], stdout=sp.PIPE)

        if code:  # Non-zero code indicates an error
            log.error("Failed to link:", output)

        return code
