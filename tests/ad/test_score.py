from unittest import TestCase
from tenable.ad.score import  ScoreApi as api
from tenable.ad import APIKeyApi as apikey



class TestScoreApi(TestCase):
    def test_api_profiles_profile_id_scores_get(self):
        """
            Get the directories score by profile
        """
        x_api_key = apikey.get_api_key(self)
        thread = api.api_profiles_profile_id_scores_get(api,x_api_key,1)
        if (len(thread) != 0):
            if (thread[0] != 'error'):
                if (thread.status == 200):
                    if (thread.data == []):
                        print ('profile scores yet to be added in the system')
                    else:
                        print('profile scores are not available')
        else:
            print('score not available error')
