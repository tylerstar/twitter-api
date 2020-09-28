import datetime
from unittest import mock
from django.test import TestCase

from twitterapi.settings import TWITTER_TOKEN
from tweets.services import (
    TwitterServices,
    TwitterUserAPIService,
    TwitterSearchAPIService
)
from tweets.tests.utils import mocked_twitter_api


class TestTwitterService(TestCase):

    def test_initialize_the_correct_api_service(self):
        """Test initialize the api service based on param search_by"""
        service = TwitterServices(
            search_by=TwitterServices.HASHTAG,
            hashtag='hashtag',
            count=10
        )
        self.assertTrue(isinstance(service._instance, TwitterSearchAPIService))

        service = TwitterServices(
            search_by=TwitterServices.USER,
            screen_name='screen_name',
            count=10
        )
        self.assertTrue(isinstance(service._instance, TwitterUserAPIService))


class TestTwitterSearchAPIService(TestCase):

    def setUp(self):
        """Setting up the twitter search api service"""
        self.headers = {'Authorization': f'Bearer {TWITTER_TOKEN}'}
        self.service = TwitterSearchAPIService(
            headers=self.headers,
            hashtag='hashtag',
            count=10
        )

    def test_initialize_the_service(self):
        self.assertEqual(self.service._headers, self.headers)
        self.assertEqual(self.service.hashtag, 'hashtag')
        self.assertEqual(self.service.count, 10)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_fetch_data(self, mock_get):
        """Test fetch data from Twitter API and process it correctly"""
        self.service.fetch_data()
        self.assertTrue(len(self.service._tweets) > 0)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_account(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        account = self.service._get_account(tweet)

        self.assertEqual(account, {
            'fullname': tweet['user']['name'],
            'href': f"/{tweet['user']['username']}",
            'id': tweet['user']['id']
        })

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_date(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        result = self.service._get_date(tweet)

        created_at = datetime.datetime.strptime(
            tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        date = created_at.strftime('%-H:%M %p - %-d %b %Y')

        self.assertEqual(date, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_hashtags(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        result = self.service._get_hashtags(tweet)

        hashtags = []
        for item in tweet['entities'].get('hashtags', []):
            hashtags.append(f"#{item['tag']}")

        self.assertEqual(hashtags, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_likes_count(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        result = self.service._get_likes_count(tweet)

        likes_count = tweet['public_metrics']['like_count']
        self.assertEqual(likes_count, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_replies_count(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        result = self.service._get_replies_count(tweet)

        replies_count = tweet['public_metrics']['reply_count']
        self.assertEqual(replies_count, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_retweets_count(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        result = self.service._get_retweets_count(tweet)

        retweets_count = tweet['public_metrics']['retweet_count']
        self.assertEqual(retweets_count, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_text(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        text = self.service._get_text(tweet)

        result = tweet['text']
        self.assertEqual(text, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_tweets(self, mock_get):
        service = TwitterSearchAPIService(
            headers=self.headers,
            hashtag='hashtag',
            count=5
        )
        service.fetch_data()
        res = service.get_tweets()
        self.assertEqual(len(res), 5)


class TestTwitterUserAPIService(TestCase):

    def setUp(self):
        """Setting up the twitter search api service"""
        self.headers = {'Authorization': f'Bearer {TWITTER_TOKEN}'}
        self.service = TwitterUserAPIService(
            headers=self.headers,
            screen_name='twitter',
            count=10
        )

    def test_initialize_the_service(self):
        self.assertEqual(self.service._headers, self.headers)
        self.assertEqual(self.service.screen_name, 'twitter')
        self.assertEqual(self.service.count, 10)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_fetch_data(self, mock_get):
        self.service.fetch_data()
        self.assertTrue(len(self.service._tweets) > 0)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_account(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        account = self.service._get_account(tweet)
        user = tweet['user']

        self.assertEqual(account, {
            'fullname': user['name'],
            'href': f"/{user['screen_name']}",
            'id': str(user['id'])
        })

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_date(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        result = self.service._get_date(tweet)

        created_at = datetime.datetime.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        date = created_at.strftime('%-H:%M %p - %-d %b %Y')

        self.assertEqual(date, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_hashtags(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        hashtags = self.service._get_hashtags(tweet)

        result = []
        for item in tweet['entities'].get('hashtags', []):
            result.append(f"#{item['text']}")

        self.assertEqual(hashtags, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_likes_count(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        likes_count = self.service._get_likes_count(tweet)

        result = tweet['favorite_count']
        self.assertEqual(likes_count, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_replies_count(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        replies_count = self.service._get_replies_count(tweet)

        result = tweet['replies_count']
        self.assertEqual(replies_count, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_retweets_count(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        retweets_count = self.service._get_retweets_count(tweet)

        result = tweet['retweeted']
        self.assertEqual(retweets_count, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_text(self, mock_get):
        self.service.fetch_data()
        tweet = self.service._tweets[0]
        text = self.service._get_text(tweet)

        result = tweet['text']
        self.assertEqual(text, result)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_get_tweets(self, mock_get):
        service = TwitterUserAPIService(
            headers=self.headers,
            screen_name='twitter',
            count=5
        )
        service.fetch_data()
        res = service.get_tweets()
        self.assertEqual(len(res), 5)
