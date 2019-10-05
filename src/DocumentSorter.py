"""
Sorts a set of Documents using Natural Language Processing
"""
from collections import Counter


class DocumentSorter:
	threshold = 89.5

	def __init__(self, files, nlp):
		self.files = files
		self.nlp = nlp

	def intersection(self, lst1, lst2):
		lst3 = [value for value in lst1 if value in lst2]
		return lst3

	def check_for_similar(self, path, file):
		similar = dict()
		for other_path, other_file in self.files.items():
			if other_path != path:
				main_doc = self.nlp(file)
				other_doc = self.nlp(other_file)
				main_doc_no_stop = self.nlp(' '.join([str(t) for t in main_doc if not t.is_stop]))
				other_doc_no_stop = self.nlp(' '.join([str(t) for t in other_doc if not t.is_stop]))
				similarity = main_doc_no_stop.similarity(other_doc_no_stop)
				print(similarity)
				if similarity >= DocumentSorter.threshold:
					similar[other_path] = other_file

	def most_similar(self, word, i):
		queries = [w for w in word.vocab if w.is_lower == word.is_lower and w.prob >= -15]
		by_similarity = sorted(queries, key=lambda w: word.similarity(w), reverse=True)
		return [w.lower_ for w in by_similarity[:i]]

	def category_name_for(self, file1, file2):
		file1_nouns = [token.text for token in self.nlp(file1) if
					   token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN"]
		file1_counter = Counter(file1_nouns)
		file2_nouns = [token.text for token in self.nlp(file2) if
					   token.is_stop != True and token.is_punct != True and token.pos_ == "NOUN"]
		file2_counter = Counter(file2_nouns)
		file1_noun = file1_counter.most_common(1)[0][0]
		file2_noun = file2_counter.most_common(1)[0][0]
		file1_similar = self.most_similar(self.nlp.vocab[file1_noun], 100)
		file2_similar = self.most_similar(self.nlp.vocab[file2_noun], 100)
		print(file1_similar)
		print(file2_similar)
		print(self.intersection(file1_similar, file2_similar))
		print(file1_noun)
		print(file2_noun)
