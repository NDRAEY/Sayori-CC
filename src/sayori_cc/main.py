# Code by NDRAEY (c) 2023

import argparse
import shutil
import os
from pathlib import Path
import subprocess as sp

try:
    from c_compiler import CCompiler, log
    from git_utils import GIT
    from linker import Linker
except Exception as _:
    from .c_compiler import CCompiler, log
    from git_utils import GIT
    from .linker import Linker

VERSION = "1.0"

HOME_PATH        = str(Path.home())
SDK_DEFAULT_PATH = HOME_PATH+"/.SayoriSDK/"
SDK_C_PATH       = SDK_DEFAULT_PATH+"/libc/"
SDK_INCLUDE_MK   = SDK_C_PATH+"/Makefile"

SDK_CHANNELS = {
    'main': "https://github.com/pimnik98/SayoriSDK",
    'experimental': "https://github.com/NDRAEY/SayoriSDK"
}
DEFAULT_CHANNEL = "experimental"
SDK_REMOTE = SDK_CHANNELS[DEFAULT_CHANNEL]

def remove_directory(d):
    shutil.rmtree(d, ignore_errors=True)

def download_sdk_if_needed(channel=None):
    if os.path.isdir(SDK_DEFAULT_PATH):
        return True  # Already exists, check for updates

    channel = channel or DEFAULT_CHANNEL
    SDK_REMOTE = SDK_CHANNELS[channel]

    log.info("Selected channel:", channel)
    log.check("Downloading latest commit of SayoriSDK")
    error = GIT().clone(SDK_REMOTE, SDK_DEFAULT_PATH, depth=1)

    if error:
        log.error("Failed to download SayoriSDK!!!")
    else:
        log.success("Successfully downloaded SayoriSDK!")
        return True, True  # Downloaded, no need to update

    return error  # If other error, no check for updates

def update_sdk_if_needed():
    if not os.path.isdir(SDK_DEFAULT_PATH):
        return False

    log.check("Updating SayoriSDK")
    error = GIT().pull(SDK_DEFAULT_PATH)

    if error:
        log.error("Failed to update SayoriSDK!!!")
    else:
        log.success("Successfully updated SayoriSDK!")

    return error

def invoke_make():
    process = sp.Popen(["make", "-sC", SDK_C_PATH, "ext_compiler"], stdout=sp.PIPE)
    data = process.stdout.read().decode("utf-8").split("\n")

    flags = {}

    for i in data:
        if i == "":
            continue

        key, *value = i.split(" ")
        value = ' '.join(value)

        flags[key] = value

    return flags

def compile_c(inputs, output, compiler=None, linker=None, link=True):
    recipe = invoke_make()
    cflags = recipe.get("CFLAGS")
    libc = recipe.get("LIBC")

    if not cflags:
        log.error("Failed to get CFLAGS from make!")
        log.error("^- It may be corrupted")
    else:
        cflags = cflags.strip()
    
    c = CCompiler(compiler)
    if not c.found:
        exit(1)
    
    ld = Linker(linker)
    if not ld.found:
        exit(1)
    
    cwd = os.getcwd()

    print(cflags)

    objs = [cwd+"/"+i+".o" for i in inputs] 

    for i in inputs:
        error = c.compile_file(i, cwd + "/" + i + ".o", flags="-c " + cflags + f" -I{SDK_C_PATH}/include")
        if error:
            for i in objs:
                os.remove(i)
            exit(1)

    if link:
        os.chdir(SDK_C_PATH)
        ld.link(objs + [SDK_C_PATH + "/" + libc], cwd+"/"+output, f"-T{SDK_C_PATH}/link.ld")
        os.chdir(cwd)

        for i in objs:
            os.remove(i)

def main(args):
    if not args.files:
        log.warn("No files specified, just checking and updating SDK and exiting")

    if args.remove:
        remove_directory(SDK_DEFAULT_PATH)
        log.success("Successfully removed SayoriSDK!")
        exit(0)

    if args.download:
        remove_directory(SDK_DEFAULT_PATH)

    if (not args.output) and args.files:
        args.output = '.'.join(args.files[0].split("/")[-1].split(".")[:-1])

    res = download_sdk_if_needed(args.channel)
    if type(res) is not tuple and not args.no_updates:
        res = update_sdk_if_needed()

    if not args.files:
        exit(0)

    compile_c(args.files, args.output, args.compiler, args.linker, link=not args.c)

def premain():
    log.success(f"SayoriSDK Compiler Wrapper v{VERSION} by NDRAEY (c) 2023")

    print(invoke_make())

    argp = argparse.ArgumentParser(prog='sayori-cc')
    argp.add_argument("--channel", help="Select SayoriSDK channel")
    argp.add_argument("-c", action='store_true', help="Compile into object file only")
    argp.add_argument("-p", "--compiler", help="Select compiler to use for this session")
    argp.add_argument("-l", "--linker", help="Select linker to use for this session")
    argp.add_argument("-o", "--output", help="Output to file")
    argp.add_argument("-d", "--download", action='store_true',
                      help='''Force download SayoriSDK
                              (overwrites current channel)
                              (Useful when you want download another channel or re-download current)
                           '''
    )
    argp.add_argument("--remove", action='store_true', help="Remove SayoriSDK")
    argp.add_argument("-n", "--no-updates", action='store_true', help="Disable updates for this session")
    argp.add_argument("-q", "--quiet", action='store_true', help="Disables output except errors and information")
    argp.add_argument("files", nargs='*')

    args = argp.parse_args()

    print(args)

    main(args)

if __name__=="__main__":
    premain()

