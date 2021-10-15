from os import getenv

db_host = getenv('db_host')
db_port = getenv('db_port')
db_url = f"http://{db_host}:{db_port}"
db_secret = getenv('db_secret')