import redis
import os


pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST', 'localhost'), port=os.getenv('REDIS_PORT', '6379'))
r = redis.Redis(connection_pool=pool)


async def save_game(key: str, value: str):
    r.json().set(key, ".", value)

