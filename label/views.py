from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import numpy as np
import random
@api_view(['GET'])
def get_label(request):
    df = pd.read_excel('./label/excel/restaurant.xlsx', sheet_name="label_static")
    df = df[df["數量"] >= 5]
    df = df.sample(n=20, replace=False)
    name = df["類別"]
    return Response({
        '類別':name
    })
    # user = request.user
    # if user.is_authenticated:
    #     return Response({
    #         'user_info': {
    #             'id': user.id,
    #             'username': user.username,
    #             'email': user.email
    #         }
    #     })
    # else:
    #     return Response({
    #         'error':'not authenticated'
    #     },status = 400)