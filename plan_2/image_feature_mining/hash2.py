#!/usr/bin/python
#coding:utf-8
import glob
import os
import sys

from PIL import Image

EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'

def avhash(im):
    if not isinstance(im, Image.Image):
        im = Image.open(im)
    im = im.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, im.getdata()) / 64.
    #print len(map(lambda i: 0 if i < avg else 1, im.getdata()))
    #return reduce(lambda x, (y, z): x | (z << y),enumerate(map(lambda i: 0 if i < avg else 1, im.getdata())),0)
    List = map(lambda i: 0 if i < avg else 1, im.getdata())
    #print List
    return "".join([str(i) for i in List])

def hamming(h1, h2):
    h, d = 0, h1 ^ h2
    while d:
        h += 1
        d &= d - 1
    return h

def writeString(string,txtPath = 'out.txt'):
    #将String写入文件
    f = open(txtPath, "a+")
    line = f.write(string + '\n')
    f.close


if __name__ == '__main__':
    im, wd = "G:\\dev\\tianchi\\image_test\\7.jpg","F:\\TDDOWNLOAD\\tianchi_fm_img1_3"
    txtPath = "data.txt"
    #h = avhash(im)
    #print im,h
    os.chdir(wd)
    images = []
    for ext in EXTS:
        images.extend(glob.glob('*.%s' % ext))
    #seq = []
    prog = int(len(images) > 50 and sys.stdout.isatty())
    f = open(txtPath, "w")
    for f in images:
        string = " ".join([f.split(u".")[0],avhash(f)])
        #seq.append(string)
        writeString(string,txtPath)
        if prog:
            perc = 100. * prog / len(images)
            x = int(2 * perc / 5)
            print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
            print '%.2f%%' % perc, '(%d/%d)' % (prog, len(images)),
            sys.stdout.flush()
            prog += 1
    #print seq
    '''
    os.chdir(wd)
    images = []
    for ext in EXTS:
        images.extend(glob.glob('*.%s' % ext))
    #print images
    seq = []
    prog = int(len(images) > 50 and sys.stdout.isatty())
    print type(avhash(im))
    print '##'
    for f in images:
        print avhash(f),f
    for f in images:
        seq.append((f, hamming(avhash(f), h)))
        if prog:
            perc = 100. * prog / len(images)
            x = int(2 * perc / 5)
            print '\rCalculating... [' + '#' * x + ' ' * (40 - x) + ']',
            print '%.2f%%' % perc, '(%d/%d)' % (prog, len(images)),
            sys.stdout.flush()
            prog += 1

    if prog: print
    for f, ham in sorted(seq, key=lambda i: i[1]):
        print "%d\t%s" % (ham, f)
    '''