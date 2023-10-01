from accounts.api.serializer import UserSerializer
from rest_framework import serializers
from dutches.models import Dutch


class DutchSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Dutch
        fields = ["user", "stuff_name", "price"]


class DutchCUSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dutch
        fields = ["stuff_name", "price"]

    def create(self, user, validated_data):
        return Dutch.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        instance.stuff_name = validated_data.get("stuff_name", instance.stuff_name)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        return instance
