from pathlib import Path
import json
import yaml

verbDataFolder = Path("verb-data/allSpanishVerbs")
outFile = Path("verbs")

def getFirstWord(s):
    return s.lstrip(" ").split(" ")[0]

def getConjugations(verbData):
    for conjugation in verbData["conjugations"]:
        conjugation["value"] = conjugation["value"].replace("se ", "")
        if "negative" in conjugation["group"]:
            # Filter negative imperative words, not necessary.
            continue
        if conjugation["value"] == "":
            # Some are empty, I don't know why
            continue
        yield getFirstWord(conjugation["value"]) 

verbs = []
for f in verbDataFolder.glob("*json"):
    verbData = json.loads(f.open("r").read())
    # some entries are not full, ignore them
    if verbData["conjugations"] is None:
        continue
    infinitive = verbData["word"]
    conjugations = getConjugations(verbData)
    uniqueConjugations = list(set(conjugations))
    sortedUniqueConjugations = sorted(uniqueConjugations)
    verbs.append([infinitive] + sortedUniqueConjugations)

yaml.dump(sorted(verbs, key=lambda x: x[0]), outFile.open("w"))
