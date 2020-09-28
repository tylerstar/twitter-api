from unittest import mock
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from tweets.tests.utils import (
    mocked_twitter_api,
    mocked_twitter_api_without_results
)


def tweets_by_hashtag_url(hashtag):
    return f'/hashtags/{hashtag}'


def tweets_by_user_url(screen_name):
    return f'/users/{screen_name}'


class PublicTweetsApiTest(TestCase):
    """Test the publically available tweets API"""

    def setUp(self):
        self.client = APIClient()

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_retrieve_tweets_by_hashtag(self, mock_get):
        """Test retrieving a list of tweets by hashtag"""
        hashtag = 'python'
        url = tweets_by_hashtag_url(hashtag)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # default return 30 tweets
        self.assertEqual(len(res.data), 30)

        tweet = res.data[0]

        # check existence and type of every field of the response
        self.assertIn('account', tweet)
        self.assertIn('fullname', tweet['account'])
        self.assertTrue(isinstance(tweet['account']['fullname'], str))
        self.assertIn('href', tweet['account'])
        self.assertTrue(isinstance(tweet['account']['href'], str))
        self.assertIn('id', tweet['account'])
        self.assertTrue(isinstance(tweet['account']['id'], str))
        self.assertIn('hashtags', tweet)
        self.assertTrue(isinstance(tweet['hashtags'], list))
        self.assertIn('likes', tweet)
        self.assertTrue(isinstance(tweet['likes'], int))
        self.assertIn('replies', tweet)
        self.assertTrue(isinstance(tweet['replies'], int))
        self.assertIn('retweets', tweet)
        self.assertTrue(isinstance(tweet['retweets'], int))
        self.assertIn('text', tweet)
        self.assertTrue(isinstance(tweet['text'], str))

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_retrieve_given_number_of_tweets_by_hashtag(self, mock_get):
        hashtag = 'python'
        url = tweets_by_hashtag_url(hashtag)
        payload = {'limit': 12}
        res = self.client.get(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 12)

    def test_retrieve_tweets_with_empty_hashtag(self):
        """Test retrieving tweets with empty hashtag"""
        hashtag = ''
        url = tweets_by_hashtag_url(hashtag)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    @mock.patch(
        'requests.get',
        side_effect=mocked_twitter_api_without_results
    )
    def test_retrieve_tweets_with_not_found_hashtag(self, mock_get):
        hashtag = 'hashtags'
        url = tweets_by_hashtag_url(hashtag)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    def test_retrieve_tweets_by_hashtags_with_invalid_limit(self):
        hashtag = 'python'
        url = tweets_by_hashtag_url(hashtag)

        payload = {'limit': 0}
        res = self.client.get(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {'limit': -1}
        res = self.client.get(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {'limit': 101}
        res = self.client.get(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_retrieve_tweets_by_user(self, mock_get):
        """Test retrieving a list of tweets by user"""
        screen_name = 'twitter'
        url = tweets_by_user_url(screen_name)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # return 30 tweets by default
        self.assertEqual(len(res.data), 30)

        tweet = res.data[0]

        # check existence and type of every field of the response
        self.assertIn('account', tweet)
        self.assertIn('fullname', tweet['account'])
        self.assertTrue(isinstance(tweet['account']['fullname'], str))
        self.assertIn('href', tweet['account'])
        self.assertTrue(isinstance(tweet['account']['href'], str))
        self.assertIn('id', tweet['account'])
        self.assertTrue(isinstance(tweet['account']['id'], str))
        self.assertIn('hashtags', tweet)
        self.assertTrue(isinstance(tweet['hashtags'], list))
        self.assertIn('likes', tweet)
        self.assertTrue(isinstance(tweet['likes'], int))
        self.assertIn('replies', tweet)
        self.assertTrue(isinstance(tweet['replies'], int))
        self.assertIn('retweets', tweet)
        self.assertTrue(isinstance(tweet['retweets'], int))
        self.assertIn('text', tweet)
        self.assertTrue(isinstance(tweet['text'], str))

    @mock.patch('requests.get', side_effect=mocked_twitter_api)
    def test_retrieve_given_number_of_tweets_by_user(self, mock_get):
        screen_name = 'twitter'
        url = tweets_by_user_url(screen_name)
        payload = {'limit': 12}
        res = self.client.get(url, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 12)

    @mock.patch(
        'requests.get',
        side_effect=mocked_twitter_api_without_results
    )
    def test_retrieve_tweets_with_user_not_exists(self, mock_get):
        """Test retrieving a twitter user doesn't exist"""
        screen_name = 'screen_name'
        url = tweets_by_user_url(screen_name)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    def test_retrieve_tweets_by_user_with_invalid_limit(self):
        screen_name = 'twitter'
        url = tweets_by_user_url(screen_name)

        payload = {'limit': 0}
        res = self.client.get(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {'limit': -1}
        res = self.client.get(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        payload = {'limit': 101}
        res = self.client.get(url, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_existed_methods(self):
        """Test post/delete/patch/put method on APIs"""
        hashtag = 'python'
        url = tweets_by_hashtag_url(hashtag)

        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.patch(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.put(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        screen_name = 'screen_name'
        url = tweets_by_user_url(screen_name)

        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.patch(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        res = self.client.put(url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
