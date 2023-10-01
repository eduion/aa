from django.shortcuts import render
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Restaurant
from . import recommender
class recommend(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        updated_request = request.data
        user = request.user
        if user.is_authenticated:
            user_id = user.id
            # uID, TimeFilter, MealFilter, LabelFilter, DistanceSort, RatingSort
            rID_list = recommender.main(user_id, updated_request['TimeFilter'],  updated_request['MealFilter'], updated_request['LabelFilter'],  updated_request['DistanceSort'],  updated_request['RatingSort'])
            result_dict = {}
            keys_to_delete = ['rid', 'sun', 'mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'all_label', 'meal_or_not']
            try:
                for i in rID_list:
                    result_dict[i] = Restaurant.objects.filter(rid=i).values()
                    result_dict[i] = result_dict[i][0]
                    result_dict[i] = {key: result_dict[i][key] for key in result_dict[i] if key not in keys_to_delete}
                    if result_dict[i]:
                        print(result_dict[i])
                    else:
                        print(f"Restaurant with rid {i} not found in the database.")
            except Exception as e:
                print(f"An error occurred while querying the database: {e}")
            return Response({
                # 前端名稱
                # rID 店名 時間 評分 距離 電話 地址
                'success': result_dict
            })
        return Response({
            'success': False
        })