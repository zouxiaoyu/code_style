from final_21metrics import *
from rmCmt import *

def useOnlyCodeMetrics(codeFileList_fin):
    tab2=0;blank2=0;
    cnt3=0;bracketCnt3=0;
    withInBrace4=0;nextLineBrace4=0;
    complex5=0;cut5=0;
    withInCase6=0;nextLineCase6=0;
    line8=0;blank8=0;
    line9=0;stats9=0;
    assign10=0;blank10=0;
    line11=0;ops11=0;
    codeRes={}

    for code_fin in file(codeFileList_fin,'r').xreadlines():
        code_fin=code_fin.strip('\n')
        trim_cmt(code_fin,"noCmtFile")

        '''tab or blank indent'''
        (tabCnt,blankCnt)=getIndentUsage(file("noCmtFile","r"))
        tab2+=tabCnt;blank2+=blankCnt

        '''if a stats has more than 3 operators, does it use ()?'''
        (cnt,bracketCnt)=getBracketUse(file("noCmtFile","r"))
        cnt3+=cnt;bracketCnt3+=bracketCnt;

        ''' how does someone use { of the {},
        { in the same code line or in the next line?
        '''
        (withInBrace,nextLineBrace)=getBraceUsage(file("noCmtFile","r"))
        withInBrace4+=withInBrace;nextLineBrace4+=nextLineBrace

        '''whether the complex stat(len>80) cut in multi lines'''
        (complexCnt,cutCnt)=complexCut(file("noCmtFile",'r'))
        complex5+=complexCnt;cut5+=cutCnt

        '''how does someone use case:[\n]XXX,
        XXX in the same code line or in the next line?
        '''
        (withInCase,nextLineCase)=getCaseUsage(file("noCmtFile","r"))
        withInCase6+=withInCase;nextLineCase6+=nextLineCase;

        '''how many blanks within a code line'''
        (blankLine,blanks)=countBlankWithinLine(file("noCmtFile","r"))
        line8+=blankLine;blank8+=blanks;

        '''only consider lines which states more than 2 statements(;ended).
           we output the lines num and the total statements stated by these lines
        '''
        (lineCnt,statsCnt)=moreThan2Stats(file("noCmtFile","r"))
        line9+=lineCnt;stats9+=statsCnt;

        '''for assign stats, do it use blanks on both sides of the ='''
        (assignCnt,useBlankCnt)=assignBlank(file("noCmtFile",'r'))
        assign10+=assignCnt;blank10+=useBlankCnt;

        '''how many ops used in a stat'''
        (statCnt,opsCnt)=getOpsNum(file("noCmtFile",'r'))
        line11+=statCnt;ops11+=opsCnt;

    if tab2+blank2==0:
        codeRes["tabIndent"]='#'
    else:
        codeRes["tabIndent"]=tab2*1.0/(tab2+blank2)

    if cnt3==0:
        codeRes["bracketUse"]="#"
    else:
        codeRes["bracketUse"]=bracketCnt3*1.0/cnt3

    if withInBrace4+nextLineBrace4==0:
        codeRes["braceUse"]="#"
    else:
        codeRes["braceUse"]=withInBrace4*1.0/(withInBrace4+nextLineBrace4)

    if complex5==0:
        codeRes["complexCut"]="#"
    else:
        codeRes["complexCut"]=cut5*1.0/complex5

    if withInCase6+nextLineCase6==0:
        codeRes["caseUse"]="#"
    else:
        codeRes["caseUse"]=withInCase6*1.0/(withInCase6+nextLineCase6)

    if line8==0:
        codeRes["blanksPerLine"]="#"
    else:
        codeRes["blanksPerLine"]=blank8*1.0/line8

    if line9==0:
        codeRes["statsPerLine"]=1
    else:
        codeRes["statsPerLine"]=stats9*1.0/line9;

    if assign10==0:
        codeRes["assignBlank"]="#"
    else:
        codeRes["assignBlank"]=blank10*1.0/assign10

    if line11==0:
        codeRes["opsPerStat"]="#"
    else:
        codeRes["opsPerStat"]=ops11*1.0/line11;

    return(codeRes)
    print "%s,%s,%s,%s,%s,%s,%s,%s,%s" % (codeRes["tabIndent"], \
            codeRes["bracketUse"],codeRes["braceUse"], codeRes["complexCut"],\
            codeRes["caseUse"],codeRes["blanksPerLine"],codeRes["statsPerLine"],\
            codeRes["assignBlank"],codeRes["opsPerStat"])

def use_oriModi_metrics(codeFileList_fin):
    oriRes={}
    line1=0
    blankLine1=0

    line7=0
    len7=0
    for code_fin in file(codeFileList_fin,'r').xreadlines():
        code_fin=code_fin.strip('\n')
        (lineCnt,blankLineCnt)=countBlankLine(file(code_fin,"r"))
        line1+=lineCnt
        blankLine1+=blankLineCnt

        (lineCnt,totalLen)=getLineLen(file(code_fin,"r"))
        line7+=lineCnt
        len7+=totalLen

    if line1==0:
        oriRes["blankLineRatio"]="#"
    else:
        oriRes["blankLineRatio"]=blankLine1*1.0/line1
    if line7==0:
        oriRes["lineLen"]="#"
    else:
        oriRes["lineLen"]=len7*1.0/line7

    return(oriRes)


if __name__ == "__main__":
    codeFileList_fin=sys.argv[1]
    finalRes=''
    oriRes=use_oriModi_metrics(codeFileList_fin)
    codeRes=useOnlyCodeMetrics(codeFileList_fin)
    finalRes=str(oriRes["blankLineRatio"])+","+str(codeRes["tabIndent"])+","+ \
            str(codeRes["bracketUse"])+","+str(codeRes["braceUse"])+","+ \
            str(codeRes["complexCut"]) +","+ str(codeRes["caseUse"])+","+ \
            str(oriRes["lineLen"])+","+ str(codeRes["blanksPerLine"])+","+\
            str(codeRes["statsPerLine"])+","+ str(codeRes["assignBlank"])+","+ \
            str(codeRes["opsPerStat"])
    print finalRes
