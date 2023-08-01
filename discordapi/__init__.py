import requests, json

from .secrets import CLIENT_ID, CLIENT_SECRET, BOT_TOKEN

API_ENDPOINT = 'https://discord.com/api/v10'
USERS_ENDPOINT = 'https://discord.com/api/users/@me'
HOST = 'http://localhost:1234'
BOT_AUTH_URL = 'https://discord.com/api/oauth2/authorize?client_id=%s&permissions=8&scope=bot' % CLIENT_ID

from .endpoints import *
