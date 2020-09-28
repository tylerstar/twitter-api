from rest_framework import serializers


class TweetSerializer(serializers.Serializer):
    """Serializers a limit field for Tweet api"""
    limit = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=100
    )
