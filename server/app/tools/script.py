#!/usr/bin/python3

import sys
import os 
from searcher import InvertedSolution


script_dir = os.path.dirname(__file__)
data_path = os.path.relpath('../data/cooking_books.tsv', script_dir)
search_query = " ".join(sys.argv[1:])
s = InvertedSolution(data_path)

print ("\n".join('{} {} {}'.format(*entry) for entry in s.search(search_query)))