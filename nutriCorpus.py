import nltk, re, string
import numpy as np
import sqlite3, ipdb

createCorpusFiles = False
root = "/home/jstraub/scratch/sr28ascCorpus/"
# create plain text corpus in some directory
if createCorpusFiles:
  conn = sqlite3.connect("sr28asc.db")
  c = conn.cursor()
  c.execute('SELECT NDB_No,Long_Desc FROM FOOD_DES')
  for i,desc in enumerate(c.fetchall()):
    with open(root+desc[0]+".txt","w") as f:
      f.write(re.sub('['+string.punctuation+']', '', desc[1]))
    # print progress
    if i%100 == 0:
      print i
  conn.close()

from nltk.corpus import PlaintextCorpusReader
from nltk import cluster
from nltk.cluster import util
from nltk.cluster import api
from nltk.cluster import euclidean_distance
from nltk.cluster import cosine_distance
from nltk.stem.lancaster import *

st = LancasterStemmer()
texts = PlaintextCorpusReader(root, '.*\.txt')
print "Read in", len(texts.fileids()), "documents..."
print "The first five are:", texts.fileids()[:5]
unique_terms = list(set(texts.words()))
unique_terms_stemmed = list(set([st.stem(word) for word in unique_terms]))
print "Found a total of", len(unique_terms), "unique terms"
print "Found a total of", len(unique_terms_stemmed), "unique stemmed terms"

unique_terms = unique_terms_stemmed

# doucment frequency; in how many documents does the word occur
df = np.zeros(len(unique_terms))

def BOW(document):
    document = nltk.Text([st.stem(word) for word in texts.words((document))])
    tf = [] # term frequency; how often does the word occur in this doc
    for i,word in enumerate(unique_terms):
        count = document.count(word)
        tf.append(count)
        if count > 0:
          df[i] += 1
    return tf

vectors = [np.array(BOW(f)) for f in texts.fileids()]
print "Vectors created."
idSorted = np.argsort(df)
unique_terms_sorted = [unique_terms[i] for i in idSorted]
print "least frequent 10 words are", unique_terms_sorted[:10]
print df[idSorted[:10]]
print "most frequent 10 words are", unique_terms_sorted[-11:-1]
print df[idSorted[-11:-1]]
print "First 10 counts for first document are", vectors[0][0:10]

with open("./unique_terms.txt","w") as f:
  f.write(" ".join(unique_terms)+"\n")
  f.write(" ".join(["{}".format(int(dfw)) for dfw in df])+"\n")
