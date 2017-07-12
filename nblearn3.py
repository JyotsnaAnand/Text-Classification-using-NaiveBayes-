import string
import math
import sys
#load the entire train-text file input to a list
trainTextFile=open(sys.argv[1],"r")
trainText=[]
trainingDataFS={}

for line in trainTextFile:
    trainText.append(line)

#load the entire train-label file input to a list
trainLabelFile=open(sys.argv[2],"r")
trainLabel=[]
for line in trainLabelFile:
    trainLabel.append(line)

#load stop words
#stopWordsFile=open('stopwordlist.txt','r')
stopWords=['is', 'no', 'just', 'its', 'called' , 'our' , 'but' , 'for' , 'has', 'when', 'i', 'be', 'a', 'out', 'could', 'in', 'are', 'on', 'will', 'was', 'the', 'of',  'two', 'so', 'would', 'there', 'go', 'were', 'it', 'and', 'one', 'while', 'we', 'their', 'that', 'have', 'here', 'me', 'very', 'do', 'as', 'them', 'an', 'or', 'my', 'this', 'which', 'they', 'by', 'you', 'from', 'with', 'to', 'at', 'he', 'had', 'been', 'she']
#sline = stopWordsFile.readline()
#while sline:
#    w=sline.strip("\n")
#    w=w.strip(" ")
#    stopWords.append(w)
#    sline=stopWordsFile.readline()
#stopWordsFile.close()

#open file handle for model file
modelFile = open('nbmodel.txt', 'w')
#testTextFile=open('D:/USC/Spring17/NLP/Assmt2/test-text3.txt','a')
#testLabelFile=open('D:/USC/Spring17/NLP/Assmt2/test-label3.txt','a')


punc="!?.-:<>/\;,()@#$\'\""
posTrainData=[]
negTrainData = []
trueTrainData = []
decTrainData = []
posProb,negProb,truthProb,deceptiveProb=0,0,0,0
posfeatureset, negfeatureset, trufeatureset, decfeatureset = {}, {}, {}, {}

#pre process data
def processData(dataSet):
    processedData=[]
    for line in dataSet:
        for w in line:
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
                        processedData.append(w)

    return processedData

#preprocess training data
def processTrainingData(trainDataSet):
    processedSet=[]
    for line in trainDataSet:
        word=line.split()
        for w in word[1:]:
            w=w.lower()
            w=w.rstrip()
            w=w.lstrip()
            w=w.strip('`~ ,;][!?.:<>(*)@#$0123456789\'\"+=&^%\n')
            if w not in stopWords:
                w = w.rstrip('s')
                if w[-3:] == "ing":
                    w = w.rstrip('ing')
                if w[-2:] == "ed":
                    w = w.rstrip('ed')
                if w[-2:] == "ly":
                    w = w.rstrip('ly')
                # w = w.strip("ed,ing,s,d")
                for ch in w:
                    if ch in punc:
                        w = w.replace(ch, "")
                if w != '':
                    processedSet.append(w)

            #if w[-2:] == "ly":
            #    w=w.rstrip("ly")
            #w=w.rstrip("s")

            #w=w.rstrip("ss")

    return processedSet

'''
#remove stop words
def stopWordRemoval(dataSet):
    for word in dataSet:
        if word in stopWords:
            dataSet.remove(word)
        else:
            # print ("no", word)
            temp.append(word)

    return dataSet
'''
#find feature set
def createFeatureSet(dataset):
    featureset = {}
    for w in dataset:

        if w not in featureset:
            featureset[w] = 1
        else:
            featureset[w] += 1
    return featureset
finalFeatureSet={}
#add missing features to pos/neg/dec/tru FS
def smoothFeatureSets(trainingDataFS, featureset):
    for k, v in trainingDataFS.items():
        if k not in featureset:
            featureset[k] = 1
        else:
            featureset[k]+=1


'''

def updateConditionalProb(posFS,negFS, truFS, decFS):

   for k in posFS:
        word=k
        modelFile.write(k)
        modelFile.write(" ")
        modelFile.write(str(posFS[k]))
        modelFile.write(" ")
        for k1 in negFS:
            if k1==word:
                modelFile.write(str(negFS[k1]))
                modelFile.write(" ")
        for k2 in truFS:
            if k2==word:
                modelFile.write(str(truFS[k2]))
                modelFile.write(" ")
        for k3 in decFS:
            if k3==word:
                modelFile.write(str(decFS[k3]))
                modelFile.write("\n")
'''


#split trainText into training set and development set using 75-25% split
size=len(trainText)

#trainDataSize=int(0.75*size)
#devDataSize=int(0.25*size)

#training and dev data set variables for text, label
trainDataSet = []
trainLabelSet=[]
#devDataSet=[]
#devLabelSet=[]

#create the training set
for i in range(size):
    trainDataSet.append(trainText[i])
    trainLabelSet.append(trainLabel[i])
'''
#write remaining data to a test data file for classify.py usage
for i in range(trainDataSize,size,1):
    devDataSet.append(trainText[i])
    devLabelSet.append(trainLabel[i])
    testTextFile.write(trainText[i])
    testLabelFile.write(trainLabel[i])
'''




#train data set- stemming, stop word removal, punctuation removal

#calculate class probabilities
#create pos,neg,truthful,dec datasets
itr=0

for line in trainLabelSet:
         line2=trainDataSet[itr]
         words=line.split()
         trainWords=line2.split()
         if words[1]=="truthful":
              truthProb+=1
              trueTrainData.append(trainWords[1:])
         elif words[1]=="deceptive":
              deceptiveProb+=1
              decTrainData.append(trainWords[1:])
         if words[2]=="positive":
              posProb+=1
              posTrainData.append(trainWords[1:])
         elif words[2]=="negative":
              negProb+=1
              negTrainData.append(trainWords[1:])
         itr+=1

#remove punctuations and pre process data

processPosTrainData=processData(posTrainData)
processNegTrainData=processData(negTrainData)
processTruTrainData=processData(trueTrainData)
processDecTrainData=processData(decTrainData)
processTrainData=processTrainingData(trainDataSet)

'''
#remove stop words
for word in processPosTrainData:

            if word in stopWords:
                    processPosTrainData.remove(word)

            else:
                    #print ("no", word)
                    temp.append(word)
'''
#processPosTrainData=stopWordRemoval(processPosTrainData)
#processDecTrainData=stopWordRemoval(processDecTrainData)
#processNegTrainData=stopWordRemoval(processNegTrainData)
#processTruTrainData=stopWordRemoval(processTruTrainData)
#processTrainData=stopWordRemoval(processTrainData)

#create feature set
posfeatureset=createFeatureSet(processPosTrainData)
negfeatureset=createFeatureSet(processNegTrainData)
trufeatureset=createFeatureSet(processTruTrainData)
decfeatureset=createFeatureSet(processDecTrainData)
trainingDataFS=createFeatureSet(processTrainData)

#SMOOThing
#add features from training FS to other FS (smoothing)
smoothFeatureSets(trainingDataFS, posfeatureset)
smoothFeatureSets(trainingDataFS, negfeatureset)
smoothFeatureSets(trainingDataFS, trufeatureset)
smoothFeatureSets(trainingDataFS, decfeatureset)


#calculate pos,neg,tru,dec vocabulary sizes
''''
posVocabsize=len(processPosTrainData)
negVocabsize = len(processNegTrainData)
truVocabsize=len(processTruTrainData)
decVocabsize=len(processDecTrainData)

'''
posVocabsize,negVocabsize,truVocabsize,decVocabsize=0,0,0,0
for k in posfeatureset:
    posVocabsize+=posfeatureset[k]
for k in negfeatureset:
    negVocabsize+=negfeatureset[k]
for k in trufeatureset:
    truVocabsize+=trufeatureset[k]
for k in decfeatureset:
    decVocabsize+=decfeatureset[k]

#find word probabilities
posVocabLog=math.log(posVocabsize)
negVocabLog=math.log(negVocabsize)
truVocabLog=math.log(truVocabsize)
decVocabLog=math.log(decVocabsize)
for k in posfeatureset:
    prob=math.log(posfeatureset[k])-posVocabLog
    posfeatureset[k]=prob
for k in negfeatureset:
    prob=math.log(negfeatureset[k])-negVocabLog
    negfeatureset[k]=prob
for k in trufeatureset:
    prob=math.log(trufeatureset[k])-truVocabLog
    trufeatureset[k]=prob
for k in decfeatureset:
    prob=math.log(decfeatureset[k])-decVocabLog
    decfeatureset[k]=prob
#create final Feature set
for k in trainingDataFS:

        v=str(posfeatureset[k])+" "+str(negfeatureset[k])+" "+str(trufeatureset[k])+" "+str(decfeatureset[k])

        finalFeatureSet[k]=v
#print (posVocabsize,negVocabsize,truVocabsize,decVocabsize)


#calculate class probabilities : class prob - total size
posClassProb=math.log(posProb)-math.log(size)
negClassProb=math.log(negProb)-math.log(size)
truClassProb=math.log(truthProb)-math.log(size)
decClassProb=math.log(deceptiveProb)-math.log(size)

#write parameters to model file
#modelFile.write("----Parameters are written in order of: 1)Class name 2)Class prior probability 3)Class Vocabulary size.")
#modelFile.write("Conditional probabilities for each word are written in order of \"word positive probability negative probability truthful probability deceptive probability")
modelFile.write("----Read me: Parameters in first four lines are written in order of: 1)Class name 2)Class prior probability 3)Class Vocabulary size.")
modelFile.write("Conditional probabilities for each word are written in order of \"word <space> positive probability <space> negative probability <space> truthful probability <space> deceptive probability----")
modelFile.write("\n")
modelFile.write("POSITIVE  ")
modelFile.write(str(posClassProb))
modelFile.write("\n")
modelFile.write("NEGATIVE  ")
modelFile.write(str(negClassProb))
modelFile.write("\n")
modelFile.write("TRUTHFUL  ")
modelFile.write(str(truClassProb))
modelFile.write("\n")
modelFile.write("DECEPTIVE  ")
modelFile.write(str(decClassProb))
modelFile.write("\n")
#updateConditionalProb(posfeatureset, negfeatureset, trufeatureset, decfeatureset)
modelFile.write("CONDITIONAL PROBABILITIES BEGIN: \n")
i=0
for l in finalFeatureSet:
    #words=finalFeatureSet[l].split()
    modelFile.write(l)
    modelFile.write(" ")
    modelFile.write(finalFeatureSet[l])
    modelFile.write("\n")





