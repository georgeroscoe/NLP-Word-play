#!python3

import requests
import nltk
from functools import reduce
from nltk.corpus import stopwords
from datamuse import datamuse

api = datamuse.Datamuse()

def not_stopword(w):
  return w['word'] not in stopwords.words('english') and w['word'] != '.'

print("Input word:")
word = input()
test_succeeding_word = api.words(rel_bga=word)
test_preceding_word = api.words(rel_bgb=word)

succeeding_words = list(filter(not_stopword, test_succeeding_word))
preceding_words = list(filter(not_stopword, test_preceding_word))

after_total_score = reduce(lambda acc, w: acc + w['score'], succeeding_words, 0)
before_total_score = reduce(lambda acc, w: acc + w['score'], preceding_words, 0)

lst = []
lst2 = []

after_words = [i.get('word') for i in succeeding_words]
after_word_score = [ (i.get('score') / after_total_score)*100 for i in succeeding_words]
lst = list(zip(after_words, after_word_score))
shortened_lst = [i for i in lst if i[1] > 2]


before_words = [i.get('word') for i in preceding_words]
before_word_score = [ (i.get('score') / before_total_score)*100 for i in preceding_words]
lst2 = list(zip(before_words, before_word_score))
shortened_lst2 = [i for i in lst2 if i[1] > 2]

print()
print("Preceding words:")
if not lst2:
    print("No preceding words")

for a,b in shortened_lst2:
    print(a,"{:.2f}".format(b) + "%")

print()
print("Succeeding words:")

if not lst:
    print("No succeeding words")

for a,b in shortened_lst:
    print(a,"{:.2f}".format(b) + "%")
