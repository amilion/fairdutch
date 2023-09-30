from rest_framework import serializers
from django.contrib.auth import get_user_model

user = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, style={"input_type": "password"})


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, style={"input_type": "password"})

    class Meta:
        model = user
        fields = ["username", "password", "email", "first_name", "last_name"]

    def create(self, validated_data):
        return user.objects.create_user(**validated_data)
