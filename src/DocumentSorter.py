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
		file1_top = file1_counter.most_common(5)
		file2_top = file2_counter.most_common(5)
		scores = dict()

		for tops in [file1_top, file2_top]:
			i = 1
			for top, _ in tops:
				for similar in self.most_similar(self.nlp.vocab[top], 50):
					if similar in scores:
						scores[similar] += 1/i
					else:
						scores[similar] = 1/i
				i += 0.1

		curr_word = ""
		curr_score = float("-inf")
		for word, score in scores.items():
			if score > curr_score:
				curr_word = word
				curr_score = score
		print(curr_word)
		print(curr_score)