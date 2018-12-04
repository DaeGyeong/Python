from django.shortcuts import render
from django.http import HttpResponse
from urllib.error import HTTPError, URLError
from django.views.decorators.csrf import csrf_exempt
import os, sys, ast, json, time, base64, hmac, hashlib
import urllib.request


@csrf_exempt
def ServiceUrl(request, category, service):
    return render(request, 'ncloud/' + category + '/' + service + '.html')

@csrf_exempt
def Hmac_Ajax(request, uri):
    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)
    api_key = request.POST.get("api_key")
    access_key = request.POST.get("access_key")
    secret_key = request.POST.get("secret_key")
    secret_key = bytes(secret_key, 'UTF-8')

    method = "GET"
    if uri == '/api-test/v1/api':
        url = "https://ta50do4nv5.apigw.ntruss.com" + uri
        message = method + " " + uri + "\n" + timestamp + "\n" + access_key
        sig = "x-ncp-apigw-signature-v2"
    else:
        url = "https://ncloud.apigw.ntruss.com" + uri
        message = method + " " + uri + "\n" + timestamp + "\n" + api_key + "\n" + access_key
        sig = "x-ncp-apigw-signature-v1"
    message = bytes(message, 'UTF-8')
    signingKey = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    sig_key = signingKey.decode('utf-8')

    req = urllib.request.Request(url)
    req.add_header("X-ncp-apigw-timestamp", timestamp)
    req.add_header("x-ncp-apigw-api-key", api_key)
    req.add_header("x-ncp-iam-access-key", access_key)
    req.add_header(sig, sig_key)
    res = urllib.request.urlopen(req)

    return res


@csrf_exempt
def App_Ajax(request, url):
    client_id = request.POST.get("client_id")
    client_secret = request.POST.get("client_secret")
    req = urllib.request.Request(url)
    req.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    req.add_header("X-NCP-APIGW-API-KEY",client_secret)
    return req


@csrf_exempt
def IaaS(request):
    rescode = "잘못된 method 입니다."
    rtnVal = {'rescode': rescode}
    if request.method=='POST':
        uri = request.POST.get("uri")
        api_list = request.POST.get("url_list")

        if request.POST.get("query") == None:
            qstring = ""
        else:
            qstring = request.POST.get("query")

        if '?' in api_list:
            queryCon = "&"
        else:
            queryCon = "?"
        uri = uri + api_list + queryCon + 'responseFormatType=json&' + qstring

        url = 'https://ncloud.apigw.ntruss.com' + uri
        try:
            res = Hmac_Ajax(request, uri)
        except URLError as e:
            rescode = "client_id 또는 client_secret 값을 확인해 주세요"
        except HTTPError as e:
            rescode = "client_id 또는 client_secret 값을 확인해 주세요"
        else:
            rescode = res.getcode()
        if(rescode == 200):
            response_body = res.read()
            result = response_body.decode()
            result = result[2:-1]
            rtnVal = {"rescode": rescode, "result": result}
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
        else:
            rtnVal = {"rescode": rescode}
            print("Error Code:" + rescode)
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
    else:
        return HttpResponse(json.dumps(rtnVal), content_type='application/json')
