import yaml
from yaml import Loader, Dumper
from pathlib import Path
import re

# class Word:
    # def __init__(self, word):

class Word:
    def __init__(self, spelling):
        self.spelling = spelling
        self.type = None

    def __eq__(self, word):
        if self.spelling == word.spelling:
            return True
        if self.type is not None and word.type is not None and self.type != word.type:
            return False
        spelling1 = self.spelling
        spelling2 = word.spelling
        if self.type is None:
            return adjectiveEquality(spelling1, spelling2) or verbEquality(spelling1, spelling2) or nounEquality(spelling1, spelling2)
        elif self.type == "adjective":
            return adjectiveEquality(spelling1, spelling2)
        elif self.type == "verb":
            return verbEquality(spelling1, spelling2)
        elif self.type == "noun":
            return nounEquality(spelling1, spelling2)
        else:
            return False

    def __repr__(self):
        return "Word({})".format(self.spelling)

def adjectiveEquality(spelling1, spelling2):
    """Compare to (potential) adjectives for equality by removing the plural and feminine/male endings and comparing the 'base words'
    # >>> adjectiveEquality("rojos", "rojas")
    # True
    # >>> adjectiveEquality("rojos", "roja")
    # True
    # >>> adjectiveEquality("largo", "largas")
    # True
    # >>> adjectiveEquality("roja", "azul")
    # False
    """
    if len(spelling1) > 3 and spelling1[:2] != spelling2[:2]:
        return False
    return stripAdjectiveEndings(spelling1) == stripAdjectiveEndings(spelling2)

def nounEquality(spelling1, spelling2):
    return adjectiveEquality(spelling1, spelling2)

def verbEquality(spelling1, spelling2):
    return False

def stripAdjectiveEndings(word):
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

def unique(items):
    """Return unique words, that is, remove those that are equal to each other. This replaces just calling set(items) 
    since Word is not a hashable type (and it is really hard to construct a hash for it)"""
    uniqueItems = []
    print(len(items))
    for item in items:
        if not item in uniqueItems:
            uniqueItems.append(item)
    return uniqueItems

def scanText(text, vocab):
    words = list(getWords(text))
    return unique(list(word for word in words if not word in vocab))

vocab = Vocabulary("vocab")
text = "".join(Path("text").open("r").readlines())
newWords = scanText(text, vocab)
print(len(newWords))
# for word in newWords:
    # print(word)
# vocab.write()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
