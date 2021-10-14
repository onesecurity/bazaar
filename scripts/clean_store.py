# This script will delete the APK that are missing from the Elastic Search index form the store. It is for development and bug fixes. 


# docker-compose -f production.yml stop django worker
# docker-compose -f production.yml run --rm django python manage.py shell

from django.core.files.storage import default_storage
from django.conf import settings
from elasticsearch import Elasticsearch

es = Elasticsearch([settings.ELASTICSEARCH_HOST], timeout=30, max_retries=5, retry_on_timeout=True)
original_index = settings.ELASTICSEARCH_APK_INDEX
tmp_index = f'{original_index}_tmp'

# Get all APKs from the store
_, hashes = default_storage.listdir('.')
for hash in hashes:
    # Check if it exists on the ES:
    if not es.exists(original_index, id=hash):
        default_storage.delete(hash)
