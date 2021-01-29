import asyncio

from .main import client
from .main import get_token


token = asyncio.run(get_token())
client.run(token)
