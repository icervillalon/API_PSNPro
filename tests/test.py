from api_methods import *
import unittest


class TestGetProfile(unittest.TestCase):
    test_profile = PsnProfile('add_a_functional_profile')

    def test_profile_exists(self):
        """Checks if profile exists"""
        if self.test_profile.profile:
            assert True
        else:
            assert False

    def test_not_existing_profile(self):
        """Checks if returns an empty list if the profile doesn't exist"""
        mocked_user = PsnProfile('MockedUser').profile
        if isinstance(mocked_user, list) and len(mocked_user) == 0:
            assert True
        else:
            assert False, f"Expected an empty list, received {type(mocked_user)} with value {str(mocked_user)}"

    def test_get_games(self):
        """Checks if the profile has games"""
        if self.test_profile.game_list:
            assert True
        else:
            assert False

    def test_trophy_data(self):
        """Checks if the trophy data is a dict with the specified keys"""
        key_data = ['level', 'platinum', 'gold', 'silver', 'bronze']
        for key in key_data:
            if key not in self.test_profile.trophy_data.keys():
                assert False, f"{key} not found in trophy data dict, received {self.test_profile.trophy_data}"
        assert True

if __name__ == '__main__':
    unittest.main()


