build with docker 
====================
go to the [db.py](app/db.py) file and change database settings
```python 
DATABASE_URL = URL.create(
    drivername="postgresql+asyncpg",
    username="postgres", # change to what is a name in docker-compose.yml
    password="postgres", # change to what is a name in docker-compose.yml
    host="db", # change to what is a name in docker-compose.yml
    port=5432,
    database="gamedb"
)
``` 
```bash 
docker build -t game-config-service .
``` 
