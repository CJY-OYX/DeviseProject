from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import User, carInfo, UserCarDetail
from rest_framework.decorators import api_view
import json
import datetime
from .utils import getPublicData
from .utils import getCenterData
from .utils import getCenterLeftData
from .utils import getBottomLeftData
from .utils import getCenterRightData
from .utils import getCenterChangeData
from .utils import getBottomRightData
import re

# Create your views here.
def center(request):
    if request.method == 'GET':
        sumCar, highVolume, topCar, mostModel, mostBrand, averagePrice = getCenterData.getBaseData()
        lastSortList = getCenterData.getRollData()
        oilRate, electricRare, mixRate = getCenterData.getTypeRate()
        return JsonResponse({
            'sumCar': sumCar,
            'highVolume': highVolume,
            'topCar': topCar,
            'mostModel': mostModel,
            'mostBrand': mostBrand,
            'averagePrice': averagePrice,
            'lastSortList': lastSortList,
            'oilRate': oilRate,
            'electricRare': electricRare,
            'mixRate': mixRate,
        })

def centerLeft(request):
    if request.method == 'GET':
        lastPieList = getCenterLeftData.getPieBrandData()
        return JsonResponse({
            'lastPieList': lastPieList,
        })

def bottomLeft(request):
    if request.method == 'GET':
        brandList, volumeList, priceList = getBottomLeftData.getSquareData()
        return JsonResponse({
            'brandList': brandList,
            'volumeList': volumeList,
            'priceList': priceList,
        })

def centerRight(request):
    if request.method == 'GET':
        realData = getCenterRightData.getPriceSortData()
        return JsonResponse({
            'realData': realData,
        })

def centerRightChange(request, energyType):
    if request.method == 'GET':
        oilData, electricData = getCenterChangeData.getCircleData()
        realData = []
        if energyType == 1:
            realData = oilData
        else:
            realData = electricData
        return JsonResponse({
            'realData': realData,
        })

def bottomRight(request):
    if request.method == 'GET':
        carData = getBottomRightData.getRankData()
        return JsonResponse({
            'carData': carData,
        })

@csrf_exempt
@api_view(['GET'])
def search_cars(request):
    name = request.GET.get('name', '')
    if not name:
        return JsonResponse({'success': False, 'message': '请输入车辆名称'})

    # 在carInfo表中搜索类似匹配的车辆
    cars = carInfo.objects.filter(carName__icontains=name)
    car_list = []
    for car in cars:
        car_list.append({
            'id': car.id,
            'carName': car.carName,
            'carModel': car.carModel,
            'brand': car.brand
        })

    return JsonResponse({'success': True, 'cars': car_list})

@csrf_exempt
@api_view(['POST'])
def save_user_car_detail(request):
    try:
        data = json.loads(request.body)
        user_id = data.get('userId')
        car_name = data.get('carName')
        car_model = data.get('carModel')
        mileage = data.get('mileage')
        purchase_date = data.get('purchaseDate')
        configuration = data.get('configuration')

        if not all([user_id, car_name, car_model, mileage, purchase_date, configuration]):
            return JsonResponse({'success': False, 'message': '请填写所有字段'})

        # 查找用户
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'})

        # 尝试查找车辆
        car = None
        try:
            car = carInfo.objects.get(carName=car_name, carModel=car_model)
        except carInfo.DoesNotExist:
            # 车辆不存在，仍然可以保存，但car字段为null
            pass

        # 尝试查找现有记录
        user_car_detail = UserCarDetail.objects.filter(user=user).first()
        
        if user_car_detail:
            # 更新现有记录
            user_car_detail.car = car
            user_car_detail.car_name = car_name
            user_car_detail.car_model = car_model
            user_car_detail.mileage = mileage
            user_car_detail.purchase_date = datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date()
            user_car_detail.configuration = configuration
            user_car_detail.save()
        else:
            # 创建新记录
            user_car_detail = UserCarDetail(
                user=user,
                car=car,
                car_name=car_name,
                car_model=car_model,
                mileage=mileage,
                purchase_date=datetime.datetime.strptime(purchase_date, '%Y-%m-%d').date(),
                configuration=configuration
            )
            user_car_detail.save()

        return JsonResponse({'success': True, 'message': '车辆详情保存成功'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            # 获取前端发送的JSON数据
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            confirm_password = data.get('confirmPassword')

            # 验证数据
            if not username or not password or not confirm_password:
                return JsonResponse({'success': False, 'message': '请填写所有字段'})

            # 验证用户名长度
            if len(username) > 8:
                return JsonResponse({'success': False, 'message': '用户名最多8个字符'})

            # 验证密码长度
            if len(password) < 8 or len(password) > 12:
                return JsonResponse({'success': False, 'message': '密码必须是8-12个字符'})

            # 验证密码复杂度（至少包含两种字符类型）
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            has_symbol = any(not c.isalnum() for c in password)

            complexity_count = sum([has_upper, has_lower, has_digit, has_symbol])
            if complexity_count < 2:
                return JsonResponse({'success': False, 'message': '密码必须包含大写字母、小写字母、数字、符号中的至少两种'})

            if password != confirm_password:
                return JsonResponse({'success': False, 'message': '两次输入的密码不一致'})

            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': '用户名已存在'})

            # 创建新用户
            user = User(username=username, password=password)
            user.save()

            return JsonResponse({'success': True, 'message': '注册成功', 'userId': user.id})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': '不支持GET请求'})

from django.contrib.auth import authenticate

@csrf_exempt
def login(request):
    if request.method == 'GET':
        return JsonResponse({'detail': 'send POST to login'})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            user = User.objects.get(username=username)

            if user is None:
                return JsonResponse({'success': False, 'message': '用户名或密码错误'})
            else:
                return JsonResponse({'success': True, 'message': '登录成功','username': username})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'登录失败: {str(e)}'})

@csrf_exempt
def entry_user_info(request):
    if request.method == 'POST':
        try:
            # 解析请求体中的JSON数据
            data = json.loads(request.body)
            username = data.get('username')
            user_id = data.get('user_id')
            id = data.get('id')
            
            # 获取用户对象
            if username:
                user = User.objects.get(username=username)
            elif user_id:
                user = User.objects.get(id=user_id)
            elif id:
                user = User.objects.get(id=id)
            else:
                return JsonResponse({'success': False, 'message': '请提供用户名或用户ID'})
            
            userid = user.id
            
            # 查询用户车辆详情
            userCarDetail = UserCarDetail.objects.filter(user_id=userid).first()
            
            if not userCarDetail:
                return JsonResponse({'success': False, 'message': '详情信息未填写，即将前往填写页'})
            
            # 查询车辆信息
            car_data = carInfo.objects.filter(id=userCarDetail.car_id).values().first()

            usercardetail = UserCarDetail.objects.filter(user_id=userid).values().first()
            
            # 准备返回数据
            userinfo = {
                'id': userCarDetail.id,
                'user_id': userCarDetail.user_id,
                'car_id': userCarDetail.car_id,
                # 添加其他需要的字段
            }
            
            return JsonResponse({
                'success': True,
                'data': car_data,
                'userinfo': userinfo,
                'usercarinfo': usercardetail

            })
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User matching query does not exist.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@api_view(['POST'])
def get_user_info(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        
        if not username:
            return JsonResponse({'success': False, 'message': '用户名不能为空'})
        
        # 获取用户对象
        user = User.objects.get(username=username)
        
        # 准备用户信息
        user_info = {
            'id': user.id,
            'username': user.username,
            'createTime': user.createTime.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return JsonResponse({'success': True, 'userInfo': user_info})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@api_view(['POST'])
def get_car_info(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        
        if not username:
            return JsonResponse({'success': False, 'message': '用户名不能为空'})
        
        # 获取用户对象
        user = User.objects.get(username=username)
        
        # 查询用户车辆详情
        user_car_detail = UserCarDetail.objects.filter(user_id=user.id).first()
        
        if not user_car_detail or not user_car_detail.car_id:
            return JsonResponse({'success': False, 'message': '未找到关联的车辆信息'})
        
        # 查询车辆信息
        car = carInfo.objects.get(id=user_car_detail.car_id)
        s = car.price.replace('[','').replace(']','').replace(' ','').split(',')
        newprice = []
        for i in s:
            newprice.append(float(i))

        # 准备车辆信息
        car_info = {
            'id': car.id,
            'brand': car.brand,
            'carName': car.carName,
            'carImg': car.carImg,
            'saleVolume': car.saleVolume,
            'price': car.price,
            'manufacturer': car.manufacturer,
            'rank': car.rank,
            'carModel': car.carModel,
            'energyType': car.energyType,
            'marketTime': car.marketTime,
            'insure': car.insure,
            'newprice': newprice
        }
        
        return JsonResponse({'success': True, 'carInfo': car_info})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'})
    except carInfo.DoesNotExist:
        return JsonResponse({'success': False, 'message': '未找到车辆信息'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

@csrf_exempt
@api_view(['POST'])
def get_user_car_detail(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        
        if not username:
            return JsonResponse({'success': False, 'message': '用户名不能为空'})
        
        # 获取用户对象
        user = User.objects.get(username=username)
        
        # 查询用户车辆详情
        user_car_detail = UserCarDetail.objects.filter(user_id=user.id).first()
        
        if not user_car_detail:
            return JsonResponse({'success': False, 'message': '未找到用户车辆详情'})

        car = getattr(user_car_detail, 'car', None)
        price_range = [6.78, 11.38]
        if car and car.price:
            try:
                price_range = [float(x) for x in car.price.strip('[]').split(',')]
            except Exception:
                pass
        
        # 准备用户车辆详情
        car_detail = {
            'id': user_car_detail.id,
            'car_name': user_car_detail.car_name,
            'car_model': user_car_detail.car_model,
            'mileage': user_car_detail.mileage,
            'purchaseDate': user_car_detail.purchase_date.isoformat(),
            'configuration': user_car_detail.configuration,
            'createTime': user_car_detail.createTime.strftime('%Y-%m-%d %H:%M:%S'),
            'priceRange':price_range,
        }
        
        return JsonResponse({'success': True, 'userCarDetail': car_detail})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
@api_view(['POST'])
def if_user_car_detail(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        
        if not username:
            return JsonResponse({'success': False, 'message': '用户名不能为空'})
        
        # 获取用户对象
        user = User.objects.get(username=username)
        userid = user.id
        
        # 查询用户车辆详情
        user_car_detail = UserCarDetail.objects.filter(user_id=userid).first()
        
        if not user_car_detail:
            return JsonResponse({'success': False, 'message': '未找到用户车辆详情'})
        
        # 查询关联的车辆信息
        car_data = None
        if user_car_detail.car_id:
            car_data = carInfo.objects.filter(id=user_car_detail.car_id).values().first()
        
        # 准备返回数据
        result = {
            'success': True,
            'userid': userid,
            'user_car_detail': {
                'id': user_car_detail.id,
                'user_id': user_car_detail.user_id,
                'car_id': user_car_detail.car_id,
                'car_name': user_car_detail.car_name,
                'car_model': user_car_detail.car_model,
                'mileage': user_car_detail.mileage,
                'purchase_date': user_car_detail.purchase_date.strftime('%Y-%m-%d'),
                'configuration': user_car_detail.configuration
            },
            'car_data': car_data
        }
        
        return JsonResponse(result)
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


