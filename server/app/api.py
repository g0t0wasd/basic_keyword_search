from flask_restful import Resource, Api
from app import app
from app.tools.searcher import InvertedSolution
from time import sleep, time

api = Api(app)

# API
class SearchBooksAPI(Resource):
	def get(self, query):
		start = time()
		s = InvertedSolution("app/data/cooking_books.tsv")
		data = s.search(query)
		end = time()
		total_time = end - start
		total_results = len(data)
		return {'results': data, 'time': "{:02f}".format(total_time), "total_results": total_results}

class BookDetailsAPI(Resource):
	def get(self, book_id):
		s = InvertedSolution("app/data/cooking_books.tsv")
		data = s.get_data()
		sleep(3)
		details = data.get(book_id, "")

		return {'details': details}

api.add_resource(SearchBooksAPI, '/api/search/<string:query>')
api.add_resource(BookDetailsAPI, '/api/details/<string:book_id>')
