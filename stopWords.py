
trainTextFile=open('D:/USC/Spring17/NLP/Assmt2/train-text.txt','r')
trainText=[]
for line in trainTextFile:
    trainText.append(line.lower())
stopwordlist={}
punc="!?.-:<>()@#$\'\""
dict1={}
for line in trainText:
    word=line.split()
    key=word[0]
    word.remove(key)
    for w in word:
        for ch in punc:
            w=w.replace(ch,"")
            w=w.rstrip()
            w=w.lstrip()
        w=w.strip(',;][!?.:<>()@#$\'\"')

        if w not in dict1:
            dict1[w]=1
        else:
            dict1[w]+=1
target = open('D:/USC/Spring17/NLP/Assmt2/stopwords.txt', 'a')

for k,v in dict1.items():
    if v > 200:
        target.write(k)
        target.write(":")
        target.write(str(v))
        target.write("\n")

