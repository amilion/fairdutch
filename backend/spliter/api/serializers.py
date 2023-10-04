from django.db.models import Sum
from django.contrib.auth import get_user_model

from rest_framework import serializers

from spliter.models import Split
from dutches.models import Dutch
from accounts.api.serializer import UserSerializer

User = get_user_model()


class SplitSerializer(serializers.ModelSerializer):
    debtor = UserSerializer()
    creditor = UserSerializer()

    class Meta:
        model = Split
        fields = ["debtor", "creditor", "amount"]

    def create(self):
        Split.objects.all().delete()
        total = Dutch.objects.all().aggregate(total=Sum("price"))["total"]

        keys = list(Dutch.objects.all().values_list("user_id").distinct())
        values = [
            Dutch.objects.filter(user_id=x).aggregate(
                total_user_spent=Sum("price") - total / len(keys)
            )["total_user_spent"]
            for x in keys
        ]
        while not values[0]:
            keys.pop(0)
            values.pop(0)
        query_to_bulk_create = []
        index = 1
        for value in values[1:]:
            if not value:
                values.pop(index)
                keys.pop(index)
                continue
            if values[index - 1] < 0:
                new_split = Split(
                    debtor=User.objects.get(id=keys[index - 1][0]),
                    creditor=User.objects.get(id=keys[index][0]),
                    amount=-1 * values[index - 1],
                )
            else:
                new_split = Split(
                    debtor=User.objects.get(id=keys[index][0]),
                    creditor=User.objects.get(id=keys[index - 1][0]),
                    amount=values[index - 1],
                )
            values[index] = values[index - 1] + value
            values[index - 1] = 0
            query_to_bulk_create.append(new_split)
            index += 1
        return Split.objects.bulk_create(query_to_bulk_create)

    def update(self, instance, validated_data):
        instance.deptor = validated_data.get("deptor", instance.deptor)
        instance.creditor = validated_data.get("creditor", instance.creditor)
        instance.amount = validated_data.get("amount", instance.amount)
        instance.save()
        return instance
