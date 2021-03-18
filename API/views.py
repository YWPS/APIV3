import json

from django.core import serializers
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .models import Product


@csrf_exempt
def CreateProduct(request, name):
    if request.method == "POST":
        # decode json
        jsonUnicode = request.body.decode('utf-8')
        jsonData = json.loads(jsonUnicode)
        # required fields
        code1code = jsonData["code1code"]
        code2code = jsonData["code2code"]
        code3code = jsonData["code3code"]
        code1name = jsonData["code1name"]
        code2name = jsonData["code2name"]
        code3name = jsonData["code3name"]
        username = jsonData["username"]
        # authenticate user
        user = username
        hash = get_random_string(length=40)
        # update or create model
        Product.objects.update_or_create(
            user=user, name=name, hash=hash, code1code=code1code, code2code=code2code, code3code=code3code, code1name=code1name, code2name=code2name, code3name=code3name)

        # response
        return JsonResponse({
            "url": f"https://api.qrserver.com/v1/create-qr-code/?data={hash}?size=1024*1024"
        })


@csrf_exempt
def GetProduct(request, hash):
    target = Product.objects.get(hash=hash)
    return JsonResponse({
        'name': target.name,
        "code1name": target.code1name,
        "code1code": target.code1code,
        "code2name": target.code2name,
        "code2code": target.code2code,
        "code3name": target.code3name,
        "code3code": target.code3code,
        'user': target.user
    })


@csrf_exempt
def UpdateProduct(request, hash):
    if request.method == "POST":
        # decode json
        jsonUnicode = request.body.decode('utf-8')
        jsonData = json.loads(jsonUnicode)
        # required fields
        name = jsonData["name"]
        code = str(jsonData["code"])
        username = jsonData["username"]
        # authenticate user
        user = User.objects.get(username=username)
        # update or create model
        Product.objects.update_or_create(
            name=name, code=code, user=user,  hash=hash)
        # response
        return JsonResponse({
            "url": f"https://api.qrserver.com/v1/create-qr-code/?data={hash};size=1024*1024"
        })


@csrf_exempt
def DeleteProduct(request, hash):
    Product.objects.get(hash=hash).delete()
    return JsonResponse({})


@csrf_exempt
def CreateUser(request, username):
    if request.method == "POST":
        jsonUnicode = request.body.decode('utf-8')
        jsonData = json.loads(jsonUnicode)
        password = jsonData["password"]
        User.objects.create_user(username=username, password=password)
        return JsonResponse({})


def GetUser(request, username):
    target = User.objects.get(username=username)
    products = eval(serializers.serialize(
        'json', Product.objects.filter(user=target)))
    output = []
    for item in products:
        output.append(item["fields"]["name"])
    return JsonResponse(
        {
            "username": target.username,
            "Products": output
        }
    )


@csrf_exempt
def UpdateUsername(request):
    if request.method == "POST":
        jsonUnicode = request.body.decode('utf-8')
        jsonData = json.loads(jsonUnicode)
        oldusername = jsonData["oldusername"]
        newusername = jsonData["newusername"]
        target = User.objects.get(username=oldusername)
        target.username = newusername
        target.save()
        return JsonResponse({})


@csrf_exempt
def UpdatePassword(request):
    if request.method == "POST":
        jsonUnicode = request.body.decode('utf-8')
        jsonData = json.loads(jsonUnicode)
        username = jsonData["username"]
        newpassword = jsonData["newpassword"]
        target = User.objects.get(username=username)
        target.set_password(newpassword)
        return JsonResponse({})


def DeleteUser(request, username):
    User.objects.delete(username=username)
    return JsonResponse({})


@csrf_exempt
def AuthUser(request, username):
    if request.method == "POST":
        jsonUnicode = request.body.decode('utf-8')
        jsonData = json.loads(jsonUnicode)
        password = jsonData["password"]
        if authenticate(username=username, password=password) is None:
            return JsonResponse({
                "fail": True
            })
        return JsonResponse({
            "fail": False
        })
