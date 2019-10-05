"""
Sorts a set of Documents using Natural Language Processing
"""
class DocumentSorter:
	threshold = 89.5
	def __init__(self, files: dict, npl):
		self.files = files
		self.npl = npl

	def check_for_similar(self, path, file):
		similar = dict()
		for other_path, other_file in self.files:
			if other_path != path:
				main_doc = self.npl(file)
				other_doc = self.npl(other_file)
				similarity = main_doc.similarity(other_doc)
				print(similarity)
				if similarity >= DocumentSorter.threshold:
					similar[other_path] = other_file
