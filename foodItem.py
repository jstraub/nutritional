import nltk, re, string
import numpy as np
from nltk.stem.lancaster import *
st = LancasterStemmer()

def BOW(tokens, bowTerms):
    document = nltk.Text(tokens)
    tf = [] # term frequency; how often does the word occur in this doc
    for i,word in enumerate(bowTerms):
        count = document.count(word)
        tf.append(count)
    return tf

class FoodItem(object):
  def __init__(self, foodDesc):
    self.foodDesc = foodDesc
    self.NDB_No = foodDesc[0]
    self.longDesc = re.sub('['+string.punctuation+']', '', foodDesc[2])
    self.tokens = [st.stem(word) for word in nltk.word_tokenize(self.longDesc)]
    self.nutrients = dict()

  def GetDescription(self):
    return self.foodDesc[2]

  def GetTFIDF(self, bowTerms, df):
    self.tf = np.array(BOW(self.tokens, bowTerms))
    self.tfidf = np.nan_to_num(self.tf/df)
#    print 'len', np.sqrt((self.tfidf**2).sum())
    self.tfidf /= np.sqrt((self.tfidf**2).sum())
    return self.tfidf

  def ComputeTFIDFangle(self, foodB, bowTerms, df):
    tfA = self.GetTFIDF(bowTerms, df)
    tfB = foodB.GetTFIDF(bowTerms, df)
    return np.arccos(min(1.,max(-1.,tfA.dot(tfB))))*180./np.pi

  def AddNutrient(self, nutrient):
    self.nutrients[nutrient.GetName()] = nutrient
  def GetNutrient(self, nutrientName):
    return self.nutrients[nutrientName]

  def LoadNutrients(self, c, nutriFilter):
    c.execute('SELECT * FROM NUT_DATA WHERE NDB_No="{}"'.format(self.NDB_No))
    nutris = dict()
    for nutri in c.fetchall():
      nutris[nutri[1]] = nutri
    self.x = np.zeros(len(nutriFilter))
    for i,nutri in enumerate(nutriFilter): 
      if nutri in nutris.keys():
        self.x[i] = float(nutris[nutri][2])

