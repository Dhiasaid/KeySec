# Create a new Django management command file: management/commands/create_index.py

from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch

class Command(BaseCommand):
    help = 'Creates an Elasticsearch index'

    def handle(self, *args, **options):
        # Connect to Elasticsearch
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        # Define index settings and mappings
        index_body = {
            'settings': {
                'number_of_shards': 1,
                'number_of_replicas': 1
            },
            'mappings': {
                'properties': {
                    'title': {'type': 'text'},
                    'description': {'type': 'text'}
                    # Add more fields and their mappings as needed
                }
            }
        }

        # Create the index
        index_name = 'KeySec'
        es.indices.create(index=index_name, body=index_body)

        self.stdout.write(self.style.SUCCESS(f'Index "{index_name}" created successfully.'))
