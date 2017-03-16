#!/usr/bin/python3

import sys
from searcher import Searcher

search_query = " ".join(sys.argv[1:])
s = Searcher("cooking_books.tsv")

print ("\n".join('{} {} {}'.format(*entry) for entry in s.search(search_query)))