from django.shortcuts import render
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UidRestaurant

class FRList(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        updated_request = request.data
        user = request.user
        if user.is_authenticated:
            user_id = user.id
            result = UidRestaurant.objects.filter(uid=user_id).values()
            result = result[0]
            like = [key for key, value in result.items() if value == 1]
            unlike = [key for key, value in result.items() if value == -1]
            # like = like[1:]
            # unlike = unlike[1:]
            like = [int(item.split('_')[1]) for item in like]
            unlike = [int(item.split('_')[1]) for item in unlike]
            return Response({
                # 前端名稱
                'success': [like, unlike]
            })
        return Response({
            'success': False
        })