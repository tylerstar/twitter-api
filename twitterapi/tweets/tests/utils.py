import os
import json
import pathlib

from tweets.services import (
    TwitterSearchAPIService,
    TwitterUserAPIService
)


class MockResponse:
    """Mock return value of requests.get"""
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    @property
    def ok(self):
        return True


def mocked_twitter_api(*args, **kwargs):
    """Mock function to simulate return value from Twitter APIs"""
    current_dir = pathlib.Path().absolute()
    mocked_data_dir = os.path.join(
        current_dir,
        'tweets',
        'tests',
        'mocked_data',
    )

    # mock results returned from twitter search api
    if args[0] == TwitterSearchAPIService.RECENT_SEARCH_API:
        filepath = os.path.join(
            mocked_data_dir,
            'twitter_search_api_mocked_data.json'
        )
        with open(filepath, 'r') as f:
            return MockResponse(json.loads(f.read()), 200)
    # mock results returned from twitter user timeline api
    elif args[0] == TwitterUserAPIService.USER_TIMELINE_API:
        filepath = os.path.join(
            mocked_data_dir,
            'twitter_user_timeline_api_mocked_data.json'
        )
        with open(filepath, 'r') as f:
            return MockResponse(json.loads(f.read()), 200)
    # mock results returned from twitter look up api
    elif args[0] == TwitterUserAPIService.LOOK_UP_API:
        filepath = os.path.join(
            mocked_data_dir,
            'twitter_tweets_api_mocked_data.json'
        )
        with open(filepath, 'r') as f:
            return MockResponse(json.loads(f.read()), 200)

    return MockResponse(None, 404)


def mocked_twitter_api_without_results(*args, **kwargs):
    """simulate twitter search api return """
    # twitter v2 search api returns results below while there's no result found
    if args[0] == TwitterSearchAPIService.RECENT_SEARCH_API:
        return_value = {
            "meta": {
                "result_count": 0
            }
        }
        return MockResponse(return_value, 200)
    # twitter v1.1 user timeline api returns results below while user not found
    elif args[0] == TwitterUserAPIService.USER_TIMELINE_API:
        return_value = {
            "errors": [
                {
                    "code": 34,
                    "message": "Sorry, that page does not exist."
                }
            ]
        }
        return MockResponse(return_value, 404)

    return MockResponse(None, 404)