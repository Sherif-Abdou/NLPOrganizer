"""
Sorts a set of Documents using Natural Language Processing
"""
from collections import Counter
import json
from os import path


class DocumentSorter:
    # The threshold for when two files are considered similar
    threshold = 0.85

    def __init__(self, files, nlp):
        self.files = files
        self.nlp = nlp
        self.cache_path = path.join(path.dirname(__file__), "cache")
        self.cache = dict()
        self.loadcache()

    def loadcache(self):
        # Make sure the path exists, if not create it
        if not path.exists(self.cache_path):
            return
        else:
            with open(self.cache_path, "r") as file:
                self.cache = json.load(file)

    def savecache(self):
        with open(self.cache_path, "w") as file:
            json.dump(self.cache, file)

    # Determines what files are similar to a given file
    def check_for_similar(self, path: str, file: str):
        similar = []
        for other_rawfile in self.files:
            other_path = other_rawfile.path
            other_file = other_rawfile.contents
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
                    similar.append((other_rawfile, similarity))
        return similar

    # Finds the i most similar words to a given word
    def most_similar(self, word, i):
        if word in self.cache:
            return self.cache[word]
        lexeme = self.nlp.vocab[word]
        queries = [w for w in lexeme.vocab if w.is_lower ==
                   lexeme.is_lower and w.prob >= -15 and w.has_vector and w.vector_norm]
        by_similarity = sorted(
            queries, key=lambda w: lexeme.similarity(w), reverse=True)
        output = [w.lower_ for w in by_similarity[:i]]
        self.cache[word] = output
        return output

    # Determines a category name
    def category_name_for(self, category):
        # Finds the 5 most common nouns in each document
        top_nouns = []
        for file in category.files:
            file_nouns = [token.text for token in self.nlp(file.contents) if
                          token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN"]
            file_counter = Counter(file_nouns)
            file_top = file_counter.most_common(5)
            top_nouns.append(
                (file_top, path.basename(file.path).split(".")[0]))

        # Scores the similar words of each noun based on number if appearances and similarity to original noun
        scores = dict()
        for tops, name in top_nouns:
            i = 1
            for top, _ in tops:
                for similar in self.most_similar(top, 50):
                    if similar == top:
                        continue
                    if similar in scores:
                        scores[similar] += 1 / i
                    else:
                        scores[similar] = 1 / i
                i += 0.1

        # Looks through the scores to find the highest scoring word
        curr_word = ""
        curr_score = float("-inf")
        for word, score in scores.items():
            if score > curr_score:
                curr_word = word
                curr_score = score
        self.savecache()
        # Outputs the highest scoring word
        category.name = curr_word
        return
