from rest_framework import serializers

from spliter.models import Split
from accounts.api.serializer import UserSerializer


class SplitSerializer(serializers.ModelSerializer):
    deptor = UserSerializer()
    creditor = UserSerializer()

    class Meta:
        model = Split
        fields = ["debtor", "creditor", "amount"]

    def create(self, validated_data):
        return Split.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.deptor = validated_data.get("deptor", instance.deptor)
        instance.creditor = validated_data.get("creditor", instance.creditor)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.save()
        return instance
