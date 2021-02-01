import asyncio
import os

from .main import client


token = os.getenv("TOKEN")
client.run(token)
