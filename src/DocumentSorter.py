"""
Sorts a set of Documents using Natural Language Processing
"""
class DocumentSorter:
	threshold = 89.5
	def __init__(self, files, nlp):
		self.files = files
		self.nlp = nlp

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
