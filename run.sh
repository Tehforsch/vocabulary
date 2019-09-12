mkdir data/backup
cp --backup=numbered data/vocab data/backup/vocab
cp --backup=numbered data/verbDict data/backup/verbDict
python3 readVocabulary.py $1
