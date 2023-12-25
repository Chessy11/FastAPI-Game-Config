import os
import redis
from rejson import Client, Path
import json
import traceback

rj = Client(host=os.getenv('REDIS_HOST', 'redis'), port=os.getenv('REDIS_PORT', '6379'), decode_responses=True)

async def save_game(key: str, value: str):
    # Set a JSON value
    rj.jsonset(key, Path.rootPath(), value)

async def delete_game(key: str):
    # Delete a key
    rj.delete(key)

def get_game_sync(key: str):
    try:
        # Use jsonget to retrieve JSON data
        game_data = rj.jsonget(key, Path.rootPath())

        # Debugging
        print(f"Type of game_data: {type(game_data)}")
        print(f"Content of game_data: {game_data}")

        if game_data is None:
            return None

        # If game_data is bytes, decode it
        if isinstance(game_data, bytes):
            game_data = game_data.decode('utf-8')

        # Since jsonget should return a Python object, no need to parse JSON
        return game_data
    except Exception as e:
        print(f"Error retrieving data for key {key}: {e}")
        print(f"Exception Traceback: {traceback.format_exc()}")
        raise e


