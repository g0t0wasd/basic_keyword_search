import csv
import re


def normalize_string(pattern, string):
	""" Makes list of words from string, based on regular expression pattern """
	return re.split(pattern, string.lower())

class DataLoader:
	def __init__(self, file):
		self.file = file
		self.load_data()

	def load_data(self):
		""" Loads data from file. Automatically checks delimiter type """
		with open(self.file) as data_f:
			dialect = csv.Sniffer().sniff(data_f.read(1024))
			data_reader = csv.reader(data_f, dialect)
			self.data = tuple(data_reader)

	def get_normalized_data(self):
		self.normalize_data()
		return self.normalized_data

	def get_id_name_norm(self, entry):
		""" Returns Book ID, book name, normalized book name """
		book_id = entry[0]
		original_name = entry[1]
		normalized_name = normalize_string("[., \-!?:()]+", entry[1])
		return book_id, original_name, normalized_name

	def normalize_data(self):
		""" Sets data as a dict with ID as a key and tuple (name, normalized name) as value """
		self.normalized_data = {}
		for entry in self.data:
			book_id, original_name, normalized_name = self.get_id_name_norm(entry)
			self.normalized_data[book_id] = (original_name, normalized_name)

	def get_inverted_data(self):
		self.invert_data()
		return self.inverted_data

	def invert_data(self):
		""" Creates a dict with word as a key and book ids as values """
		self.inverted_data = {}
		for entry in self.data:
			book_id, original_name, normalized_name = self.get_id_name_norm(entry)
			for word in normalized_name:
				if word not in self.inverted_data:
					self.inverted_data[word] = [book_id]
				else:
					self.inverted_data[word].append(book_id)

class Searcher:
	def __init__(self, file_name):
		data_loader = DataLoader(file_name)
		self.data = data_loader.get_normalized_data()

	def calculate_exact_match(self, query, name):
		""" Calculates number of repetitions of words from query in name """
		match = 0
		for item in query:
			match += name.count(item)
		return match

	def format_output(self, data):
		""" Sets output in format: ID name score """
		return "\n".join('{} {} {}'.format(*entry) for entry in data)

	def get_results(self, query):
		output = []
		for book_id, value in self.data.items():
			name = value[0]
			normalized_name = value[1]
			intersection = set(query).intersection(set(normalized_name))
			match_rate = len(intersection)
			if match_rate:
				match_rate = self.calculate_exact_match(query, normalized_name)
				output.append((book_id, name, match_rate))
		return output

	def search(self, query):
		""" Main searching function """
		normalized_query = normalize_string("[., \-!?:()]+", query)
		search_results = self.get_results(normalized_query)
		sorted_results = self.sort_results(search_results)
		return self.format_output(sorted_results)

	def sort_results(self, results):
		""" Sorts results by score from highest to lowest """
		return sorted(results, key=lambda x: x[2], reverse=True)


class InvertedSolution(Searcher):
	def __init__(self, file_name):
		data_loader = DataLoader(file_name)
		self.data = data_loader.get_normalized_data()
		self.inverted_data = data_loader.get_inverted_data()

	def search(self, query):
		book_ids = []
		normalized_query = normalize_string("[., \-!?:()]+", query)
		for word in normalized_query:
			if word in self.inverted_data.keys():
				book_ids.extend(self.inverted_data[word])
		book_ids = set(book_ids)

		output = []
		for book_id in book_ids:
			name = self.data[book_id][0]
			normalized_name = self.data[book_id][1]
			match_rate = self.calculate_exact_match(normalized_query, normalized_name)
			output.append((book_id, name, match_rate))

		sorted_results = self.sort_results(output)
		return self.format_output(sorted_results)

if __name__ == "__main__":
	print ("Invoking testing procedure")
	s = Searcher("test.tsv")
	si = InvertedSolution("test.tsv")
	assert s.search("Julia").split()[-1] == '2', "there should be 2 mentions of word Julia"
	assert s.search("Julia") == si.search("Julia"), "original and inverted search should match here!"
	assert s.search("Kitchen") == s.search("KITCHEN") == s.search("kItChen"), "Case should not affect search"
	assert "The All-American Cowboy Cookbook" in s.search("300 recipes from").split("\n")[0], "Cowboy Cookbook should be top result"
	from time import time
	simple_start_time = time()
	s.search("Swap BoTTle!")
	simple_end_time = time()
	inverted_start_time = time()
	si.search("Swap BoTTle!")
	inverted_end_time = time()
	simple_time = simple_end_time - simple_start_time
	inverted_time = inverted_end_time - inverted_start_time
	assert inverted_time < simple_time, "Inverted should be faster"