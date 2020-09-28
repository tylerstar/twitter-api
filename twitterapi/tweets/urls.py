from django.urls import path

from tweets import views

app_name = 'tweets'

urlpatterns = [
    path('hashtags/<slug:hashtag>', views.TweetsByHashtagApiView.as_view()),
    path('users/<slug:screen_name>', views.TweetsByUserApiView.as_view())
]
