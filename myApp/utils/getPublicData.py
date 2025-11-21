from myApp.models import carInfo

def getAllCars():
    return carInfo.objects.all()