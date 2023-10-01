from rest_framework import serializers, validators
from .models import CostDetail
from django.contrib.auth.models import User


class CostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CostDetail
        fields = (
            'uid','ResName', 'date', 'which_meal', 'rid', 'price', 'rating', 'my_text')

    def create(self, validated_data):
        uid = validated_data.get('uid')
        ResName = validated_data.get('ResName')
        date = validated_data.get('date')
        which_meal = validated_data.get('which_meal')
        rid = validated_data.get('rid')
        price = validated_data.get('price')
        rating = validated_data.get('rating')
        my_text = validated_data.get('my_text')

        cost = CostDetail.objects.create(
            uid=uid,
            ResName=ResName,
            date=date,
            which_meal=which_meal,
            rid=rid,
            price=price,
            rating=rating,
            my_text=my_text,
        )
        return cost
