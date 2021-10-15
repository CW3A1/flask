import os

db_url = f"http://{os.getenv('db_host')}:{os.getenv('db_port')}"
db_secret = os.getenv('db_secret')