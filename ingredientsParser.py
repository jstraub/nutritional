#http://allrecipes.com/recipe/173730/kale-and-banana-smoothie/
from lxml import html
import requests
import nltk, re
import numpy as np
import sqlite3


if False:
  page = requests.get('http://allrecipes.com/recipe/173730/kale-and-banana-smoothie/')
  tree = html.fromstring(page.content)
  ingredients = tree.xpath('//span[@itemprop="ingredients"]/text()')
ingredients = ['1 banana', '2 cups chopped kale', '1/2 cup light unsweetened soy milk', '1 tablespoon flax seeds', '1 teaspoon maple syrup']

units = ["cup", "teaspoon", "tablespoon"]
class Ingredient(object):
  def __init__(self):
    self.amount = 1
    self.unit = "piece"
    self.item = []

  def setAmount(self,token):
    if re.search("[0-9]+|[0-9]*[ ]*[1-9]+\/[1-9]+",token):
      self.amount = token
      return True
    return False
  def setUnit(self,token):
    if token in units:
      self.unit = token
      return True
    return False
  def setItem(self,token):
    # TODO this might start checking the nutritional database
    self.item.append(token)
    return True

  def parseTokens(self,tokens):
    state = "start"
    for t in tokens:
      if state == "start":
        if self.setAmount(t):
          state = "amount"
        elif self.setUnit(t):
          self.amount = 1 
          state = "unit"
        elif self.setItem(t):
          self.amount = 1 
          self.unit = "piece"
          state = "item"
      elif state == "amount":
        if self.setUnit(t):
          state = "unit"
        elif self.setItem(t):
          self.unit = "piece"
          state = "item"
      elif state == "unit":
        if self.setItem(t):
          state = "item"
      elif state == "item":
        self.item.append(t) 

conn = sqlite3.connect("sr28asc.db")
c = conn.cursor()

print ingredients
stemmer = nltk.PorterStemmer()
for ingredient in ingredients:
  tokens = nltk.word_tokenize(ingredient)
  stemmed = [stemmer.stem(t) for t in nltk.word_tokenize(ingredient)]
#  print tokens
  # amount in decimal number or word or nothing (in which case 1)
  # unit
  # ingredient
  ing = Ingredient()
  ing.parseTokens(stemmed)
  print ing.amount, ing.unit, ing.item
  res = []
  for item in ing.item: 
    c.execute('SELECT Long_Desc FROM FOOD_DES WHERE Long_Desc LIKE "%{}%"'.format(item))
    res += c.fetchall()
  descs = [r[0] for r in res]
  print len(descs)
  scores = []
  for desc in descs:
    starts = []
    for item in ing.item: 
#      print item, desc
      m = re.search(item.lower(), desc.lower());
      if m:
        starts.append(m.start(0))
    score = starts[0] / float(len(starts))
    for start in starts[1:]:
      score += start / float(len(starts))
    scores.append(score)
  idSorted = np.argsort(np.array(scores))
  for id in idSorted[:5]:
    print descs[id]
#  for i in range(len(ing.item)-1): 
#    c.execute('SELECT Long_Desc FROM FOOD_DES WHERE Long_Desc LIKE "%{}%{}%"'.format(ing.item[i],ing.item[i+1]))
#    res += c.fetchall()
#  print len(res)
conn.close()
