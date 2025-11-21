from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import User, carInfo, UserCarDetail, AllCarInfo
from rest_framework.decorators import api_view
import json
import datetime
from .utils import getPublicData
from .utils import getCenterData
from .utils import getCenterLeftData
from .utils import getBottomLeftData
from .utils.getCenterRightData import getPriceSortData
from .utils import getCenterChangeData
from .utils import getBottomRightData
import re
from django.db.models import Count, Avg, Q
import subprocess
import sys
import os
import psutil

# Create your views here.

# 全局变量用于存储爬虫进程
crawler_process = None

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            # 验证用户名和密码
            user = User.objects.filter(username=username, password=password).first()
            if user:
                return JsonResponse({'success': True, 'message': '登录成功'})
            else:
                return JsonResponse({'success': False, 'message': '用户名或密码错误'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': '仅支持POST请求'})
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
        realData = getPriceSortData()
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
def user_info(request):
    if request.method == 'GET':
        return JsonResponse({'detail': 'send POST to get user info'})
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            user = User.objects.get(username=username)
            
            if user:
                return JsonResponse({
                    'success': True,
                    'message': '获取用户信息成功',
                    'userInfo': {
                        'id': user.id,
                        'username': user.username,
                        'createTime': user.createTime.strftime('%Y-%m-%d %H:%M:%S')
                    }
                })
            else:
                return JsonResponse({'success': False, 'message': '用户不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

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
            car_obj = carInfo.objects.filter(id=userCarDetail.car_id).first()
            car_data = None
            if car_obj:
                try:
                    s = str(car_obj.price).replace('[','').replace(']','').replace(' ','').split(',')
                    newprice = []
                    for i in s:
                        newprice.append(float(i))
                except Exception:
                    newprice = []
                car_data = {
                    'id': car_obj.id,
                    'brand': car_obj.brand,
                    'carName': car_obj.carName,
                    'carImg': car_obj.carImg,
                    'saleVolume': car_obj.saleVolume,
                    'price': car_obj.price,
                    'manufacturer': car_obj.manufacturer,
                    'rank': car_obj.rank,
                    'carModel': car_obj.carModel,
                    'energyType': car_obj.energyType,
                    'marketTime': car_obj.marketTime,
                    'insure': car_obj.insure,
                    'newprice': newprice
                }

            usercardetail = UserCarDetail.objects.filter(user_id=userid).values().first()
            if usercardetail is not None:
                # 附加价格区间
                price_range = []
                if car_obj and car_obj.price:
                    try:
                        price_range = [float(x) for x in str(car_obj.price).strip('[]').split(',')]
                    except Exception:
                        price_range = []
                usercardetail['priceRange'] = price_range
            
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


# 管理员面板综合API - 一次性返回所有需要的数据
def getAdminDashboardData(request):
    if request.method == 'GET':
        try:
            # 获取用户列表（已格式化）
            users = User.objects.all()
            user_list = []
            for user in users:
                user_list.append({
                    'id': user.id,
                    'username': user.username,
                    'role': '管理员' if user.id == 1 else '普通用户',
                    'createdAt': user.createTime.strftime('%Y-%m-%d') if user.createTime else ''
                })
            
            # 获取用户统计数据
            total_users = User.objects.count()
            users_with_cars = UserCarDetail.objects.values('user').distinct().count()
            today = datetime.date.today()
            today_new_users = User.objects.filter(createTime__date=today).count()
            
            # 获取汽车信息列表 - 从allcarinfo表获取
            cars = AllCarInfo.objects.all()
            car_list = []
            for car in cars:
                # 处理价格数据
                price_range = []
                if car.price:
                    try:
                        price_range = [float(x) for x in car.price.strip('[]').split(',')]
                    except Exception:
                        price_range = [0, 0]
                
                car_list.append({
                    'id': car.id,
                    'brand': car.brand,
                    'carName': car.carName,
                    'energyType': car.energyType,
                    'price': car.price,
                    'priceRange': price_range,
                    'marketTime': car.marketTime
                })
            
            # 获取用户汽车详情
            user_car_details = UserCarDetail.objects.all()
            details_list = []
            for detail in user_car_details:
                # 添加用户名信息
                user_name = detail.user.username if detail.user else '未知用户'
                
                details_list.append({
                    'username': user_name,
                    'carName': detail.car_name or '-',
                    'model': detail.car_model or '-',
                    'purchaseDate': detail.purchase_date.strftime('%Y-%m-%d') if detail.purchase_date else '-'
                })
            
            # 整合所有数据并返回
            return JsonResponse({
                'success': True,
                'users': user_list,
                'userStats': {
                    'totalUsers': total_users,
                    'usersWithCars': users_with_cars,
                    'todayNewUsers': today_new_users,
                    'activeUsers': users_with_cars
                },
                'carInfoList': car_list,
                'userCarDetails': details_list,
                'totalData': len(car_list),
                'dataTypes': AllCarInfo.objects.values('energyType').distinct().count()
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

# 管理员面板API
def getUsersList(request):
    if request.method == 'GET':
        try:
            users = User.objects.all()
            user_list = []
            for user in users:
                user_list.append({
                    'id': user.id,
                    'username': user.username,
                    'role': '管理员' if user.id == 1 else '普通用户',  # 直接在后端判断用户角色
                    'createdAt': user.createTime.strftime('%Y-%m-%d') if user.createTime else ''  # 日期格式化移至后端
                })
            return JsonResponse({'success': True, 'users': user_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


def getCarInfoList(request):
    if request.method == 'GET':
        try:
            # 从allcarinfo表获取数据
            cars = AllCarInfo.objects.all()
            car_list = []
            for car in cars:
                # 处理价格数据
                price_range = []
                if car.price:
                    try:
                        price_range = [float(x) for x in car.price.strip('[]').split(',')]
                    except Exception:
                        price_range = [0, 0]
                
                car_list.append({
                    'id': car.id,
                    'brand': car.brand,
                    'carName': car.carName,
                    'carImg': car.carImg,
                    'saleVolume': car.saleVolume,
                    'price': car.price,
                    'priceRange': price_range,
                    'manufacturer': car.manufacturer,
                    'rank': car.rank,
                    'carModel': car.carModel,
                    'energyType': car.energyType,
                    'marketTime': car.marketTime,
                    'insure': car.insure
                })
            return JsonResponse({'success': True, 'cars': car_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


def searchCarInfo(request):
    if request.method == 'GET':
        try:
            carName = request.GET.get('carName', '')
            if not carName:
                return JsonResponse({'success': False, 'message': '请输入搜索关键词'})
            
            # 在allcarinfo表中搜索类似匹配的车辆，支持品牌、车型和车名的搜索
            cars = AllCarInfo.objects.filter(
                Q(brand__icontains=carName) | 
                Q(carName__icontains=carName) | 
                Q(carModel__icontains=carName)
            )
            
            car_list = []
            for car in cars:
                # 处理价格数据
                price_range = []
                if car.price:
                    try:
                        price_range = [float(x) for x in car.price.strip('[]').split(',')]
                    except Exception:
                        price_range = [0, 0]
                
                car_list.append({
                    'id': car.id,
                    'brand': car.brand,
                    'carName': car.carName,
                    'carImg': car.carImg,
                    'saleVolume': car.saleVolume,
                    'price': car.price,
                    'priceRange': price_range,
                    'manufacturer': car.manufacturer,
                    'rank': car.rank,
                    'carModel': car.carModel,
                    'energyType': car.energyType,
                    'marketTime': car.marketTime,
                    'insure': car.insure
                })
            
            return JsonResponse({'success': True, 'carInfoList': car_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


def getUserStats(request):
    if request.method == 'GET':
        try:
            # 计算用户总数
            total_users = User.objects.count()
            
            # 计算拥有车辆的用户数
            users_with_cars = UserCarDetail.objects.values('user').distinct().count()
            
            # 计算汽车总数 - 从allcarinfo表获取
            total_cars = AllCarInfo.objects.count()
            
            # 计算平均每用户车辆数
            avg_cars_per_user = 0
            if total_users > 0:
                avg_cars_per_user = round(users_with_cars / total_users, 2)
            
            # 获取能源类型分布 - 从allcarinfo表获取
            energy_stats = AllCarInfo.objects.values('energyType').annotate(count=Count('id'))
            energy_distribution = {}
            for item in energy_stats:
                energy_distribution[item['energyType']] = item['count']
            
            # 获取品牌分布 - 从allcarinfo表获取
            brand_stats = AllCarInfo.objects.values('brand').annotate(count=Count('id'))
            brand_distribution = {}
            for item in brand_stats:
                brand_distribution[item['brand']] = item['count']
            
            # 计算今日新增用户数
            today = datetime.date.today()
            today_new_users = User.objects.filter(createTime__date=today).count()
            
            # 计算活跃用户数（拥有车辆的用户）
            active_users = users_with_cars
            
            return JsonResponse({
                'success': True,
                'stats': {
                    'totalUsers': total_users,
                    'usersWithCars': users_with_cars,
                    'totalCars': total_cars,
                    'avgCarsPerUser': avg_cars_per_user,
                    'energyDistribution': energy_distribution,
                    'brandDistribution': brand_distribution,
                    'todayNewUsers': today_new_users,
                    'activeUsers': active_users
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


def getUpdateLogs(request):
    if request.method == 'GET':
        try:
            # 模拟更新日志数据
            logs = [
                {
                    'id': 1,
                    'timestamp': '2023-08-26 10:30:00',
                    'operation': '系统更新',
                    'description': '优化了数据加载性能',
                    'operator': '系统管理员',
                    'updateTime': '2023-08-26 10:30:00'
                },
                {
                    'id': 2,
                    'timestamp': '2023-08-25 15:45:00',
                    'operation': '数据更新',
                    'description': '更新了车辆信息数据',
                    'operator': '数据管理员',
                    'updateTime': '2023-08-25 15:45:00'
                },
                {
                    'id': 3,
                    'timestamp': '2023-08-24 09:15:00',
                    'operation': '用户添加',
                    'description': '添加了3个新用户',
                    'operator': '系统管理员',
                    'updateTime': '2023-08-24 09:15:00'
                }
            ]
            return JsonResponse({'success': True, 'logs': logs})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def searchUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            keyword = data.get('keyword', '')
            
            if not keyword:
                users = User.objects.all()
            else:
                users = User.objects.filter(username__icontains=keyword)
            
            user_list = []
            for user in users:
                user_list.append({
                    'id': user.id,
                    'username': user.username,
                    'role': '管理员' if user.id == 1 else '普通用户',  # 直接在后端判断用户角色
                    'createdAt': user.createTime.strftime('%Y-%m-%d') if user.createTime else ''  # 日期格式化移至后端
                })
            
            return JsonResponse({'success': True, 'users': user_list})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def updateUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('id')
            username = data.get('username')
            
            if not user_id or not username:
                return JsonResponse({'success': False, 'message': '缺少必要参数'})
            
            user = User.objects.get(id=user_id)
            user.username = username
            user.save()
            
            return JsonResponse({'success': True, 'message': '更新成功'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def deleteUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('id')
            
            if not user_id:
                return JsonResponse({'success': False, 'message': '缺少用户ID'})
            
            user = User.objects.get(id=user_id)
            user.delete()
            
            return JsonResponse({'success': True, 'message': '删除成功'})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def addUser(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({'success': False, 'message': '缺少用户名或密码'})
            
            # 验证用户名长度
            if len(username) > 8:
                return JsonResponse({'success': False, 'message': '用户名最多8个字符'})
            
            # 验证密码长度
            if len(password) < 8 or len(password) > 12:
                return JsonResponse({'success': False, 'message': '密码必须是8-12个字符'})
            
            # 检查用户名是否已存在
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': '用户名已存在'})
            
            # 创建新用户
            user = User(username=username, password=password)
            user.save()
            
            return JsonResponse({'success': True, 'message': '添加成功'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def getUserCarDetails(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            user_id = data.get('userId')
            
            if not user_id:
                return JsonResponse({'success': False, 'message': '缺少用户ID'})
            
            user = User.objects.get(id=user_id)
            user_car_details = UserCarDetail.objects.filter(user=user)
        elif request.method == 'GET':
            # GET请求返回所有用户的汽车详情
            user_car_details = UserCarDetail.objects.all()
        else:
            return JsonResponse({'success': False, 'message': '不支持的请求方法'})
    
        details_list = []
        for detail in user_car_details:
            car_data = None
            if detail.car:
                car = detail.car
                price_range = []
                if car.price:
                    try:
                        price_range = [float(x) for x in car.price.strip('[]').split(',')]
                    except Exception:
                        price_range = [0, 0]
                
                car_data = {
                    'id': car.id,
                    'brand': car.brand,
                    'carName': car.carName,
                    'priceRange': price_range
                }
            
            # 添加用户名信息
            user_name = detail.user.username if detail.user else '未知用户'
            
            details_list.append({
                'id': detail.id,
                'user_name': user_name,  # 添加用户名
                'car_name': detail.car_name,
                'car_model': detail.car_model,
                'mileage': detail.mileage,
                'purchase_date': detail.purchase_date.strftime('%Y-%m-%d'),
                'configuration': detail.configuration,
                'car_data': car_data
            })
        
        return JsonResponse({'success': True, 'details': details_list})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def getCarDataStats(request):
    if request.method == 'GET':
        try:
            # 计算汽车总数 - 从allcarinfo表获取
            total_data = AllCarInfo.objects.count()
            
            # 计算能源类型数量 - 从allcarinfo表获取
            energy_types = AllCarInfo.objects.values('energyType').distinct()
            data_types = energy_types.count()
            
            return JsonResponse({
                'success': True,
                'stats': {
                    'totalData': total_data,
                    'dataTypes': data_types
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


import sys
import subprocess
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import psutil

# 检查自动更新服务状态
@csrf_exempt
def checkAutoUpdateStatus(request):
    if request.method == 'GET':
        try:
            # 检查是否有auto_update.py进程在运行
            auto_update_running = False
            process_info = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # 检查进程是否为Python并且命令行中包含auto_update.py
                    if proc.info['name'].lower() == 'python.exe' and proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline'])
                        if 'auto_update.py' in cmdline:
                            auto_update_running = True
                            process_info.append({
                                'pid': proc.info['pid'],
                                'cmdline': cmdline
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # 检查日志文件是否存在
            log_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'update.log')
            log_exists = os.path.exists(log_file)
            
            return JsonResponse({
                'success': True,
                'status': 'running' if auto_update_running else 'stopped',
                'processes': process_info,
                'log_file_exists': log_exists
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    else:
        return JsonResponse({
            'success': False,
            'error': '只支持GET请求'
        }, status=400)

# 执行数据更新
@csrf_exempt
def executeDataUpdate(request):
    # 在函数开头声明使用全局变量
    global crawler_process
    
    if request.method == 'POST':
        try:
            # 同时支持从request.body和request.POST获取参数
            try:
                data = json.loads(request.body)
                update_type = data.get('updateType', 'full')
            except json.JSONDecodeError:
                # 如果body不是JSON格式，尝试从POST表单获取
                update_type = request.POST.get('updateType', 'full')
            
            if update_type == 'full':
                # 手动更新优先：若有自动更新或其它爬虫在运行，则先停止
                try:
                    running_pids = []
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        if proc.info['name'].lower() == 'python.exe' and proc.info['cmdline']:
                            cmdline = ' '.join(proc.info['cmdline'])
                            if ('auto_update.py' in cmdline) or ('spiderMan' in cmdline and 'spiders.py' in cmdline):
                                running_pids.append(proc.info['pid'])
                    for pid in running_pids:
                        try:
                            p = psutil.Process(pid)
                            p.terminate()
                            p.wait(timeout=20)
                        except Exception:
                            try:
                                p.kill()
                            except Exception:
                                pass
                except Exception:
                    pass
                # 清理锁文件
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                lock_file_path = os.path.join(project_root, 'spiderMan', 'update.lock')
                try:
                    if os.path.exists(lock_file_path):
                        os.remove(lock_file_path)
                except Exception:
                    pass
                # 获取项目根目录
                print(f"项目根目录: {project_root}")
                
                # 设置环境变量
                env = os.environ.copy()
                env['PYTHONPATH'] = project_root
                # 明确设置Django设置模块
                env['DJANGO_SETTINGS_MODULE'] = 'DeviseProject.settings'
                print(f"设置后的PYTHONPATH: {env['PYTHONPATH']}")
                print(f"设置后的DJANGO_SETTINGS_MODULE: {env['DJANGO_SETTINGS_MODULE']}")
                
                # 正确的爬虫脚本路径
                spider_script_path = os.path.join(project_root, 'spiderMan', 'spiders.py')
                print(f"爬虫脚本路径: {spider_script_path}")
                
                # 确保爬虫脚本存在
                if not os.path.exists(spider_script_path):
                    error_msg = f"爬虫脚本不存在: {spider_script_path}"
                    print(error_msg)
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    })
                
                # 创建日志文件路径
                log_file_path = os.path.join(project_root, 'spiderMan', 'crawler_logs.txt')
                
                # 清除之前的日志
                if os.path.exists(log_file_path):
                    with open(log_file_path, 'w', encoding='utf-8') as f:
                        f.write('')
                
                # 使用subprocess.Popen启动爬虫脚本，不使用shell=True以提高安全性
                process = subprocess.Popen(
                    [sys.executable, spider_script_path],  # 使用sys.executable确保使用正确的Python解释器
                    env=env,
                    cwd=project_root,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # 保存进程ID到会话或其他存储方式，以便后续可以终止它
                # 这里为了简化，我们将进程ID保存到全局变量
                global crawler_process
                crawler_process = process
                
                # 创建一个线程来读取输出并写入日志文件
                def read_output(process, log_file):
                    with open(log_file, 'a', encoding='utf-8') as f:
                        while True:
                            output = process.stdout.readline()
                            if output == '' and process.poll() is not None:
                                break
                            if output:
                                # 写入到日志文件
                                f.write(output.strip() + '\n')
                                f.flush()  # 立即写入文件，不缓冲
                            
                        # 读取错误输出
                        error_output = process.stderr.read()
                        if error_output:
                            f.write(f"错误: {error_output.strip()}\n")
                            f.flush()
                
                # 启动线程读取输出
                import threading
                log_thread = threading.Thread(target=read_output, args=(process, log_file_path))
                log_thread.daemon = True
                log_thread.start()
                
                print(f"成功启动爬虫进程，PID: {process.pid}")
                return JsonResponse({
                    'success': True,
                    'message': '数据更新已开始，请耐心等待完成'
                })
            elif update_type == 'stop':
                # 停止数据更新的逻辑
                try:
                    if crawler_process and crawler_process.poll() is None:
                        # 进程仍在运行，尝试终止它
                        # 在Windows系统上使用terminate
                        # 在Unix系统上可能需要使用kill
                        try:
                            crawler_process.terminate()
                            # 等待进程终止，最多等待5秒
                            crawler_process.wait(timeout=35)
                            # 记录到日志文件
                            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                            log_file_path = os.path.join(project_root, 'spiderMan', 'crawler_logs.txt')
                            with open(log_file_path, 'a', encoding='utf-8') as f:
                                f.write('\n数据更新已被用户手动停止\n')
                            
                            print(f"成功终止爬虫进程，PID: {crawler_process.pid}")
                            crawler_process = None
                            return JsonResponse({
                                'success': True,
                                'message': '数据更新已停止'
                            })
                        except subprocess.TimeoutExpired:
                            # 超时，强制终止
                            crawler_process.kill()
                            print(f"强制终止爬虫进程，PID: {crawler_process.pid}")
                            crawler_process = None
                            return JsonResponse({
                                'success': True,
                                'message': '数据更新已强制停止'
                            })
                    else:
                        # 进程已不存在或已结束
                        print("没有正在运行的爬虫进程")
                        return JsonResponse({
                            'success': True,
                            'message': '没有正在运行的数据更新'
                        })
                except Exception as stop_error:
                    error_msg = f"停止数据更新时出错: {str(stop_error)}"
                    print(error_msg)
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': '不支持的更新类型'
                })
        except Exception as e:
            # 记录详细的错误信息
            error_msg = f"执行数据更新失败: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'message': error_msg
            })
    else:
        return JsonResponse({
            'success': False,
            'message': '仅支持POST请求'
        })


@csrf_exempt
def getCrawlerLogs(request):
    if request.method == 'GET':
        try:
            # 获取项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # 日志文件路径
            log_file_path = os.path.join(project_root, 'spiderMan', 'crawler_logs.txt')
            
            # 检查日志文件是否存在
            if not os.path.exists(log_file_path):
                return JsonResponse({
                    'success': True,
                    'logs': []
                })
            
            # 读取日志文件内容
            with open(log_file_path, 'r', encoding='utf-8') as f:
                logs = f.readlines()
            
            # 去除每行的换行符
            logs = [log.strip() for log in logs]
            
            # 限制返回的日志数量，避免数据过大
            max_logs = 100
            recent_logs = logs[-max_logs:] if len(logs) > max_logs else logs
            
            return JsonResponse({
                'success': True,
                'logs': recent_logs
            })
        except Exception as e:
            error_msg = f"获取爬虫日志失败: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'message': error_msg
            })
    else:
        return JsonResponse({
            'success': False,
            'message': '仅支持GET请求'
        })


# 获取自动更新服务日志
@csrf_exempt
def getAutoUpdateLogs(request):
    if request.method == 'GET':
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_file_path = os.path.join(project_root, 'spiderMan', 'auto_update_logs.txt')
            if not os.path.exists(log_file_path):
                return JsonResponse({'success': True, 'logs': []})
            with open(log_file_path, 'r', encoding='utf-8') as f:
                logs = [line.strip() for line in f.readlines()]
            recent_logs = logs[-100:] if len(logs) > 100 else logs
            return JsonResponse({'success': True, 'logs': recent_logs})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    else:
        return JsonResponse({'success': False, 'message': '仅支持GET请求'})

# 启动自动更新服务
@csrf_exempt
def startAutoUpdate(request):
    if request.method == 'POST':
        try:
            global auto_update_process
            
            # 如果已有进程在运行，先停止它
            if 'auto_update_process' in globals() and auto_update_process and auto_update_process.poll() is None:
                auto_update_process.terminate()
                auto_update_process.wait(timeout=10)
                
            # 获取项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # 设置环境变量
            env = os.environ.copy()
            env['PYTHONPATH'] = project_root
            env['DJANGO_SETTINGS_MODULE'] = 'DeviseProject.settings'
            
            # 自动更新脚本路径
            auto_update_script = os.path.join(project_root, 'spiderMan', 'auto_update.py')
            
            # 启动自动更新进程
            process = subprocess.Popen(
                [sys.executable, auto_update_script],
                env=env,
                cwd=project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 保存进程引用
            auto_update_process = process
            
            # 创建线程读取输出并写入日志
            def read_output(process):
                log_file_path = os.path.join(project_root, 'spiderMan', 'auto_update_logs.txt')
                with open(log_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now()}] 自动更新服务启动 (PID: {process.pid})\n")
                    f.flush()
                    
                    while True:
                        output = process.stdout.readline()
                        if output == '' and process.poll() is not None:
                            break
                        if output:
                            f.write(f"[{datetime.now()}] [输出] {output.strip()}\n")
                            f.flush()
                    
                    # 读取错误输出
                    error_output = process.stderr.read()
                    if error_output:
                        f.write(f"[{datetime.now()}] [错误] {error_output.strip()}\n")
                        f.flush()
                    
                    # 记录进程结束信息
                    exit_code = process.returncode
                    status = "正常结束" if exit_code == 0 else f"异常结束 (退出码: {exit_code})"
                    f.write(f"[{datetime.now()}] 自动更新服务{status}\n")
                    f.flush()
            
            # 启动日志记录线程
            import threading
            from datetime import datetime
            log_thread = threading.Thread(target=read_output, args=(process,))
            log_thread.daemon = True
            log_thread.start()
            
            return JsonResponse({
                'success': True,
                'message': '自动更新服务已启动，每5分钟检查一次排行榜变化'
            })
            
        except Exception as e:
            error_msg = f"启动自动更新服务失败: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'message': error_msg
            })
    else:
        return JsonResponse({
            'success': False,
            'message': '仅支持POST请求'
        })




# 停止自动更新服务
@csrf_exempt
def stopAutoUpdate(request):
    if request.method == 'POST':
        try:
            global auto_update_process
            
            if 'auto_update_process' in globals() and auto_update_process and auto_update_process.poll() is None:
                auto_update_process.terminate()
                auto_update_process.wait(timeout=30)
                
                # 记录到日志文件
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                log_file_path = os.path.join(project_root, 'spiderMan', 'auto_update_logs.txt')
                with open(log_file_path, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.datetime.now()}] [用户操作] 自动更新服务已被手动停止\n")
                    f.flush()
                
                auto_update_process = None
                return JsonResponse({
                    'success': True,
                    'message': '自动更新服务已停止'
                })
            else:
                return JsonResponse({
                    'success': True,
                    'message': '没有正在运行的自动更新服务'
                })
                
        except Exception as e:
            error_msg = f"停止自动更新服务失败: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'message': error_msg
            })
    else:
        return JsonResponse({
            'success': False,
            'message': '仅支持POST请求'
        })

# 检查自动更新服务状态
@csrf_exempt
def checkAutoUpdateStatus(request):
    if request.method == 'GET':
        try:
            # 同时检查全局变量和系统进程，确保状态准确性
            global auto_update_process
            is_running = False
            pid = None
            
            # 先检查全局变量
            if 'auto_update_process' in globals() and auto_update_process and auto_update_process.poll() is None:
                is_running = True
                pid = auto_update_process.pid
            else:
                # 如果全局变量显示未运行，再通过psutil检查系统中是否有实际运行的auto_update.py进程
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        if proc.info['name'].lower() == 'python.exe' and proc.info['cmdline']:
                            cmdline = ' '.join(proc.info['cmdline'])
                            if 'auto_update.py' in cmdline:
                                is_running = True
                                pid = proc.info['pid']
                                break
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        pass
            
            return JsonResponse({
                'success': True,
                'is_running': is_running,
                'pid': pid,
                'message': '服务正在运行' if is_running else '服务未运行'
            })
        except Exception as e:
            error_msg = f"检查自动更新服务状态失败: {str(e)}"
            print(error_msg)
            return JsonResponse({
                'success': False,
                'message': error_msg
            })
    else:
        return JsonResponse({
            'success': False,
            'message': '仅支持GET请求'
        })



def updateCarInfo(request):
    """
    更新汽车信息
    """
    if request.method == 'POST':
        try:
            # 这里可以添加权限验证逻辑
            # 例如: if not request.user.is_staff: return JsonResponse({'code': 403, 'msg': '无权限操作'})
            
            # 执行数据更新逻辑
            # 这里假设有一个执行数据更新的函数
            from spiderMan.spiders import main as update_data
            update_data()
            
            return JsonResponse({
                'code': 200,
                'msg': '汽车信息更新成功',
                'data': None
            })
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'更新失败: {str(e)}',
                'data': None
            })
    else:
        return JsonResponse({
            'code': 405,
            'msg': '仅支持POST请求',
            'data': None
        })


def searchUsers(request):
    """
    搜索用户功能
    支持按用户名、邮箱或手机号搜索
    """
    if request.method == 'GET':
        query = request.GET.get('q', '').strip()
        
        if not query:
            return JsonResponse({
                'code': 400,
                'msg': '搜索关键词不能为空',
                'data': []
            })
        
        # 搜索用户（按用户名、邮箱、手机号）
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)  # 假设有phone字段
        ).values('id', 'username', 'email', 'phone', 'date_joined')
        
        user_list = list(users)
        
        return JsonResponse({
            'code': 200,
            'msg': f'找到 {len(user_list)} 个用户',
            'data': user_list
        })
    else:
        return JsonResponse({
            'code': 405,
            'msg': '仅支持GET请求',
            'data': None
        })


def admin_panel(request):
    """
    管理员面板视图函数
    """
    # 这里可以添加管理员权限验证逻辑
    # 例如: if not request.user.is_staff: return redirect('login')
    
    # 获取一些统计数据用于展示
    total_cars = carInfo.objects.count()
    total_users = User.objects.count()
    
    context = {
        'total_cars': total_cars,
        'total_users': total_users,
    }
    
    # 如果是AJAX请求，返回JSON数据
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'code': 200,
            'msg': '成功获取管理员面板数据',
            'data': context
        })
    
    # 否则渲染HTML模板
    # 注意: 你需要创建对应的HTML模板文件
    return render(request, 'admin_panel.html', context)


