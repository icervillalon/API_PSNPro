import requests
import re
import json
import bs4

PROFILE_PAGE = 'https://psnprofiles.com/{}?ajax=1&completion=all&order=last-played&pf=all&page={}'
FULL_PROFILE_PAGE = 'https://psnprofiles.com/{}'
TROPHY_PAGE = 'https://psnprofiles.com/trophies/{}/{}'

class PsnProfile():
    def __init__(self, user):
        self.user = user
        self.profile, self.trophy_data = self._get_profile()
        self.game_list = self._get_game_list()

    def _get_profile(self):
        '''
        Get the profile pages for a user
        :return [list]: List of HTML pages dict
        :return [dict]: Trophy data
        '''
        try:
            parsed_page = []
            page_number = 0
            parsed_html = json.loads(requests.get(PROFILE_PAGE.format(self.user, page_number)).text)['html']
            trophy_data = self._get_user_trophy_data()
            parsed_page.append(parsed_html.strip())
            while re.search('Show [0-9]+ more games', parsed_page[-1]) is not None:
                page_number += 1
                parsed_html = json.loads(requests.get(PROFILE_PAGE.format(self.user, page_number)).text)['html']
                parsed_page.append(parsed_html)
        except json.JSONDecodeError:
            print(f"Profile not found for user '{self.user}'")
            return [], {}
        return parsed_page, trophy_data

    @staticmethod
    def _validate_game(game):
        return False if game == '\n' or re.search('more games', game) is not None else True

    def _get_game_list(self):
        game_list = []
        for page in self.profile:
            parsed_html = bs4.BeautifulSoup(page, 'html.parser')
            data = parsed_html.find_all('a', 'title')
            for item in data:
                if self._validate_game(item.string):
                    game_list.append(item.string)
        return game_list

    def _get_user_trophy_data(self):
        """
        Captures the 'profile-bar' item in the profile page, which contains the trophy level and the number of trophies.
        :return: dict(str,str) with trophy data. Keys: ['level', 'platinum', 'gold', 'silver', 'bronze']
        """
        html = requests.get(FULL_PROFILE_PAGE.format(self.user)).text
        parsed_html = bs4.BeautifulSoup(html, 'html.parser').find('ul', attrs={'class': 'profile-bar'})
        trophy_data = {data['class'][0].replace('icon-sprite', 'level'): data.getText().strip().replace(',','') for data in parsed_html.find_all('li')}
        return trophy_data

    #TODO
    def get_game_details(self, game_id):
        print(requests.get(PROFILE_PAGE.format(game_id, self.user)).text)

    #TODO
    def platinum_trophy(self, game_id):
        'if the image /lib/img/icons/platinum-icon.png is present on game page, the player has the trophy'
        pass