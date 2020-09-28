import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from tweets.services import TwitterServices
from tweets.serializers import TweetSerializer


class TweetsByHashtagApiView(APIView):

    serializer_class = TweetSerializer

    def get(self, request, hashtag):
        '''Retrieving a list of tweets by hashtag'''
        serializer = self.serializer_class(data=request.query_params)

        # validate the query params
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # fetch the data via twitter api
        try:
            count = serializer.validated_data.get('limit', 30)
            tweets = TwitterServices.get_tweets(
                search_by=TwitterServices.HASHTAG,
                hashtag=hashtag,
                count=count
            )
            return Response(tweets)
        except Exception as e:
            # logging unexpected errors for debugging
            logging.exception(
                f'failed to run TwitterServices.get_tweets_by_hashtag: {e}'
            )
            # hide the actual error message and return
            # internal server error ensure the error response's
            # format as same as the django's default format
            return Response(
                {'internal server error': ['unknown error occurred.']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class TweetsByUserApiView(APIView):

    serializer_class = TweetSerializer

    def get(self, request, screen_name):
        '''Retrieving a list of tweets by user'''
        serializer = self.serializer_class(data=request.query_params)

        # validate the query params
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # fetch the data via twitter api
        try:
            count = serializer.validated_data.get('limit', 30)
            tweets = TwitterServices.get_tweets(
                search_by=TwitterServices.USER,
                screen_name=screen_name,
                count=count
            )
            return Response(tweets)
        except Exception as e:
            # logging unexpected errors for debugging
            logging.exception(
                f'failed to run TwitterServices.get_tweets_by_user: {e}'
            )
            # hide the actual error message and return
            # internal server error ensure the error response's
            # format as same as the django's default format
            return Response(
                {'internal server error': ['unknown error occurred.']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
