import sys
import yaml
from yaml import Loader, Dumper
from pathlib import Path
import re
from collections import Counter

verbsFile = Path("data/verbs")
textFile = Path(sys.argv[1])
vocabularyFile = Path("data/vocab")

verbType = "verb"
adjectiveType = "adjective"
nounType = "noun"


def progress(items):
    oldIndex = -1
    for (i, item) in enumerate(items):
        index = int(i / len(items) * 100)
        if index > oldIndex:
            print("{}%".format(index))
        oldIndex = index
        yield item

class Word:
    def __init__(self, spelling):
        self.spelling = spelling
        infinitive = getInfinitive(self.spelling)
        if infinitive is not None:
            self.type = verbType
            self.baseForm = infinitive
        else:
            self.type = nounType
            self.baseForm = stripNounEndings(self.spelling)

    def __eq__(self, word):
        if self.type == word.type and self.baseForm == word.baseForm:
            return True

    def __hash__(self):
        return (self.type, self.baseForm).__hash__()

    def __repr__(self):
        if self.type == verbType:
            return "Word({})".format(self.baseForm)
        else:
            return "Word({})".format(self.spelling)

def getInfinitive(spelling):
    for verbConjugations in verbs:
        if spelling in verbConjugations:
            return verbConjugations[0]

def stripNounEndings(word):
    possibleEndings = ["o", "a", "os", "as", "e", "es"]
    for ending in possibleEndings:
        if word.endswith(ending):
            return word.rstrip(ending)
    else:
        return word

class Vocabulary:
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        words = yaml.load(self.path.open("r"), Loader=Loader)
        self.words = []
        for word in words:
            if isinstance(word, Word):
                self.words.append(word)
            else:
                assert isinstance(word, str)
                print("Found new word: {}".format(word))
                self.words.append(Word(word))

    def __contains__(self, word):
        return word in self.words

    def write(self):
        yaml.dump([w for w in self.words], self.path.open("w"))

def getWords(text):
    return (Word(word.lower()) for word in progress(re.findall("[\w]+", text)))

def scanText(text, vocab):
    words = list(getWords(text))
    print("Read {} words".format(len(words)))
    return list(set(list(word for word in words if not word in vocab)))

def getMostRepeated(text, vocab):
    words = list(getWords(text))
    print("Read {} words".format(len(words)))
    return Counter((word for word in words if not word in vocab))

print("Loading verbs")
verbs = yaml.load(verbsFile.open("r"), Loader=Loader)

print("Reading vocabulary")
vocab = Vocabulary(vocabularyFile)
vocab.write() # Write recognized words to file

# print("Scanning text for new words")
# text = textFile.open("r").read()
# print(getMostRepeated(text, vocab).items())

# # newWords = scanText(text, vocab)
# # print("New words:", len(newWords))
# # for word in newWords:
# #     print(word)
# # vocab.words = vocab.words + newWords
# # vocab.write()

# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
