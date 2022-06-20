'''spefic a movie by id then update its prime genre'''
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from dotenv import load_dotenv
import os
#Brazil

id = "Citizen Kane"
partition_key = "Mystery"
genre = "Drama"
UPDATE_SPROC = "sp_update_genre"

load_dotenv()
URL             = os.getenv('COSMOS_URL')
KEY             = os.getenv('COSMOS_KEY')
client          = CosmosClient(URL, credential=KEY)
database        = client.get_database_client('demodb')

container   = database.get_container_client("movies")
result      = container.scripts.execute_stored_procedure(sproc=UPDATE_SPROC,params=[genre, id],partition_key=partition_key) 
print(result)
