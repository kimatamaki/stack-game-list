import requests
import json
from settings import (STEAMID, API_KEY)

response_json = requests.get(
    f'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={STEAMID}&format=json&include_appinfo=1&include_played_free_games=true'
    ).json()
# ~~ response sample
#{
#  "response": {
#    "game_count": 494,
#    "games": [
#      {
#        "appid": 4000,
#        "name": "Garry's Mod",
#        "playtime_forever": 0,
#        "img_icon_url": "4a6f25cfa2426445d0d9d6e233408de4d371ce8b",
#        "img_logo_url": "70ef9d2ec9f0f4560c3cb9fee6cc3665c93c8d0c",
#        "has_community_visible_stats": true,
#        "playtime_windows_forever": 0,
#        "playtime_mac_forever": 0,
#        "playtime_linux_forever": 0
#      },
#      .
#      .
#      .
#  }
#}
game_count = response_json['response']['game_count']
print('所持ゲーム数：{}'.format(game_count))
games = []
for game in response_json['response']['games']:
    games.append(
        {
            "appid": game['appid'],
            "name": game['name'],
            "img_logo_url": f"http://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_logo_url']}.jpg",
            "img_icon_url": f"http://media.steampowered.com/steamcommunity/public/images/apps/{game['appid']}/{game['img_icon_url']}.jpg",
        }
    )
print('')
print('============ 所持ゲーム一覧 ============')
for game in games:
    print('{} : {}'.format(game['name'], game['img_logo_url']))
