#!/usr/bin/python
import sys
from collections import defaultdict,Counter
from pprint import pprint
from functools import partial
import sys,re
from collections import Counter, defaultdict
from itertools import groupby
#from pgrules import isverbpat
pgPreps = 'in_favor_of|_|about|after|against|among|as|at|between|behind|by|for|from|in|into|of|on|upon|over|through|to|toward|towards|with|towarV in favour of	ruled in favour ofV in favour of	ruled in favour ofds|with'.split('|')
otherPreps ='out|down'.split('|')
verbpat = ('V; V n; V ord; V oneself; V adj; V -ing; V to v; V v; V that; V wh; V wh to v; V quote; '+\
              'V so; V not; V as if; V as though; V someway; V together; V as adj; V as to wh; V by amount; '+\
              'V amount; V by -ing; V in favour of n; V in favour of ing; V n in favour of n; V n in favour of ing; V n n; V n adj; V n -ing; V n to v; V n v n; V n that; '+\
              'V n wh; V n wh to v; V n quote; V n v-ed; V n someway; V n with together; '+\
              'V n as adj; V n into -ing; V adv; V and v').split('; ')
verbpat += ['V %s n' % prep for prep in pgPreps]+['V n %s n' % prep for prep in verbpat]
verbpat += [pat.replace('V ', 'V-ed ') for pat in verbpat]
nounpat = ('N for n to v; N from n that; N from n to v; N from n for n; N in favor of; N in favour of; '+\
            'N of amount; N of n as n; N of n to n; N of n with n; N on n for n; N on n to v'+\
            'N that; N to v; N to n that; N to n to v; N with n for n; N with n that; N with n to v').split('; ')
nounpat += nounpat + ['N %s -ing' % prep for prep in pgPreps ]
nounpat += nounpat + ['ADJ %s n' % prep for prep in pgPreps if prep != 'of']+ ['N %s -ing' % prep for prep in pgPreps]
adjpat = ('ADJ adj; ADJ and adj; ADJ as to wh; '+\
        'ADJ enough; ADJ enough for n; ADJ enough for n to v; ADJ enough n; '+\
        'ADJ enough n for n; ADJ enough n for n to v; ADJ enough n that; ADJ enough to v; '+\
        'ADJ for n to v; ADJ from n to n; ADJ in color; ADJ -ing; '+\
        'ADJ in n as n; ADJ in n from n; ADJ in n to n; ADJ in n with n; ADJ in n as n; ADJ n for n'+\
        'ADJ n to v; ADJ on n for n; ADJ on n to v; ADJ that; ADJ to v; ADJ to n for n; ADJ n for -ing'+\
        'ADJ wh; ADJ on n for n; ADJ on n to v; ADJ that; ADJ to v; ADJ to n for n; ADJ n for -ing').split('; ')
adjpat += [ 'ADJ %s n'%prep for prep in pgPreps ]
pgPatterns = verbpat + adjpat + nounpat
reservedWords = 'how wh; who wh; what wh; when wh; someway someway; together together; enoguh enough; amount amount; that that'.split('; ')
pronOBJ = ['me', 'us', 'you', 'him', 'them','her']

def isverbpat(pat):
    return  pat in verbpat
def isnounpat(pat):
    return  pat in nounpat
def isadjpat(pat):
    return  pat in adjpat

maxDegree = 9

def sentence_to_ngram(words, lemmas, tags, chunks): 
    return [ (k, k+degree) for k in range(1,len(words)) for degree in range(2, min(maxDegree, len(words)-k+1)) ]
    #                 if chunks[k][-1] in ['H-VP', 'H-NP', 'H-ADJP'] 
    #                 and chunks[k+degree-1][-1] in ['H-VP', 'H-NP', 'H-ADJP', 'H-ADVP'] ]

mapHead = dict( [('H-NP', 'N'), ('H-VP', 'V'), ('H-ADJP', 'ADJ'), ('H-ADVP', 'ADV'), ('H-VB', 'V')] )
#mapRest = dict( [('H-NP', 'n'), ('H-VP', 'v'), ('H-TO', 'to'), ('H-ADJ', 'adj'), ('H-ADV', 'adv')] )
mapRest = dict( [('VBG', 'ing'), ('VBD', 'v-ed'), ('VBN', 'v-ed'), ('VB', 'v'), ('NN', 'n'), ('NNS', 'n'), ('JJ', 'adj'), ('RB', 'adv'),
                    ('NP', 'n'), ('VP', 'v'), ('JP', 'adj'), ('ADJP', 'adj'), ('ADVP', 'adv'), ('SBAR', 'that')] )

mapRW = dict( [ pair.split() for pair in reservedWords ] )

def hasTwoObjs(tag, chunk):
    if chunk[-1] != 'H-NP': return False
    return (len(tag) > 1 and tag[0] in pronOBJ) or (len(tag) > 1 and 'DT' in tag[1:])
output = set()    
def chunk_to_element(words, lemmas, tags, chunks, i, isHead):
    #print ('***', i, words[i], lemmas[i], tags[i], chunks[i], isHead, tags[i][-1] == 'RP' and tags[i-1][-1][:2] == 'VB')
    if isHead:                                                          return mapHead[chunks[i][-1]] if chunks[i][-1] in mapHead else '*'
    if lemmas[i][0] == 'favour' and words[i-1][-1]=='in' and words[i+1][0]=='of': return 'favour'
    if tags[i][-1] == 'RP' and tags[i-1][-1][:2] == 'VB':                return '_'
    if tags[i][0][0] in ['W','R'] and lemmas[i][-1] in mapRW:                    return mapRW[lemmas[i][-1]]
    if tags[i][0]=='CD': return 'amount'
    if hasTwoObjs(tags[i], chunks[i]):                                              return 'n n'
    if tags[i][-1] in mapRest:                            return mapRest[tags[i][-1]]
    if tags[i][-1][:2] in mapRest:                        return mapRest[tags[i][-1][:2]]
    if chunks[i][-1] in mapHead:                            return mapHead[chunks[i][-1]].lower()
    if lemmas[i][-1] in pgPreps:                                         return lemmas[i][-1]
    return lemmas[i][-1]

def simplifyPat(pat): 
#     output.add(pat)
    if pat == 'V ,':
        return 'V'
    elif pat =='N ,':
        return 'N'
    elif pat =='J ,':
        return 'ADJ'
    else:
        return pat.replace(' _', '').replace('_', ' ').replace('  ', ' ')

def ngram_to_pat(words, lemmas, tags, chunks, start, end):
    pat, doneHead = [], False
    for i in range(start, end):
        isHead = tags[i][-1][0] in ['V','J','N'] and not doneHead
        pat.append( chunk_to_element(words, lemmas, tags, chunks, i, isHead) )
        if isHead: doneHead = True
    pat = simplifyPat(' '.join(pat))
    #print ('===', start, end, pat, words[start:end])
    return pat if isverbpat(pat) or isnounpat(pat) or isadjpat(pat) else ''

def ngram_to_head(words, lemmas, tags, chunks, start, end):
    for i in range(start, end):
        # if lemmas[i][-1].lower()+'-'+tags[i][-1][0] in akl_list:
        if tags[i][-1][0] in 'V' and tags[i+1][-1]=='RP':  return lemmas[i][-1].upper()+ ('_'+lemmas[i+1][-1].upper())
        if tags[i][-1][0] in ['V','N','J']:  return lemmas[i][-1].upper()
        # else: return ""
def output(test_pat,test_word):
    candidates = []
    for key,val in patternRec[test_pat].items():
    #     print(key+'\t'+str(len(val)))
        candidates.append((key,len(val)*(len(key.split())-1)**1.5))
    mean = sum([c[1] for c in candidates])/len(candidates)
    dev =pow(sum([pow(c[1]-mean,2) for c in candidates])/len(candidates),0.5)
    candidates = [c[0] for c in candidates if c[1]>mean+dev]
    for candidate in candidates:
        output = dict()
        for sent in  patternRec[test_pat][candidate]:
            words = sent.lower().split()
            if len(words)>20:
                continue
            cond1 = len([g for g in words if g not in firewords_list])
            cond2 = len([g for g in words if g in pron_list])
            score = 0
            if test_word in words:
                score = words.index(test_word) - cond1 - cond2
            else:
                for id, w in enumerate(words):
                    if test_word in w:
                        score = id - cond1 - cond2
            if len(words)>5 and len(words)<10:
                score += 10
            output[sent] = score
        gdex = max(output.keys(), key=lambda x: output[x])
        print(test_pat,len(patternRec[test_pat][candidate]),candidate,'\n',gdex)

NumReducer=32

if __name__ == '__main__':
    #fd = open('pat.txt','w')
    #lines = open('UM-Corpus.en.200k.tagged.txt','r').readlines()
    i=0

    for line in sys.stdin:
        i=i+1
        print('%d\t%s' % (i % NumReducer, line),end='')

