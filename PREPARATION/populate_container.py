'''script -> take from csv && place in cosmos db container'''
from dotenv import load_dotenv
from azure.cosmos import CosmosClient, PartitionKey, exceptions
import os, csv

PARTITION_ATTRIBUTE = "primary_genre"

'''1. process csv'''
def data_from_csv(file_name):
    with open(file_name, 'r', encoding='utf-8-sig') as file:
        return [record for record in csv.DictReader(file, delimiter=';')]
    
def set_primary_genre(record):
    record[f'{PARTITION_ATTRIBUTE}'] = record['genres'].split('|')[0]
    return record

def map_identifiers(record):
    record['RowID'] = record['id']
    record['id'] = record['original_title']
    return record
    
data = data_from_csv('../Movies/movies_part_1.csv')

for operation in (set_primary_genre, map_identifiers):
    data = [operation(record) for record in data]

'''2. connect to cosmos'''
load_dotenv()
URL             = os.getenv('COSMOS_URL')
KEY             = os.getenv('COSMOS_KEY')
client          = CosmosClient(URL, credential=KEY)
database        = client.get_database_client('demodb')

def init_container(container_name, partition_key):
    try:
        return database.create_container(container_name, partition_key)
    except exceptions.CosmosResourceExistsError:
        return database.get_container_client(container_name)
    
container = init_container("movies", PartitionKey(path=f"/{PARTITION_ATTRIBUTE}"))

'''3. upload to cosmos'''
import asyncio
async def upload_movies(container, movies):
    tasks  = (upload_task(container, movies[index]) for index, movie in enumerate(movies) if index <= 3000)
    await asyncio.gather(*tasks)
    print(f'all {len(movies)} movies uploaded!')
 
async def upload_task(container, movie):
    print(f"uploading movie {movie['id']}")
    return await asyncio.create_task(container.upsert_item(movie))

asyncio.run(upload_movies(container, movies = data))     