import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)


async def save_game(key: str, value: str):
    r.json().set(key, ".", value)

