from rest_framework.views import APIView
from rest_framework.response import Response
from elasticsearch import Elasticsearch

class ElasticsearchQueryView(APIView):
    def get(self, request, format=None):
        # Connect to Elasticsearch
        es = Elasticsearch(['localhost:9200'])

        # Extract query parameters from request
        query = request.query_params.get('query', '')
        index_name = request.query_params.get('index', 'your_default_index')

        # Query Elasticsearch
        try:
            response = es.search(index=index_name, body={'query': {'match': {'content': query}}})
            hits = response['hits']['hits']
            # Process hits as needed
            return Response(hits)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
