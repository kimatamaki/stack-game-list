import os
import requests
import json

def load_settings(settings):
    if os.path.exists('./settings.json'):
        with open('./settings.json') as f:
            settings = json.load(f)
    else:
        print('\nPlease Input Your Steam Web API Key And SteamId')
        settings['SteamWebAPI']['API_KEY'] = input('API Key :')
        settings['SteamWebAPI']['STEAM_ID'] = input ('steamId :')

        with open('./settings.json', 'w') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    return settings

def main():
    settings = {}
    settings = load_settings({'SteamWebAPI':{'API_KEY':'','STEAM_ID':'',}})
    api_url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': settings['SteamWebAPI']['API_KEY'],
        'steamid': settings['SteamWebAPI']['STEAM_ID'],
        'format': 'json',
        'include_played_free_games': True,
        'include_appinfo': True,
    }
    response_json = requests.get(api_url, params=params).json()
    game_count = response_json['response']['game_count']
    print('所持ゲーム数：{}'.format(game_count))
    games = []
    img_url_format = 'http://media.steampowered.com/steamcommunity/public/images/apps/{}/{}.jpg'
    for game in response_json['response']['games']:
        games.append(
            {
                "appid": game['appid'],
                "name": game['name'],
                "img_logo_url": img_url_format.format(game['appid'],game['img_logo_url'] ),
                "img_icon_url": img_url_format.format(game['appid'],game['img_icon_url'] ),
            }
        )
    print('')
    print('============ 所持ゲーム一覧 ============')
    for game in games:
        print('{} : {}'.format(game['name'], game['img_logo_url']))

if __name__ == '__main__':
    main()

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
