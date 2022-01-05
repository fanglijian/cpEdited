# coding:utf-8

import os,os.path
import sys
import getopt
import shutil

_PRJ_DIR = r'/home/dev/code/gw/8030FPGA'

_OUT_DIR = r'/home/dev/share/src'

_GIT_CMD = r'git status -s'

def _del_files(dir):
    for root, _, files in os.walk(dir):
        for name in files:
            os.remove(os.path.join(root, name))

def _del_dirs(dir):
    _del_files(dir)
    for root, dirs, _ in os.walk(dir, topdown = False):
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def _usage():
    print("CPEDITED [cp|clean]")
    print("\t-p : project dir")
    print("\t-d : destination dir\n")
    sys.exit(1)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:d:", ["project", "dest"])
    except getopt.GetoptError as err:
        print(err)
        _usage()
    for o,v in opts:
        if o == '-p' or o == '--project':
            if not os.path.exists(v):
                print('NOT EXIST:' + v)
                sys.exit(1)
            _PRJ_DIR = v
        elif o == '-d' or o == '--dest':
            if not os.path.exists(v):
                print('NOT EXIST:' + v)
                sys.exit(1)
            _OUT_DIR = v
    for a in args:
        if 'clean' == a:
            _del_dirs(_OUT_DIR)
            sys.exit(0)
        elif 'cp' != a:
            _usage()

    _del_files(_OUT_DIR)
    os.chdir(_PRJ_DIR)
    stream = os.popen(_GIT_CMD)
    output = stream.read()
    if None == output:
        sys.exit(1)
    lines = output.split("\n")
    for line in lines:
        ll = line.strip().split(" ")
        if len(ll) != 2:
            continue
        fp = ll[1]
        dl = fp.split(os.path.sep)
        if len(dl) > 1:
            cd = _OUT_DIR
            for i in range(len(dl) - 1):
                cd = os.path.join(cd, dl[i])
                if not os.path.exists(cd):
                    os.mkdir(cd)
        src = os.path.join(_PRJ_DIR, fp)
        dst =  os.path.join(_OUT_DIR, fp)
        shutil.copyfile(src, dst)
