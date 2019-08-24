#!/usr/bin/env python
from operator import itemgetter
from itertools import groupby
import sys
from collections import Counter
def read_mapper_output(file, separator = '@'):
    for key in file:
        yield key.rstrip().split(separator, 1)

separator = '\t'
data = read_mapper_output(sys.stdin, separator =separator)

# fd=open('HiFreWords','r').readlines()
# firewords_list=[]
# pron_list=[]
# fd=open('prons.txt','r').readlines()

# for line in fd:
#     pron_list.extend(line.split())
# for line in fd:
#     firewords_list.extend(line.split())
redundant = ['me', 'us', 'you', 'him', 'them','her','I','you','she','they','my','he','his','their','your','we','our','ours','it','then','but','could','can','should','and','might','would','may','will','not','also','or']
for key, sents in groupby(data, itemgetter(0)):
    cnt = Counter()
    if len(key)>1:
        for sent in sents:
            if type(sent) == list and len(sent)==2:
                if all(s.isalpha() or s.isdigit() for s in sent[1].split()):
                    if any(s in redundant for s in sent[1].split()):
                        continue
                    if 'that' == sent[0].split()[-1] and len(sent[1].split()) == 2:
                        continue
                    if sent[1].islower():
                        cnt[sent[1]]+=1

        if sum(cnt.values()) > 20:
            num = len(key.split("#")[1].split())
            fine = 0
            out = '\t'.join(key.split("#"))
            candidates = []
            for common in cnt.most_common(10):
                if len(common[0].split()) < num*2+1:
                    # print("%s\t%s"%('\t'.join(key.split("#")),common))
                    candidates.append(common[0])
                    fine += 1
                if fine > 2:
                    out += '\t'+' | '.join(candidates)
                    print(out)
                    break

