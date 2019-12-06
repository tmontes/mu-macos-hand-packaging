#!/usr/bin/env python3

import glob
import os
import shutil
import stat
import subprocess
import sys


SYSTEM_SAFE_PATHS = (
    '/System/',
    '/usr/lib/',
)

SHLIB_FILENAME_PATTERNS = (
    '*.dylib',
    '*.so',
)

LIB_TARGET_DIR = 'lib'


def basename(fname):
    return os.path.basename(fname)


def in_sys_safe_path(fname):
    for sys_safe_path in SYSTEM_SAFE_PATHS:
        if fname.startswith(sys_safe_path):
            return True
    return False


def non_system_safe_dep(binfile):
    output = subprocess.check_output(['otool', '-L', binfile]).decode('utf-8')
    for line in output.split('\n'):
        if line.endswith('is not an object file'):
            continue
        if line.endswith(':'):
            # first output line, containing full path to the binfile
            if basename(line.rstrip(':')) == basename(binfile):
                continue
        dep, _, _ = line.strip().partition(' ')
        if dep and not in_sys_safe_path(dep):
            if basename(dep) == basename(binfile):
                continue
            yield dep


def shlib_filenames(basedir):
    for pattern in SHLIB_FILENAME_PATTERNS:
        for name in glob.glob(f'{basedir}/**/{pattern}', recursive=True):
            yield name


def shlibs_needing_relink(basedir):
    for binfile in shlib_filenames(basedir):
        for dep in non_system_safe_dep(binfile):
            yield binfile, dep


def execs_needing_relink(basedir):
    for binfile in glob.glob(f'{basedir}/python3*'):
        for dep in non_system_safe_dep(binfile):
            yield binfile, dep


def main():

    local_dependencies = set(execs_needing_relink('./bin/'))
    local_dependencies.update(shlibs_needing_relink('./lib'))
    if not local_dependencies:
        return
        
    while local_dependencies:
        binfile, dep = local_dependencies.pop()
        dep_basename = basename(dep)
        dep_copy = os.path.join(LIB_TARGET_DIR, dep_basename)
        if not os.path.exists(dep_copy):
            print(f'Copying {dep!r} to {LIB_TARGET_DIR!r}.')
            shutil.copy(dep, LIB_TARGET_DIR)
        lib_mode = os.stat(binfile).st_mode
        os.chmod(binfile, lib_mode | stat.S_IWRITE)
        print(f'Relinking {binfile!r} to copied dependency.')
        subprocess.run([
            'install_name_tool',
            '-change',
            dep,
            f'@executable_path/../{LIB_TARGET_DIR}/{dep_basename}',
            binfile,
        ])
        os.chmod(binfile, lib_mode)
        for dep in non_system_safe_dep(dep_copy):
            local_dependencies.add((dep_copy, dep))


if __name__ == '__main__':

    main()
