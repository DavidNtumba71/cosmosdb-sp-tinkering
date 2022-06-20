'''pull a random movie then insert it into cosmos via sp'''

#*1. pulling the movie
from random import choice
import csv

def data_from_csv(file_name):
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        return [record for record in csv.DictReader(file, delimiter=';')]

random_movie = choice(data_from_csv("../Movies/movies_part_2.csv"))
import json
print(json.dumps(random_movie))
random_movie = json.dumps(random_movie)

#*2. uploading the movie
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from dotenv import load_dotenv
import os

INSERT_SPROC = "sp_insert_movie"

load_dotenv()
URL             = os.getenv('COSMOS_URL')
KEY             = os.getenv('COSMOS_KEY')
client          = CosmosClient(URL, credential=KEY)
database        = client.get_database_client('demodb')

container   = database.get_container_client("movies")
result      = container.scripts.execute_stored_procedure(sproc=INSERT_SPROC,params=[[random_movie]],partition_key="") 
print(result)