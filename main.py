import os
import requests
import json
from trello import TrelloClient

def load_settings(settings):
    use_trello = False
    if os.path.exists('./settings.json'):
        with open('./settings.json') as f:
            settings = json.load(f)
        choice = input('\nDo you want to output to Trello? [y/N]').lower()
        if choice in ['y', 'yes']:
            use_trello = True
    else:
        print('\nPlease Input Your Steam Web API Key And SteamId')
        settings['SteamWebAPI']['API_KEY'] = input('API Key :')
        settings['SteamWebAPI']['STEAM_ID'] = input ('steamId :')

        choice = input('\nDo you want to output to Trello? [y/N]').lower()
        if choice in ['y', 'yes']:
            use_trello = True

            print('\nPlease Input Your Trello API Key, API Secret Key And Token')
            settings['Trello']['API_KEY'] = input('API Key :')
            settings['Trello']['API_SECRET'] = input('API Secret Key :')
            settings['Trello']['TOKEN'] = input ('token :')

            print('\nPlease Input Your Trello Board Id And List Id')
            settings['Trello']['BOARD_ID'] = input('Board Id :')
            settings['Trello']['LIST_ID'] = input ('List Id :')

        with open('./settings.json', 'w') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

    return settings, use_trello

def get_games(settings):
    api_url = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    params = {
        'key': settings['SteamWebAPI']['API_KEY'],
        'steamid': settings['SteamWebAPI']['STEAM_ID'],
        'format': 'json',
        'include_played_free_games': True,
        'include_appinfo': True,
    }
    response_json = requests.get(api_url, params=params).json()
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
    return games

def output_to_trello(settings, games):
    client = TrelloClient(
        api_key=settings['Trello']['API_KEY'],
        api_secret=settings['Trello']['API_SECRET'],
        token=settings['Trello']['TOKEN'],
    )
    board = client.get_board(settings['Trello']['BOARD_ID'])
    target_list = board.get_list(settings['Trello']['LIST_ID'])
    labels = [v for v in board.get_labels() if v.name == 'Steam']
    if len(labels) < 1:
        board.add_label(name='Steam',color='black')
        labels = [v for v in board.get_labels() if v.name == 'Steam']

    exists_cards = []
    for card in board.get_cards(card_filter='open'):
        if 'Steam' in [v.name for v in card.labels if v.name is not None]:
            exists_cards.append(card)
    exists_appid_list = [json.loads(v.desc)['appid'] for v in exists_cards]

    for game in games:
        if game['appid'] in exists_appid_list:
            continue

        card = target_list.add_card(
            name=game['name'],
            desc=json.dumps({
                'appid': game['appid'],
                'name': game['name'],
                'img_logo_url': game['img_logo_url']}),
            labels=labels,
        )
        card.attach(url=game['img_logo_url'])

def main():
    settings = {}
    settings, use_trello = load_settings({
        'SteamWebAPI':{'API_KEY':'','STEAM_ID':'',},
        'Trello':{'API_KEY':'','API_SECRET':'','TOKEN':'','BOARD_ID':'','LIST_ID':'',},
    },)
    games = get_games(settings)
    if use_trello:
        output_to_trello(settings, games)
    else:
        print('')
        print('============ 所持ゲーム一覧 ============')
        for game in games:
            print('{} : {}'.format(game['name'], game['img_logo_url']))

if __name__ == '__main__':
    main()

# ~~ Steam Web API response sample
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
