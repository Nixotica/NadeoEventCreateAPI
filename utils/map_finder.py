import requests as requests


def get_random_map_uid() -> str:
    url = 'https://trackmania.exchange/mapsearch2/search?api=on&random=1'
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Get-random-map / nixotica@gmail.com'
    }
    map_info = requests.post(url, headers=headers).json()
    return map_info['results'][0]['TrackUID']
