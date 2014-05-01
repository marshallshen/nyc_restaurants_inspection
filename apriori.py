import csv
import sys
import operator
from numpy import *
from optparse import OptionParser
from operator import itemgetter

def loadDataSet(dataFile):
    dataset = []
    csvReader = csv.reader(open(dataFile, 'rb'), delimiter=',')

    for row in csvReader:
        dataset.append(row)
    return dataset

def generateRawOutputFile():
    f = open('datasets/raw_output.txt', 'wr')
    f.close()

def processRawOutputFile(rawDataFile, minSupport, minConfidence):
    support_rows = []
    confidence_rows = []

    csvReader = csv.reader(open(rawDataFile, 'rb'), delimiter=';')
    for row in csvReader:
        if row[0] == 'support':
            support_rows += [row]
        if row[0] == 'confidence':
            confidence_rows += [row]
    sorted_support_rows = sorted(support_rows, key=itemgetter(2), reverse=True)
    sorted_confidence_rows = sorted(confidence_rows, key=itemgetter(3), reverse=True)

    f = open('ouput.txt', 'wr')
    f.write("\n\n")
    f.write('==Frequent itemsets (min_sup=' + str(minSupport) + ')\n')
    for support_row in sorted_support_rows:
        sanitized_row = support_row[1].split("frozenset")[1].strip("(").strip(")")
        f.write(sanitized_row + ' support: ' + support_row[2] + '\n')
    f.write("\n\n")
    f.write('==High-confidence association rules (min_conf=' + str(minConfidence) + ')\n')
    for confidence_row in sorted_confidence_rows:
        f.write(confidence_row[1] + ' support: ' + confidence_row[2] + ' confidence: ' + confidence_row[3] + '\n')
    f.write("\n\n")
    f.close()

    print "Finish generating rules, please check output.txt"

#Choose frozen set as default data structure
#So we can use the set as the key in dict
def generateC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])            
    C1.sort()
    return map(frozenset, C1)

def generateCk(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2:
                retList.append(Lk[i] | Lk[j])
    return retList

def scanData(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            f = open('datasets/raw_output.txt', 'a+b')
            f.write('support;' + str(key) + ';' + str(support) + '; nil' + "\n")
            f.close()

            retList.insert(0,key)
        supportData[key] = support

    return retList, supportData


def apriori(dataSet, minSupport = 0.5):
    C1 = generateC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanData(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = generateCk(L[k-2], k)
        Lk, supK = scanData(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def generateRules(L, supportData, minConf=0.7):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList         

def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = [] #create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf and len(conseq) == 1: # only output rules with only 1 item on the RHS 
            f = open('datasets/raw_output.txt', 'a+b')
            sanitized_freqSet_conseq = str(freqSet-conseq).split("frozenset")[1].strip("(").strip(")")
            sanitized_conseq = str(conseq).split("frozenset")[1].strip("(").strip(")")
            f.write(str('confidence' + ';' + sanitized_freqSet_conseq + '-->' + sanitized_conseq + ';' + str(supportData[freqSet]) + ';' + str(conf) + "\n"))
            f.close()

            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)

    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):    
    Hmp1=calcConf(freqSet, H, supportData, brl, minConf)

    if Hmp1:
        m = len(Hmp1[0])
        if (len(freqSet) > (m + 1)):
            Hmp1 = generateCk(Hmp1, m+1)
            Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
            if (len(Hmp1) > 1):  
                rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__ == "__main__":

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='dataFile',
                         help='filename containing csv',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minS',
                         help='minimum support value',
                         default=0.15,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minC',
                         help='minimum confidence value',
                         default=0.6,
                         type='float')

    (options, args) = optparser.parse_args()

    inFile = None
    if options.dataFile is None:
            inFile = sys.stdin
    elif options.dataFile is not None:
            print "Data file detected.. \n"
    else:
            print 'No dataset filename specified, system with exit\n'
            sys.exit('System will exit')

    dataFile = options.dataFile
    minSupport = options.minS
    minConfidence = options.minC

    generateRawOutputFile()
    dataSet=loadDataSet(dataFile)
    L,supportData=apriori(dataSet,minSupport)
    brl=generateRules(L,supportData,minConfidence)
    processRawOutputFile('datasets/raw_output.txt', minSupport, minConfidence)































