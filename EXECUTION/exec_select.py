'''specify a year then sproc-query all the movies before that year'''
from azure.cosmos import CosmosClient, PartitionKey
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
import os


YEARS_AGO = 30
release_date = (datetime.today() - relativedelta(years= YEARS_AGO))
release_date = datetime.strftime(release_date, '%Y-%m-%d')

partition_key = "Comedy"
SELECT_SPROC = "sp_select_movies_before_year"

load_dotenv()
URL             = os.getenv('COSMOS_URL')
KEY             = os.getenv('COSMOS_KEY')
client          = CosmosClient(URL, credential=KEY)
database        = client.get_database_client('demodb')

container   = database.get_container_client("movies")
result      = container.scripts.execute_stored_procedure(
                sproc=SELECT_SPROC,
                params=[release_date],
                partition_key=partition_key) 
print(result)
