Nutritional is a collection of scripts to interact with the [USDA
nutrition database](http://ndb.nal.usda.gov/).

-  [nutriParser](nutriParser.py) parses the raw USDA DB files and
   populates a SQLite database. You can download the resulting DB [here](http://jstraub.de/download/nutriDB/sr28asc.db).
-  [nutriCorpus](nutriCorpus.py) computes a list of unique terms from all food item
   descriptions and their frequency and writes them to a text file
   [./unique_terms.txt](http://jstraub.de/download/nutriDB/unique_terms.txt).
- [nutriRanking](nutriRanking.py) uses the SQLite DB as well as the
  term frequency file to compute a decluttered ranking of food items
  for each nutrient in [nutrientsBase.txt](./nutrientsBase.txt).

The USDA DB parser was inspired by the following projects:
[nutrient-db](https://github.com/schirinos/nutrient-db),
[django-usda](https://github.com/notanumber/django-usda) and
[nutritionparser](https://github.com/lnielsen/nutritionparser).
