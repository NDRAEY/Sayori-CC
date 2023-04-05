# Sayori-CC
This is a wrapper for building programs for SayoriOS that allows compile programs in one command.

# How it works
1. It downloads latest release of [SayoriSDK](https://github.com/pimnik98/SayoriSDK)
2. It parses include.mk (from SDK) file for instructions for building
3. It compiles an app with custom settings, flags, and parameters.

In the end you will get executable that you can copy
to SayoriOS' initrd and run SayoriOS!

# Installation

Just run command to install a latest commit of Sayori-CC:
```bash
pip3 install https://github.com/NDRAEY/Sayori-CC/archive/main.zip
```

# Usage

Just run command to compile a file:
```bash
sayorios-cc myfile.c -o program.elf
```
