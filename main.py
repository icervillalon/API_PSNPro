import requests
import re
import json
import bs4

PROFILE_PAGE = 'https://psnprofiles.com/{}?ajax=1&completion=all&order=last-played&pf=all&page={}'

class PsnProfile():
    def __init__(self, user):
        self.user = user
        self.profile = self._get_profile()
        self.game_list = self._get_game_list()

    def _get_profile(self):
        '''
        Get the profile pages for a user
        :return [list]: List of HTML pages dict
        '''
        try:
            parsed_page = []
            page_number = 0
            parsed_html = json.loads(requests.get(PROFILE_PAGE.format(self.user, page_number)).text)['html']
            parsed_page.append(parsed_html.strip())
            while re.search('Show [0-9]+ more games', parsed_page[-1]) is not None:

                page_number += 1
                parsed_html = json.loads(requests.get(PROFILE_PAGE.format(self.user, page_number)).text)['html']
                parsed_page.append(parsed_html)
        except json.JSONDecodeError:
            print(f"Profile not found for user '{self.user}'")
            return []
        return parsed_page

    def _get_game_list(self):
        game_list = []
        for page in self.profile:
            parsed_html = bs4.BeautifulSoup(page, 'html.parser')
            data = parsed_html.find_all('a', 'title')
            for item in data:
                if self._validate_game(item.string):
                    game_list.append(item.string)
        return game_list

    def _validate_game(self, game):
        return False if game == '\n' or re.search('more games', game) is not None else True

test_profile = PsnProfile('user_to_test')

print(test_profile.game_list)
[print(name) for name in test_profile.game_list]