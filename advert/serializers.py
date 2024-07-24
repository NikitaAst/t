from rest_framework import serializers


class AdvertSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    title = serializers.CharField()
    description = serializers.CharField()
    views = serializers.IntegerField()
    category_name = serializers.CharField()
    city_name = serializers.CharField()
