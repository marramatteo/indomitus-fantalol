from pprint import pprint
from typing import List

import requests

api_key = 'RGAPI-24a48f9d-73aa-43d8-aeab-bd39e5654a82'


class GetUserInfo:
    def __init__(self):
        self.url_by_riot_id = 'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'
        self.url_by_puuid = 'https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/'
        self.url_by_puuid_enc = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/'
        self.url_matches_id = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/'
        self.url_single_match = 'https://europe.api.riotgames.com/lol/match/v5/matches/'

    def _get_user_puuid(self, username: str, user_tag: str) -> str:
        '''
        This function returns the puuid for an account having the account name and his tag
        '''
        req = requests.get(f'{self.url_by_riot_id}{username}/{user_tag}?api_key={api_key}')
        return req.json()['puuid']

    def get_user_info_by_riot_id(self, username: str, user_tag: str):
        '''
        This function returns all infos for an account in a json format
        '''
        puuid = self._get_user_puuid(username, user_tag)
        req = requests.get(f'{self.url_by_puuid_enc}{puuid}?api_key={api_key}')
        return req.json()

    def get_matches_id_for_user(self, username: str, user_tag: str, num: int = 1):
        '''
        This function returns all of the match history based on a puuid
        '''
        puuid = self._get_user_puuid(username, user_tag)
        req = requests.get(f'{self.url_matches_id}{puuid}/ids?count={num}&api_key={api_key}')
        return req.json()


    def analyze_match(self, match_id: str):
        '''
        This function analyzes one match in particular and extracts its most meaningful metadata
        '''
        req = requests.get(f'{self.url_single_match}{match_id}?api_key={api_key}').json()
        players = self.get_players_name_by_riot_id(puuids=req['metadata']['participants'])
        dict_to_return = {'Partecipanti': players}
        return req

    def get_players_name_by_riot_id(self, puuids: List[str]) -> List[str]:
        '''
        This function returns the name and tag of all players who have a puuid in list
        '''
        players_list = []
        for puuid in puuids:
            user_info_json = requests.get(f'{self.url_by_puuid}{puuid}/?api_key={api_key}').json()
            user_str = user_info_json['gameName'] + ' #' + user_info_json['tagLine']
            players_list.append(user_str)
        return players_list

    def get_match_by_id(self, match_id: str):
        req = requests.get(f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}')
        return req.json()


if __name__ == '__main__':
    obj = GetUserInfo()
    match_id = obj.get_matches_id_for_user('abracamarra', 'EUW')[0]
    match_results = obj.analyze_match(match_id=match_id)
    # match_results = obj.get_match_by_id(match_id='7275336519')
    pprint(match_results)
