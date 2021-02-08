import requests
from settings import (STEAMID, API_KEY)

r = requests.get(f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAMID}&format=json&include_appinfo=1')
print(r.json())
