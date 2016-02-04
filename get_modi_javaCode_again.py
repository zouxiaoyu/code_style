# -*- encoding:utf-8 -*-
from __future__ import print_function
import io
import sys
import traceback
import re

def isMultiCmtStart(line):
    multi=line.rfind("/*")
    single=line.rfind("*/")
    double=line.find("//")
    multiStartFlag=False
    '''has /*'''
    if multi != -1:
        '''has no */ or */ is in front of /*'''
        if multi>single:
            '''has no // in this line'''
            if double == -1:
                multiStartFlag=True
            else:#has // in this line, but after /*'''
                if double>multi:
                    multiStartFlag=True
    return multiStartFlag

def isMultiCmtEnd(line):
    single=line.rfind("*/")
    if not isMultiCmtStart and single!=-1:
        return True

#use this function to make the comment display rationally
def cmtMakeup(code_piece):
    normal=''
    contbtwCmt=''
    strp=re.compile(r"\".*?\"")
    multiCmtEndp=re.compile(r"\*/(\w|\s)*$")
    code=code_piece.split('\n')
    multiCmtStart=False
    multiCmtEnd=False
    oriMultiFlag=False
    for line in code:
        line=line+'\n'
        s=re.sub(strp,'',line)
        ##########already has multiCmtStart
        if multiCmtStart:
            if multiCmtEndp.search(s):
                if normal:
                    print(normal,end="")
                    normal=''
                if line[0]=="+":
                    contbtwCmt+=line[1:]
                    if oriMultiFlag:
                        contbtwCmt='/*'+contbtwCmt
                        print(contbtwCmt,end="")
                        contbtwCmt=''
                        oriMultiFlag=False
                else:
                    if contbtwCmt:
                        if oriMultiFlag:
                            contbtwCmt='/*'+contbtwCmt+'*/\n'
                            oriMultiFlag=False
                        else:
                            contbtwCmt+='*/\n'
                        print(contbtwCmt,end="")
                        contbtwCmt=''
                multiCmtStart=False
        else:
            #this line contains a multiCmt start
            if isMultiCmtStart(s):
                multiCmtStart=True
                if line[0]=='+':
                    contbtwCmt+=line[1:]
                else:
                    oriMultiFlag=True
            else:
                '''a true */ without matched /*'''
                if isMultiCmtEnd(s):
                    if line[0]=='+':
                        normal='/*'+normal+line[1:]
                    else:
                        if normal:
                            normal='/*'+normal+'*/\n'
                    if normal:
                        print(normal,end="")
                        multiCmtStart=False
                        normal=""
                        oriMultiFlag=False
                else:
                    if line[0]=='+':
                        normal+=line[1:]

    if multiCmtStart:
        if normal:
            print(normal,end="")
        if contbtwCmt:
            if oriMultiFlag:
                contbtwCmt='/*'+contbtwCmt+'*/\n'
            else:
                contbtwCmt=contbtwCmt+'*/\n'
            print(contbtwCmt,end="")

#we only extract the modi java code(new added + modi) from the patch file
def get_modi_javaCode(patch_fin):
    try:
        diffFlag=0
        indexFlag=0
        linesFlag=0
        laterVer=''

        for line in patch_fin.readlines():
            try:
                fromp=re.compile(r'^From ')
                javaDiffp=re.compile(r'^diff.*.java')
                allDiffp=re.compile(r'^diff')
                indexp=re.compile(r'^index ')
                linesp=re.compile(r'^@@ -[0-9]+,[0-9]+ \+[0-9]+,[0-9]+ @@')
                chgLinep=re.compile(r'^[ +]')

                if fromp.match(line):
                    indexFlag=0
                    linesFlag=0
                    diffFlag=0
                    continue
                if allDiffp.match(line):
                    indexFlag=0
                    linesFlag=0
                    diffFlag=0
                    if javaDiffp.match(line):
                        diffFlag=1
                    continue

                if diffFlag==0:
                    continue

                if indexp.match(line):
                    indexFlag=1
                    continue

                if linesp.match(line):
                    linesFlag=1
                    if laterVer:
                        cmtMakeup(laterVer)
                        laterVer=''
                    continue

                if diffFlag and indexFlag and linesFlag:
                    if chgLinep.match(line):
                        laterVer+=line
            except:
                traceback.print_exc()
        if laterVer:
            cmtMakeup(laterVer)
    except:
        traceback.print_exc()


if __name__ == '__main__':
    try:
        #print(isMultiCmtStart("f*///dj/*jfkdf//sdf"))
        patch_fin=sys.argv[1]
        get_modi_javaCode(file(patch_fin))
    except:
        traceback.print_exc()

