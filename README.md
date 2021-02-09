# stack-game-list

This is a script that outputs a list of games it owns to digest Steam's stacking games.

# DEMO

Not yet

# Features

You can output the acquired game list to a text file and import it to Trello.

# Requirement

* Python 3.9.1

# Installation

```bash
pip install -r requirements.txt
```

# Usage

```bash
git clone https://github.com/kimatamaki/stack-game-list
cd stack-game-list
```
Edit settings.py and enter the API key obtained from the Steam Web API in the following variables.
```python:settings.py
API_KEY = "Your Steam Web API Key"
STEAMID = "Youre Steam Profile ID"
```
```bash
python stackgamelist.py
```

# Note

# Author

作成情報を列挙する

* [@menow_white](https://twitter.com/menow_white)

# License
Not yet