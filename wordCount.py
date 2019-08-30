import re
import sys

if len(sys.argv) is not 3:
    print("Incorrect usage")
    sys.exit(0)

wordMap = {}
textFname = sys.argv[1]
#speech.txt
outputFname = sys.argv[2]
with open(textFname, 'r') as inputs:
    for line in inputs:
        line = line.strip()
        word = re.split('[ \t]', line)
        for singleWord in word:
            if singleWord.endswith(',') or singleWord.endswith('.'):
                singleWord = singleWord[:-1]
            if singleWord not in wordMap:
                wordMap[singleWord] = 0 
            wordMap[singleWord] += 1
with open(outputFname, "w") as outs:
    for singleWord in sorted(wordMap.keys()):
        outs.write(singleWord+" "+str(wordMap[singleWord])+"\n")
