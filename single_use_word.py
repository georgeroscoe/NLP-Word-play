#!python3
import sys

from functools import reduce
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.corpus import words as wd
from datamuse import datamuse
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

api = datamuse.Datamuse()


def show_stopwords():
    choice = input("Type S to show stopwords, any other key to not show: ").lower()

    if choice == "s":
        return True
    else:
        return False


def preceding_or_succeeding():
    word_type = input("Type P for preceding word, or S for succeeding: ").lower()

    if word_type == "p":
        return 'before'
    elif word_type == "s":
        return 'after'
    else:
        print("Invalid character, please try again: ")
        preceding_or_succeeding()


def words_generator(word, position):
    if position == 'before':
        return api.words(rel_bgb=word)
    elif position == 'after':
        return api.words(rel_bga=word)


def not_word_remover(words):
    for word in words:
        if not word[0] in wd.words():
            words.remove(word)
    return words


def stopword_remover(words):
    stop_words = set(stopwords.words('english'))
    new_words = [w for w in words if w[0] not in stop_words]
    return new_words


def score_generator(words):
    total_score = reduce(lambda acc, w: acc + w['score'], words, 0)

    return [(i.get('score') / total_score) * 100 for i in words]


def words_score_zipper(word, position):
    words = [i.get('word') for i in words_generator(word, position)]

    real_words = not_word_remover(words)

    word_score = score_generator(words_generator(word, position))

    return list(zip(real_words, word_score))


def duplicate_remover(words, stopwords_removed=False):
    lemmatized_lst = []

    if stopwords_removed:
        words = stopword_remover(words)

    # Create list of words by their lemmatized form, plus their score
    for word in words:
        raw = wordnet_lemmatizer.lemmatize(word[0])
        lemmatized_lst.append((raw, word[1]))

    d = defaultdict(list)

    # Convert to a default dict, combining all words with the same lemmatized form
    for k, v in lemmatized_lst:
        d[k].append(v)

    # Sum up all words with the same lemmatized form and make that the new score
    for k, v in d.items():
        word_sum = reduce((lambda x, y: x + y), v)

        d[k] = word_sum

    # Convert back to a list
    lst = [(k, v) for k, v in d.items()]
    return sorted(lst, key=lambda x: x[1], reverse=True)


def results_format(input_word, word_score_list, position):
    print("Inputted word:")
    print("  {}".format(input_word))
    print()
    print("Preceding words: ") if position == 'before' else print("Succeeding words: ")
    for word, score in word_score_list:
        print("  " + word, "{:.2f}".format(score) + "%")


def end_of_run_options():
    choice = input("Type A to choose another word or any other key to quit: ").lower()

    if choice == "a":
        run_module()
    else:
        sys.exit()


def run_module():
    print("Please input word:")
    input_word = input()
    list_position = preceding_or_succeeding()
    words_and_score = words_score_zipper(input_word, list_position)
    duplicates_and_stopwords_removed = duplicate_remover(words_and_score, stopwords_removed=True)

    showing_stopwords = show_stopwords()

    if showing_stopwords:
        duplicates_removed = duplicate_remover(words_and_score)
        print()
        print("Stopwords included list:")
        results_format(input_word, duplicates_removed, list_position)
    print()
    print("Stopwords removed list:")
    results_format(input_word, duplicates_and_stopwords_removed, list_position)

    end_of_run_options()


if __name__ == "__main__":
    run_module()
