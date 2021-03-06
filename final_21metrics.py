import os
import sys
import traceback
import re
###########match and search, check it for each metric !!!!!!!!!
#########################following metrics use both code and comments:
##blankLine,lineLength,commentRatio,cmtMethod,blankB4cmt,blankAfterCmt,cmtIndent
##1) blankLine
'''this function is to cal the blank lines number of
a whole of part of code file'''
def isBlankLine(str_line):
    blankp=re.compile(r'^\s*$')
    if blankp.match(str_line):
        return True
    else:
        return False

def countBlankLine(code_fin):
    '''blank line cal'''
    lineCnt=0
    blankLineCnt=0
    for line in code_fin.xreadlines():
        try:
            #blank line count
            lineCnt+=1
            if isBlankLine(line):
                blankLineCnt+=1
        except:
            traceback.print_exc()
    return (lineCnt,blankLineCnt)


'''this function is to cal the length of a string line stripped with blanks'''
def lineLen(str_line):
    '''we remove the such kinds of lines which only contains { or }'''
    rm=re.compile(r'^\s*[\{\}]*\s*$')
    if rm.match(str_line):
        return -1
    else:
        return len(str_line.strip())

def getLineLen(code_fin):
    '''line length cal'''
    totalLen=0
    lenCnt=0
    for line in code_fin.xreadlines():
        try:
            #line length count
            length=lineLen(line)
            if length != -1:
                totalLen+=length
                lenCnt+=1
        except:
            traceback.print_exc()
    return(lenCnt,totalLen)


#######################follwing metrics use only code:
##tabOrBlankIndent,braceUse,braceMethod,singleBrace,complexCut,caseUse,
##blankPerLine,statsPerLine,assignBlank,
##1)tabOrBlankIndent
'''this function is to cal how much does tab or blank used to
as indentation in the code file,including code and comment indentation'''
def indentation(str_line):
    tab=0
    blank=0
    indentp=re.compile(r'^[\t| ]+')
    if not isBlankLine(str_line):
        if indentp.match(str_line):
            indent=indentp.findall(str_line)
            #has \t indentation
            if indent[0].find("\t") !=-1:
                tab=1
            #has " " indentation
            if indent[0].find(" ") !=-1:
                    blank=1
    return (tab,blank)

def getIndentUsage(code_fin):
####!!!!need to call the function to remove comments!!!don't forget that
    '''indentation use cal'''
    tabIndentCnt=0
    blankIndentCnt=0
    for line in code_fin.xreadlines():
        try:
            #cal indentation
            (tabIndent,blankIndent)=indentation(line)
            tabIndentCnt+=tabIndent
            blankIndentCnt+=blankIndent
        except:
            traceback.print_exc()
    return(tabIndentCnt,blankIndentCnt)


'''this function is used to cal how does someone use { of the {}, { in the same
   code line or in the next line?'''
def braceUsage(str_line):
    strp=re.compile(r"([^\\])\".*?[^\\]\"")
    str_line=re.sub(strp,'\\1',str_line)
    withInp=re.compile(r'^.*\S+.*{')
    nextp=re.compile(r'^\s*{')
    withInLine=0
    nextLine=0
    if withInp.match(str_line):
        withInLine=1
    elif nextp.match(str_line):
        nextLine=1
    return(withInLine,nextLine)

def getBraceUsage(code_fin):
    '''brace use cal'''
    withInbrace=0
    nextLinebrace=0
    for line in code_fin.xreadlines():
        try:
            #cal braceUsage
            (within,nextLine)=braceUsage(line)
            withInbrace+=within
            nextLinebrace+=nextLine
        except:
            traceback.print_exc()
    return(withInbrace,nextLinebrace)

'''this function is used to cal how does someone use case:[\n]XXX, XXX in the same
   code line or in the next line?'''
def caseUsage(str_line):
    strp=re.compile(r"([^\\])\".*?[^\\]\"")
    str_line=re.sub(strp,'\\1',str_line)
    withInp=re.compile(r'(\S+ |^\s*| +)case +\S+\s*:\s*\S+')
    nextp=re.compile(r'(\S+ |^\s*| +)case +\S+\s*:\s*$')
    withInLine=0
    nextLine=0
    if withInp.search(str_line):
        withInLine=1
    elif nextp.search(str_line):
        nextLine=1
    return(withInLine,nextLine)

def getCaseUsage(code_fin):
    '''case use cal'''
    withInCase=0
    nextLineCase=0
    for line in code_fin.xreadlines():
        try:
            #cal caseUsage
            (within,nextLine)=caseUsage(line)
            withInCase+=within
            nextLineCase+=nextLine
        except:
            traceback.print_exc()
    return(withInCase,nextLineCase)

'''this function is used to cal how many blanks within a code line
exclude the blanks within the string constant
'''
def blankWithinLine(str_line):
    if not isBlankLine(str_line):
        strp=re.compile(r"([^\\])\".*?[^\\]\"")
        str_line=re.sub(strp,'\\1',str_line)
        return str_line.strip().count(" ")
    else:
        return -1
def countBlankWithinLine(code_fin):
    '''blanks within code line cal'''
    blankWithin=0
    blankWithinCnt=0
    for line in code_fin.xreadlines():
        try:
            #cal blanks within code lines
            blanks=blankWithinLine(line)
            if blanks != -1:
                blankWithin+=blanks
                blankWithinCnt+=1
        except:
            traceback.print_exc()
    return(blankWithinCnt,blankWithin)

'''for statsPerLine, we consider consider lines which states more than 2 statements.
we output the lines num and the total statements stated by these lines
we use ";" to identify the statements. since string and // comments will most likely
increase the false indentification of states. we first remove them before calculation'''
def moreThan2Stats(code_fin):
    strp=re.compile(r"\".*?\"")
    coma=re.compile(r";")
    cmt=re.compile(r"//.*")
    lineCnt=0
    comaCnt=0
    for line in code_fin.xreadlines():
        line=line.strip("\n")
        s=re.sub(strp,'',line)
        s=re.sub(cmt,'',s)
        if coma.search(s):
            lenM=len(coma.findall(s))
            if lenM != 1:
                lineCnt+=1
                comaCnt+=lenM
    return(lineCnt,comaCnt)

'''for assign stats, do it use blanks on both sides of the ='''
def assignBlank(code_fin):
    assignp=re.compile(r"(\s|\w)=(\s|\w)")
    assignBlankp=re.compile(r"\s=\s")
    calp=re.compile(r"[\+\-\*\/\%\&\|\^]=")
    calBlankp=re.compile(r"\s[\+\-\*\/\%\&\|\^]=\s")
    bitp=re.compile(r"(<<|>>|>>>)=")
    bitBlankp=re.compile(r" (<<|>>|>>>)= ")
    totalAssign=0
    assignBlank=0
    strp=re.compile(r"([^\\])\".*?[^\\]\"")
    for line in code_fin.xreadlines():
        line=re.sub(strp,'\\1',line)
        if calp.search(line):
            totalAssign+=len(calp.findall(line))
            assignBlank+=len(calBlankp.findall(line))
        if bitp.search(line):
            totalAssign+=len(bitp.findall(line))
            assignBlank+=len(bitBlankp.findall(line))
        if assignp.search(line):
            totalAssign+=len(assignp.findall(line))
            assignBlank+=len(assignBlankp.findall(line))
    return(totalAssign,assignBlank)

'''whether the complex stat(len>80) cut in multi lines'''
def complexCut(code_fin):
    cutp=re.compile(r'[){;]\s*$')
    cutCnt=0
    complexCnt=0
    for line in code_fin.xreadlines():
        if not isBlankLine(line):
            line=line.rstrip()
            lineLen=len(line)
            if lineLen>80:
                complexCnt+=1
                if not cutp.search(line):
                    cutCnt+=1
    return(complexCnt,cutCnt)

'''if a stats has more than 3 operators, does it use ()?'''
def getBracketUse(code_fin):
    content=''
    ops=re.compile(r'\+\+|\-\-|&&|\|\||[!~\+\-\*/%&\|\^]|<<|>>>|>>|[><]|\?.+:')
    cnt=0
    bracketCnt=0
    strp=re.compile(r"([^\\])\".*?[^\\]\"")
    for line in code_fin.xreadlines():
        str_line=re.sub(strp,"\\1",line)
        content=content+str_line
    stats=content.split(";")
    for stat in stats:
        if ops.search(stat):
            opCnt=len(ops.findall(stat))
            if opCnt>=3:
                cnt+=1
                if re.compile(r'\(.*\)').search(stat):
                    bracketCnt+=1
    return(cnt,bracketCnt)

def getOpsNum(code_fin):
    content=''
    ops=re.compile(r'\+\+|\-\-|&&|\|\||[!~\+\-\*/%&\|\^]|<<|>>>|>>|[><]|\?.+:')
    statCnt=0
    opsCnt=0
    strp=re.compile(r"([^\\])\".*?[^\\]\"")
    for line in code_fin.xreadlines():
        str_line=re.sub(strp,"\\1",line)
        content=content+str_line
    stats=content.split(";")
    for stat in stats:
        if ops.search(stat):
            opsCnt+=len(ops.findall(stat))
            statCnt+=1
    return(statCnt,opsCnt)


'''
if __name__ == "__main__":
    code_fin=sys.argv[1]
    print(getBracketUse(file(code_fin,'r')))
    print(assignBlank(file(code_fin,'r')))
    print(countBlankWithinLine(file(code_fin,'r')))
    print(complexCut(file(code_fin,'r')))
'''
