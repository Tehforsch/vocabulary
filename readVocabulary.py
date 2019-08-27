import yaml
from yaml import Loader, Dumper
from pathlib import Path
import re

verbsFile = Path("verbsSmall")
textFile = Path("harryPotter")

verbType = "verb"
adjectiveType = "adjective"
nounType = "noun"

vocabularyFile = "vocab"

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
    def __init__(self, filename):
        self.path = Path(filename)
        self.read()

    def read(self):
        self.words = [Word(w) for w in yaml.load(self.path.open("r"), Loader=Loader)]

    def __contains__(self, word):
        return word in self.words

    def write(self):
        yaml.dump(self.words, self.path.open("w"))

def getWords(text):
    return (Word(word.lower()) for word in re.findall("[\w]+", text))

def scanText(text, vocab):
    words = list(getWords(text))
    print("Read {} words".format(len(words)))
    return list(set(list(word for word in words if not word in vocab)))

print("Loading verbs")
verbs = yaml.load(verbsFile.open("r"), Loader=Loader)

print("Reading vocabulary")
vocab = Vocabulary(vocabularyFile)

print("Scanning text for new words")
text = textFile.open("r").read()
newWords = scanText(text, vocab)
print("New words:", len(newWords))
# for word in newWords:
    # print(word)
# vocab.write()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
