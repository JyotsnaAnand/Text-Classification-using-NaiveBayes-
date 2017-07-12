import math
import sys
modelFile=open('nbmodel.txt','r')
testTextFile=open(sys.argv[1],'r')
outputFile=open('nboutput.txt','w')
testText=[]
punc="!?.-:<>/\;,()@#$\'\""
classProb=0.0
modelData=[]
for line in modelFile:
   modelData.append(line)

#load stop words
#stopWordsFile=open('stopwordlist.txt','r')
stopWords=['is', 'no', 'just', 'its', 'called' , 'our' , 'but' , 'for' , 'has', 'when', 'i', 'be', 'a', 'out', 'could', 'in', 'are', 'on', 'will', 'was', 'the', 'of',  'two', 'so', 'would', 'there', 'go', 'were', 'it', 'and', 'one', 'while', 'we', 'their', 'that', 'have', 'here', 'me', 'very', 'do', 'as', 'them', 'an', 'or', 'my', 'this', 'which', 'they', 'by', 'you', 'from', 'with', 'to', 'at', 'he', 'had', 'been', 'she']
'''
sline = stopWordsFile.readline()
while sline:
    w=sline.strip("\n")
    w=w.strip(" ")
    stopWords.append(w)
    sline=stopWordsFile.readline()
stopWordsFile.close()
'''
for line in testTextFile:
    testText.append(line)

#find class priors and vocabulary sizes from model file
pl=modelData[1]
nl=modelData[2]
tl=modelData[3]
dl=modelData[4]
wp=pl.split()
wn=nl.split()
wt=tl.split()
wd=dl.split()
posPrior=float(wp[1])
#posVocab=math.log(float(wp[2]))
negPrior=float(wn[1])
#negVocab=math.log(float(wn[2]))
truPrior=float(wt[1])
#truVocab=math.log(float(wt[2]))
decPrior=float(wd[1])
#decVocab=math.log(float(wd[2]))
posFinal, negFinal, truFinal, decFinal=0.0,0.0,0.0,0.0
#create a dict to store conditional prob.
ctr=0
for line in modelData:
    if "CONDITIONAL PROBABILITIES BEGIN" in line:
        start=ctr+1
        break
    else:
        ctr+=1

probDict={}
for line in range(start,len(modelData),1):
    w=modelData[line].split()
    value=""
    value=str(w[1]+ " "+ w[2]+" "+ w[3]+" "+w[4])
    probDict[w[0]]=value


def processData(line):
        dataToClassify=[]
        words=line.split()
        for w in words[1:]:
                w = w.lower()
                w = w.rstrip()
                w = w.lstrip()
                w = w.strip('`~ ,;][!?.:<>(*)@#$\'\"+=&^%1234567890\n')
                if w not in stopWords:
                    w=w.rstrip('s')
                    if w[-3:] == "ing":
                        w = w.rstrip('ing')
                    if w[-2:]=="ed":
                        w=w.rstrip('ed')
                    if w[-2:] == "ly":
                        w = w.rstrip('ly')
                #w = w.strip("ed,ing,s,d")
                    for ch in w:
                        if ch in punc:
                            w = w.replace(ch, "")
                    if w != '':
                        dataToClassify.append(w)
        return dataToClassify
'''

def findClass(parameter, testSentence):
    wordprob=0.0
    prior=0.0
    prob=0
    classprob=0.0
    if parameter=="POSITIVE":
        cp=1
    elif parameter=="NEGATIVE":
        cp=2
    elif parameter=="TRUTHFUL":
        cp=3
    elif parameter=="DECEPTIVE":
        cp=4

    for line in modelData:
        if parameter in line:
            w=line.split()
            prior=float(w[1])
            vocab=float(w[2])
            break;

    classprob+=prior
    for word in testSentence:
        for line in modelData:
            cw=line.split()
            if word == cw[0]:

                prob=int(cw[cp])
                p1=math.log(prob)
                p2=math.log(vocab)

                wordprob=p1-p2
                classprob += wordprob
                break;

        #classprob += wordprob

        #print(cw[cp],prob)
        #p1=math.log(prob)
        #p2=math.log(vocab)

        #wordprob=p1-p2


    #print(classprob)
    return classprob
'''

#preprocess test data set
for line in testText:

    w=line.split()

    dataToClassify=processData(line)
    posFinal=posPrior
    negFinal=negPrior
    truFinal=truPrior
    decFinal=decPrior
    for word in dataToClassify:
        if word in probDict:
            value=probDict[word]
            value=value.split()
            posWordProb=float(value[0])
            negWordProb=float(value[1])
            truWordProb=float(value[2])
            decWordProb=float(value[3])
            posFinal+= posWordProb
            negFinal+=negWordProb
            truFinal+=truWordProb
            decFinal+=decWordProb
    outputFile.write(w[0])
    if truFinal>=decFinal:
        #outputDict[word[0]].append(" truthful")
        outputFile.write(" truthful ")
    else:
        #outputDict[word[0]].append(" deceptive")
        outputFile.write(" deceptive ")
    if posFinal >= negFinal:
        #outputDict[word[0]].append(" positive")
        outputFile.write("positive")
        outputFile.write("\n")
    else:
        #outputDict[word[0]].append(" negative")
        outputFile.write("negative")
        outputFile.write("\n")










'''
   words=line.split()
   dataToClassify=processData(line)
   a=dataToClassify
   posProb=findClass("POSITIVE",a)
   negProb = findClass("NEGATIVE", a)
   truProb = findClass("TRUTHFUL", a)
   decProb = findClass("DECEPTIVE", a)
   outputFile.write(words[0])
   if (truProb >= decProb):
       outputFile.write(" truthful ")
   else:
       outputFile.write(" deceptive ")
   if (posProb >= negProb):
       outputFile.write("positive")
       outputFile.write("\n")
   else:
       outputFile.write("negative")
       outputFile.write("\n")
'''





