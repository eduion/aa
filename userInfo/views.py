from django.shortcuts import render
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer,UserSerializer,UserLikeSerializer
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from userLike import label_convert
from .models import UserInfo
from baby.models import UserBaby

@api_view(['POST'])
def get_user_data(request):
    print(request.data)
    # print(request.data)
    user = request.user
    if user.is_authenticated:
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    else:
        return Response({
            'error':'not authenticated'
        },status = 400)
# @api_view(['POST'])
# def login_api(request):
#     serializer = AuthTokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     user = serializer.validated_data['user']
#     _, token = AuthToken.objects.create(user)
#
#     return Response({
#         'user_info': {
#             'username': user.username,
#         },
#         'token': token
#     })
class login_api(generics.GenericAPIView):
    serializer_class = AuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        _, token = AuthToken.objects.create(user)
        print(token)
        return Response({
            'success':True,
            'token': token
        })
# Create your views here.
class register_api(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validate(attrs=request.data)  # 判斷密碼是否相同
        serializer2 = UserSerializer(data=request.data)
        serializer2.is_valid()
        print(request.data["preferences"])
        big_label = request.data["preferences"]
        small_label = []
        label = {}

        for i in range(len(big_label)):
            small_label = small_label+label_convert.get(big_label[i])

        for i in range(len(small_label)):
            label[small_label[i]] = 1 #小標籤評分


        serializer3 = UserLikeSerializer(data=label)
        serializer3.is_valid()
        serializer3.save()

        serializer2.save()
        serializer.save()

        name = request.data['username']
        uid = UserInfo.objects.filter(username=name).values()[0]['uid']
        serializer4 = UserBaby.objects.create(uid=uid,babyid=1)
        serializer4.save()

        return Response({
            'success':True
        })

@api_view(['POST'])
def get_user_money(request):
    user = request.user
    if user.is_authenticated:
        uid = user.id
        money = UserInfo.objects.filter(uid=uid).values()[0]['money']
        return Response({
            'coins':money
        })
    else:
        return Response({
            'error':'not authenticated'
        },status = 400)

