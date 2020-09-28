import requests
import datetime

from twitterapi.settings import TWITTER_TOKEN


class TwitterServices:
    """List of services to fetch data via Twitter APIs
       All services will have two common methods:

       1. fetch_data() which fetch data through Twitter APIs
       2. get_tweets() format the responses of Twitter's APIs
          and return a list of tweets

       NOTICE: You need to configure the Twitter API Bearer Token
               before calling these services
    """
    HASHTAG = 0
    USER = 1
    HEADERS = {'Authorization': f'Bearer {TWITTER_TOKEN}'}

    def __init__(self, search_by, **kwargs):
        """Initialize the service instance base on param search_by"""
        if search_by == self.HASHTAG:
            self._instance = TwitterSearchAPIService(self.HEADERS, **kwargs)
        elif search_by == self.USER:
            self._instance = TwitterUserAPIService(self.HEADERS, **kwargs)

    @classmethod
    def get_tweets(cls, search_by, **kwargs):
        """Universal interface to call the initialized service"""
        service = cls(search_by, **kwargs)
        service._instance.fetch_data()
        return service._instance.get_tweets()


class TwitterSearchAPIService:
    RECENT_SEARCH_API = 'https://api.twitter.com/2/tweets/search/recent'

    def __init__(self, headers, hashtag, count):
        """Initialize the Search API service

        :param hashtag: tweets with given hashtag
        :param count: number of tweets that return
        """
        self._headers = headers
        self.hashtag = hashtag
        self.count = count
        self._tweets = []

    def fetch_data(self):
        # when count < 10, twitter api would throw out an error
        # ensure minimum value of count is equal or larger than 10
        max_results = 10 if self.count < 10 else self.count

        payload = {
            'query': f'#{self.hashtag}',
            'max_results': max_results,
            'tweet.fields': 'entities,created_at,public_metrics',
            'user.fields': 'id,url,name,username',
            'expansions': 'author_id',
        }

        res = requests.get(
            self.RECENT_SEARCH_API,
            headers=self._headers,
            params=payload
        )

        # failed to request tweets via twitter api
        if not res.ok:
            raise Exception(res.json())

        # no tweets found
        if res.json()['meta']['result_count'] == 0:
            return

        tweets = res.json()['data']

        users = {}
        for user in res.json()['includes']['users']:
            users[user['id']] = user

        for tweet in tweets:
            tweet['user'] = users[tweet['author_id']]

        self._tweets = tweets

    @classmethod
    def _get_account(cls, tweet):
        """Get account from field user"""
        return {
            'fullname': tweet['user']['name'],
            'href': f"/{tweet['user']['username']}",
            'id': tweet['user']['id']
        }

    @classmethod
    def _get_date(cls, tweet):
        """Get date from field tweet"""
        created_at = datetime.datetime.strptime(
            tweet['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        return created_at.strftime('%-H:%M %p - %-d %b %Y')

    @classmethod
    def _get_hashtags(cls, tweet):
        """Get hashtags from field tweet"""
        return [f"#{x['tag']}" for x in tweet['entities'].get('hashtags', [])]

    @classmethod
    def _get_likes_count(cls, tweet):
        """Get likes count from field tweet"""
        return tweet['public_metrics']['like_count']

    @classmethod
    def _get_replies_count(cls, tweet):
        """Get replies count from field tweet"""
        return tweet['public_metrics']['reply_count']

    @classmethod
    def _get_retweets_count(cls, tweet):
        """Get retweet count from field tweet"""
        return tweet['public_metrics']['retweet_count']

    @classmethod
    def _get_text(cls, tweet):
        """Get text from field tweet"""
        return tweet['text']

    def get_tweets(self):
        res = []
        for tweet in self._tweets:
            # get user of this tweet
            item = {}
            item['account'] = self._get_account(tweet)
            item['date'] = self._get_date(tweet)
            item['hashtags'] = self._get_hashtags(tweet)
            item['likes'] = self._get_likes_count(tweet)
            item['replies'] = self._get_replies_count(tweet)
            item['retweets'] = self._get_retweets_count(tweet)
            item['text'] = self._get_text(tweet)

            res.append(item)

        # ensure to return the correct number of items
        return res[:self.count]


class TwitterUserAPIService:
    USER_TIMELINE_API = \
        'https://api.twitter.com/1.1/statuses/user_timeline.json'
    LOOK_UP_API = 'https://api.twitter.com/2/tweets'

    def __init__(self, headers, screen_name, count):
        """Initialize user service

        :param screen_name: tweeter's screen_name
        :param count: number of tweets that return
        """
        self._headers = headers
        self.screen_name = screen_name
        self.count = count
        self._tweets = []

    def fetch_data(self):
        # when count < 10, twitter api will throw an error
        # ensure minimum value of count is equal or larger than 10
        max_results = 10 if self.count < 10 else self.count

        timeline_payload = {
            'screen_name': self.screen_name,
            'count': max_results
        }

        timeline_res = requests.get(
            self.USER_TIMELINE_API,
            headers=self._headers,
            params=timeline_payload
        )

        # twitter user timeline api v1.1 return 404 status code while
        # there's no result found
        if timeline_res.status_code == 404:
            return

        if not timeline_res.ok:
            raise Exception(f'Error: {timeline_res.json()}')

        # user_timeline api (1.1) has not provided the likes count in response
        # and so  it's necessary to call lookup api (2.0)
        # to get the replies count for each tweets
        tweets = timeline_res.json()
        tweet_ids = [str(x['id']) for x in tweets]

        lookup_payload = {
            'ids': ','.join(tweet_ids),
            'tweet.fields': 'public_metrics',
        }

        lookup_res = requests.get(
            self.LOOK_UP_API,
            headers=self._headers,
            params=lookup_payload
        )

        if not timeline_res.ok:
            raise Exception(f'Error: {timeline_res.json()}')

        lookup_data = lookup_res.json()['data']
        replies_count = {}
        for item in lookup_data:
            replies_count[item['id']] = item['public_metrics']['reply_count']

        for tweet in tweets:
            tweet['replies_count'] = replies_count[str(tweet['id'])]

        self._tweets = tweets

    def _get_account(self, tweet):
        # get the user of the tweet
        user = tweet['user']

        return{
            'fullname': user['name'],
            'href': f"/{user['screen_name']}",
            'id': str(user['id'])
        }

    def _get_date(self, tweet):
        # tweet's created time
        # response's format: "Wed Sep 23 17:08:34 +0000 2020"
        created_at = datetime.datetime.strptime(
            tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        return created_at.strftime('%-H:%M %p - %-d %b %Y')

    def _get_hashtags(self, tweet):
        return [f"#{x['text']}" for x in tweet['entities'].get('hashtags', [])]

    def _get_likes_count(self, tweet):
        return tweet['favorite_count']

    def _get_replies_count(self, tweet):
        return tweet['replies_count']

    def _get_retweets_count(self, tweet):
        return tweet['retweeted']

    def _get_text(self, tweet):
        return tweet['text']

    def get_tweets(self):
        res = []
        for tweet in self._tweets:
            # get user of this tweet
            item = {}
            item['account'] = self._get_account(tweet)
            item['date'] = self._get_date(tweet)
            item['hashtags'] = self._get_hashtags(tweet)
            item['likes'] = self._get_likes_count(tweet)
            item['replies'] = self._get_replies_count(tweet)
            item['retweets'] = self._get_retweets_count(tweet)
            item['text'] = self._get_text(tweet)

            res.append(item)

        # ensure to return the correct number of items
        return res[:self.count]
