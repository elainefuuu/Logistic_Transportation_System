import re

def readFile(pathName):
    f = open(pathName, "r", encoding="UTF-8")
    text = f.read()
    f.close()
    return text

def removeStopwords(wordlist, stopwords):
    return [re.sub(r"[^a-zA-Z0-9]","",w) for w in wordlist if w not in stopwords]