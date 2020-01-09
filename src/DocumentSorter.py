"""
Sorts a set of Documents using Natural Language Processing
"""
from collections import Counter
from typing import List
from src.File import File
from src.Category import Category
import json
from os import path


class DocumentSorter:
    # The threshold for when two files are considered similar
    threshold = 0.86
    append_threshold = 0.88

    def __init__(self, files: List[File], nlp):
        self.files = files
        self.nlp = nlp
        self.cache_path = path.join(path.dirname(__file__), "cache")
        self.cache = dict()
        self.__load_cache()

    def __load_cache(self):
        # Make sure the path exists, if not create it
        if not path.exists(self.cache_path):
            return

        with open(self.cache_path, "r") as file:
            self.cache = json.load(file)

    def __save_cache(self):
        with open(self.cache_path, "w") as file:
            json.dump(self.cache, file)

    # Determines what files are similar to a given file
    def check_for_similar(self, path: str, file: str):
        similar = []
        for other_raw_file in self.files:
            other_path = other_raw_file.path
            other_file = other_raw_file.contents
            if other_path != path:
                # Loads each file into Spacy's Natural Language Processing
                main_doc = self.nlp(file)
                other_doc = self.nlp(other_file)
                # Removes useless stop words from each file
                main_doc_no_stop = self.nlp(
                    ' '.join([str(t) for t in main_doc if not t.is_stop]))
                other_doc_no_stop = self.nlp(
                    ' '.join([str(t) for t in other_doc if not t.is_stop]))
                # Compares the two files' similarity
                similarity = main_doc_no_stop.similarity(other_doc_no_stop)
                if similarity >= DocumentSorter.threshold:
                    similar.append((other_raw_file, similarity))
        return similar

    # Finds the i most similar words to a given word
    def most_similar(self, word, i):
        # Don't recalculate word if already in cache
        if word in self.cache:
            return self.cache[word]

        # Collect all word vectors in the nlp dictionary
        lexeme = self.nlp.vocab[word]
        queries = [w for w in lexeme.vocab if w.is_lower ==
                   lexeme.is_lower and w.prob >= -15 and w.has_vector and w.vector_norm]

        # Sort the nlp dictionary by similarity to given word and collect the top i
        by_similarity = sorted(
            queries, key=lambda w: lexeme.similarity(w), reverse=True)
        output = [w.lower_ for w in by_similarity[:i]]
        self.cache[word] = output
        return output

    # Determines a category name
    def category_name_for(self, category: Category):
        # Finds the 5 most common nouns in each document
        top_nouns = []
        for file in category.files:
            file_nouns = [token.text for token in self.nlp(file.contents) if
                          token.is_stop is not True and token.is_punct is not True and token.pos_ == "NOUN"]
            file_counter = Counter(file_nouns)
            file_top = file_counter.most_common(5)
            top_nouns.append(
                (file_top, path.basename(file.path).split(".")[0]))

        scores = self.__get_scores(top_nouns)

        curr_word = self.__highest_scoring_word(scores)

        # Updates the internal cache
        self.__save_cache()
        # Outputs the highest scoring word
        category.name = curr_word
        return

    # Looks through the scores to find the highest scoring word
    @staticmethod
    def __highest_scoring_word(scores):
        curr_word = ""
        # Start at the lowest possible value
        curr_score = float("-inf")

        # Looks through each for the highest value
        for word, score in scores.items():
            if score > curr_score:
                curr_word = word
                curr_score = score
        return curr_word

    # Scores the similar words of each noun based on number if appearances and similarity to original noun
    def __get_scores(self, top_nouns):
        scores = dict()
        for tops, name in top_nouns:
            i = 1
            for top, _ in tops:
                # Ignore if there is not a vector
                if self.nlp.vocab[top].vector_norm == 0:
                    continue

                # Add scores for the top similar words
                for similar in self.most_similar(top, 50):
                    if similar == top:
                        continue

                    if similar in scores:
                        scores[similar] += 1 / i
                    else:
                        scores[similar] = 1 / i
                i += 0.1
        return scores
