from django.shortcuts import render
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CostSerializer
from restaurant.models import Restaurant
from .models import CostDetail
from django.db.models import Sum



class cost_detail(generics.GenericAPIView):
    serializer_class = CostSerializer
    def post(self, request, *args, **kwargs):
        updated_request = request.data.copy()
        user = request.user
        if user.is_authenticated:
            user_id = user.id
            rid = Restaurant.objects.filter(rname=request.data['ResName']).values()
            updated_request.update({'uid':user_id,'rid':rid[0]['rid']})
            serializer = self.get_serializer(data = updated_request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'success': True
            })
        return Response({
            'success': False
        })

@api_view(['POST'])
def cost_record(request):
    user = request.user
    date = request.data['date']
    data = []
    if user.is_authenticated:
        user_id = user.id
        for i in range(len(CostDetail.objects.filter(uid = user_id,date=date).values())):
            data.append(CostDetail.objects.filter(uid = user_id,date=date).values()[i])
        total = CostDetail.objects.filter(uid=user_id, date=date).aggregate(total=Sum('price'))
        return Response({
            'data':data,
            'total':total,
            'success': True
        })
    return Response({
        'success': False
    })
@api_view(['POST'])
def cost_record_month(request):
    user = request.user
    year = request.data['year']
    month = request.data['month']
    breakfast= 0
    lunch= 0
    dinner= 0
    other= 0
    if user.is_authenticated:
        user_id = user.id
        month_detail = CostDetail.objects.filter(uid = user_id,date__year=year,date__month=month).values()
        for i in range(len(month_detail)):
            if month_detail[i]['which_meal'] == 0:
                breakfast = breakfast + month_detail[i]['price']
            elif month_detail[i]['which_meal'] == 1:
                lunch = lunch + month_detail[i]['price']
            elif month_detail[i]['which_meal'] == 2:
                dinner = dinner + month_detail[i]['price']
            else:
                other = other + month_detail[i]['price']
        # 忘記要哪種格式了
        return Response({
            'breakfast':{'breakfast':breakfast},
            'lunch':lunch,
            'dinner':dinner,
            'other':other,
            'success': True
        })
    return Response({
        'success': False
    })