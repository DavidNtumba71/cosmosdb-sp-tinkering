'''script -> state a genere, then delete all movies matching'''
from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
import os

GENRE = 'Fantasy'
PARTITION_ATTRIBUTE = "primary_genre"


SPROC = "sp_delete_movies_of_genre"

load_dotenv()
URL             = os.getenv('COSMOS_URL')
KEY             = os.getenv('COSMOS_KEY')
client          = CosmosClient(URL, credential=KEY)
database        = client.get_database_client('demodb')

container   = database.get_container_client("movies")
result      = container.scripts.execute_stored_procedure(
                sproc=SPROC,
                params=[GENRE],
                partition_key=GENRE) 
print(result)