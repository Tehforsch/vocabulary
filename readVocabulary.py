import sys
import yaml
from yaml import Loader, Dumper
from pathlib import Path
import re
from collections import Counter
from translate import Translator

translator = Translator(from_lang="es", to_lang="en")

verbsFile = Path("data/verbDictSmall")
textFile = Path(sys.argv[1])
vocabularyFile = Path("data/vocab")
verbs = None
vocab = None

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
            self.isVerb = True
            self.baseForm = infinitive
        else:
            self.isVerb = False
            self.baseForm = stripNounEndings(self.spelling)

    def __eq__(self, word):
        if self.isVerb == word.isVerb and self.baseForm == word.baseForm:
            return True

    def __hash__(self):
        return (self.isVerb, self.baseForm).__hash__()

    def __repr__(self):
        if self.isVerb == True:
            return "{}".format(self.baseForm)
        else:
            return "{}".format(self.spelling)

def getInfinitive(spelling):
    if spelling in verbs:
        return verbs[spelling]

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
        self.words = set()
        for word in words:
            assert isinstance(word, str)
            w = Word(word)
            self.words.add(Word(word))

    def __contains__(self, word):
        return word in self.words

    def write(self):
        yaml.dump(list(str(w) for w in self.words), self.path.open("w"))

def getWordsFromText(text):
    return (Word(word.lower()) for word in re.findall("[\w]+", text))

def getMostRepeated(text, vocab):
    words = getWordsFromText(text)
    return Counter(word for word in words if not word in vocab)

def getMostFrequentNewWords():
    print("Scanning text for new words")
    text = textFile.open("r").read()
    counter = getMostRepeated(text, vocab)
    sortedCounter = list(counter.items())
    sortedCounter.sort(key = lambda x: -x[1])
    return sortedCounter

def goThroughWordsOneByOne():
    sortedByOccurences = getMostFrequentNewWords()
    newWords = []
    oldWords = []
    for (word, count) in sortedByOccurences:
        print("- {} {}".format(word, count))
        print("({})".format(translator.translate(word.spelling)))
        inp = input("Known (empty), new (n) or abort (a)? ")
        if inp == "n":
            newWords.append(word)
        elif inp == "a":
            break
        else:
            oldWords.append(word)

    print("New words found:")
    print("\n".join(str(w) for w in newWords))
    if input("Write all other words to vocabulary (y/N)? ") == "y":
        for word in newWords + oldWords:
            vocab.words.add(word)
        vocab.write()

def printMostFrequentWords():
    sortedByOccurences = getMostFrequentNewWords()
    for (word, count) in sortedByOccurences:
        print("- {}".format(word))

print("Loading verbs")
verbs = yaml.load(verbsFile.open("r"), Loader=Loader)

print("Reading vocabulary")
vocab = Vocabulary(vocabularyFile)

goThroughWordsOneByOne()

# if __name__ == '__main__':
    # import doctest
#     doctest.testmod()
