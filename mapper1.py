#!/usr/bin/env python
import os,sys,re
import shutil

for line in sys.stdin:
    line = line.split('\t')
    print("%s\t%s"%(line[0]+'#'+line[1],line[2]))