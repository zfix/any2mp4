from config import *
import subprocess as SP
import re
import logging
import sys
import os
import json


def newname(oldname):
    newfile = re.findall(regexpsearch, oldname)
    # newfile = re.findall(regexpsearch, oldname)[0]
    return newfile[0] + ".mp4"


def convert(filename):
    cmd = cmdtempl
    newfile = newname(filename)
    # check encoder and build full cmd array
    if "ffmpeg" == cmd[0]:
        cmd[2] = filename
    else:
        cmd[-3] = filename
    cmd[-1] = newfile
    proc = SP.Popen(cmd, stdout=SP.PIPE, stderr=SP.PIPE)
    print('Converting "%s" to "%s"' % (filename, newfile))
    res, err = proc.communicate()
    # check converting result
    if streamAnalyze(newfile):
        return True
    else:
        return False


def findfile(indir, srclist):
    cmd = "find %s -name *.%s -print" % (indir, inext)
    proc = SP.Popen(cmd.split(), stdout=SP.PIPE, stderr=SP.PIPE)
    res, err = proc.communicate()
    filelist = open(srclist, 'w')
    filelist.write(res)
    filelist.close()


def runTest(filename):
    """Running test media file"""
    cmd = cmdffp
    isfile = os.access(filename, os.F_OK)
    if isfile:
        cmd[-1] = '%s' % filename
        proc = SP.Popen(cmd, stdout=SP.PIPE, stderr=SP.PIPE)
        ffpout, ffperr = proc.communicate()
        return ffpout
    else:
        return '{}'


def streamAnalyze(filename):
    """Simple stream analyzer"""
    jarray = runTest(filename)
    d = json.loads(jarray)
    msg = False
    try:
        # converted file must have least 2 streams
        array = d['streams']
        if len(array) > 1:
            msg = True
    except KeyError:
        msg = False
    return msg


def main():
    try:
        indir = sys.argv[1]
        try:
            srclist = sys.argv[2]
        except KeyError:
            print('Using as file list %s' % srclist)
    except KeyError:
        print('Using as inputdir %s file list %s' % (indir,srclist))
    # Find all files for convert
    findfile(indir, srclist)
    infile = open(srclist, 'r')
    insrc = infile.readlines()
    infile.close()
    # COnvert each founded files
    for inp in insrc:
        log_file = open(logfile, 'a')
        filename = inp.strip('\n')
        # Check if conversion was ready
        srccheck = streamAnalyze(newname(filename))
        if srccheck:
            # if file was converted we can delete source file
            print('%s:"%s" Was converted\n' % (str(logging.time.time()), filename))
            log_file.write('%s:"%s" Was converted\n' % (str(logging.time.ctime()), filename))
            # try:
            #     os.unlink(filename)
            # except OSError:
            #     log_file.write('%s:"%s" OSError!\n' % (str(logging.time.ctime()), filename))
        else:
            # converting file to same name with ".mp4" extension
            print('"%s" Will convert' % filename)
            res = convert(filename)
            if res:
                # Check conversion result
                check = streamAnalyze(newname(filename))
                if check:
                    log_file.write('%s:"%s" Success\n' % (str(logging.time.ctime()), filename))
                    # os.unlink(filename)
                    log_file.write('%s:"%s" Deleted\n' % (str(logging.time.ctime()), filename))
                else:
                    log_file.write('%s:"%s" Failed\n' % (str(logging.time.ctime()), filename))
            else:
                log_file.write('%s:"%s" Failed\n' % (str(logging.time.ctime()), filename))
        log_file.close()


if __name__ == '__main__':
    main()