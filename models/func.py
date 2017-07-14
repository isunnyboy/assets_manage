# -*- coding: utf-8 -*-
# 功能函数，将以 ‘,’分割的字符串进行唯一化处理，并再次转化为以 ‘,’分割的字符串
def strPlus(strOrig, strToPlus):

    listOrig = list(str(strOrig).split(','))
    listToPlus = list(str(strToPlus).split(','))
    listToPlus.extend(listOrig)
    listOne = list(set(listToPlus))

    joinStr = ''
    for r in listOne:
        if joinStr == '':
            joinStr = r
        else:
            joinStr = joinStr + ',' + r
    return joinStr

def test():
    listA = []
    dicA = {}
