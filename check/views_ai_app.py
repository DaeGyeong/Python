from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from urllib.error import HTTPError, URLError
import os, sys, ast, json, time, base64, hmac, hashlib
import urllib.request
from django.conf import settings
from ncloud.views import Hmac_Ajax, App_Ajax
from .models import NaverApiStatus
# from django.http import HttpResponseNotFound
# Create your views here.

def index(request):
    data = {}
    data['data'] = NaverApiStatus.objects.all()
    return render(request, 'ncloud/index.html', data)

def Clova(request):
    return render(request, 'ncloud/ai_application/clova.html')

def Maps(request):
    return render(request, 'ncloud/ai_application/maps.html')

@csrf_exempt
def Papago(request):
    if request.method=="POST":
        rtnVal = {}
        encText = urllib.parse.quote(request.POST.get("encText"))
        target_lang = request.POST.get("target_lang")
        data = "source=ko&target=" + target_lang + "&text=" + encText
        papago_target = request.POST.get("target")
        url = "https://naveropenapi.apigw.ntruss.com/" + papago_target + "/v1/translation"

        req = App_Ajax(request, url)

        try:
            res = urllib.request.urlopen(req, data=data.encode("utf-8"))
        except URLError as e:
            rescode = str(e)
        except HTTPError as e:
            rescode = str(e)
        else:
            rescode = res.getcode()

        if(rescode==200):
            response_body = res.read()
            result = response_body.decode('utf-8')
            result = ast.literal_eval(result)
            content = result['message']['result']
            rtnVal = {
                "rescode": rescode,
                "transText": content['translatedText'],
                "srcLangType": content['srcLangType'],
                "targetLangType": target_lang,
                "papago_target": papago_target
                }
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
        else:
            print("Error Code\n")
            print(rescode)
            result = response_body.decode('utf-8')
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
    else:
        return render(request, 'ncloud/ai_application/papago.html')

def nShortURL(request):
    return render(request, 'ncloud/ai_application/nshorturl.html')

@csrf_exempt
def CAPTCHA(request):
    if request.method=='POST':
        rtnVal = {}
        client_id = request.POST.get("client_id")
        client_secret = request.POST.get("client_secret")
        target = request.POST.get("target")

        if not client_id or not client_secret:
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
        code = "0"
        if target == 'IMG':
            url = "https://naveropenapi.apigw.ntruss.com/captcha/v1/nkey?code=" + code
        elif target == 'AUDIO':
            url = "https://naveropenapi.apigw.ntruss.com/scaptcha/v1/skey?code=" + code
        req = urllib.request.Request(url)
        req.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        req.add_header("X-NCP-APIGW-API-KEY",client_secret)
        try:
            res = urllib.request.urlopen(req)
        except URLError as e:
            rescode = str(e)
        except HTTPError as e:
            rescode = str(e)
        except targetError as e:
            rescode = "API Type 지정 해주세요."
        else:
            rescode = res.getcode()
        if(rescode == 200):
            response_body = res.read()
            result = response_body.decode('utf-8')
            result = ast.literal_eval(result)
            img_rescode = getCAPTCHA(result, client_id, client_secret, target)
            rtnVal = {"key_rescode": rescode, "img_rescode": img_rescode}
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
        else:
            print("Error Code:" + rescode)
            return HttpResponse(json.dumps(result), content_type='application/json')

    else:
        return render(request, 'ncloud/ai_application/captcha.html')

@csrf_exempt
def getCAPTCHA(result, client_id, client_secret, target):
    key = result['key']
    if target=='IMG':
        url = "https://naveropenapi.apigw.ntruss.com/captcha-bin/v1/ncaptcha?key=" + key + "&X-NCP-APIGW-API-KEY-ID=" + client_id;
        target_save = '/captcha.jpg'
    elif target=='AUDIO':
        url = "https://naveropenapi.apigw.ntruss.com/scaptcha-bin/v1/scaptcha?key=" + key + "&X-NCP-APIGW-API-KEY-ID=" + client_id;
        target_save = '/captcha.wav'
    req = urllib.request.Request(url)
    res = urllib.request.urlopen(req)
    rescode = res.getcode()
    if(rescode==200):
        response_body = res.read()
        with open(settings.MEDIA_ROOT + target_save, 'wb') as f:
            img = f.write(response_body)
        global tot
        tot = {
            'client_id': client_id,
            'client_secret': client_secret,
            'key': key,
            'target': target
        }
        return rescode
    else:
        print("Error Code:" + rescode)
        return rescode


@csrf_exempt
def CAPTCHA_Check(request):
    tot_value = tot
    client_id = tot_value['client_id']
    client_secret = tot_value['client_secret']
    code = "1"
    key = tot_value['key']
    value = request.POST.get("cap_value")
    if tot_value['target'] == 'IMG':
        url = "https://naveropenapi.apigw.ntruss.com/captcha/v1/nkey?code=" + code + "&key=" + key + "&value=" + value
    elif tot_value['target']:
        url = "https://naveropenapi.apigw.ntruss.com/scaptcha/v1/skey?code=" + code + "&key=" + key + "&value=" + value
    req = urllib.request.Request(url)
    req.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    req.add_header("X-NCP-APIGW-API-KEY",client_secret)
    res = urllib.request.urlopen(req)
    rescode = res.getcode()
    if(rescode==200):
        response_body = res.read()
        result = response_body.decode('utf-8')
        # result = ast.literal_eval(result)
        return HttpResponse(result)
    else:
        print("Error Code:" + rescode)
        return HttpResponse(rescode)



@csrf_exempt
def SearchTrend(request):
    if request.method=='POST':
        rtnVal = {}
        client_id = request.POST.get("client_id")
        client_secret = request.POST.get("client_secret")
        if not client_id or not client_secret:
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')

        url = "https://naveropenapi.apigw.ntruss.com/datalab/v1/search";
        body = "{\"startDate\":\"2017-01-01\",\"endDate\":\"2017-04-30\",\"timeUnit\":\"month\",\"keywordGroups\":[{\"groupName\":\"한글\",\"keywords\":[\"한글\",\"korean\"]},{\"groupName\":\"영어\",\"keywords\":[\"영어\",\"english\"]}],\"device\":\"pc\",\"ages\":[\"1\",\"2\"],\"gender\":\"f\"}";
        req = urllib.request.Request(url)
        req.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        req.add_header("X-NCP-APIGW-API-KEY",client_secret)
        try:
            res = urllib.request.urlopen(req, data=body.encode("utf-8"))
        except URLError as e:
            rescode = str(e)
        except HTTPError as e:
            rescode = str(e)
        else:
            rescode = res.getcode()

        if(rescode == 200):
            response_body = res.read()
            result = response_body.decode('utf-8')
            result = ast.literal_eval(result)
            rtnVal = {"key_rescode": rescode}
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
        else:
            print("Error Code:" + rescode)
            return HttpResponse(json.dumps(result), content_type='application/json')

    else:
        return render(request, 'ncloud/ai_application/searchtrend.html')

# CSS 호출
@csrf_exempt
def CSS(request):
    rescode = 1
    rtnVal = {"rescode": rescode}
    if request.method=='POST':
        encText = urllib.parse.quote("네이버 클로바 테스트 입니다.")
        data = "speaker=mijin&speed=0&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"

        request = App_Ajax(request, url)
        try:
            response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        except URLError as e:
            rescode = str(e)
        except HTTPError as e:
            rescode = str(e)
        else:
            rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            with open(settings.MEDIA_ROOT + '/NAVER_TEST.mp3', 'wb') as f:
                f.write(response_body)
            rtnVal["rescode"] = rescode
        else:
            rtnVal["rescode"] = rescode
        return HttpResponse(json.dumps(rtnVal), content_type='application/json')
    else:
        return HttpResponse(json.dumps(rtnVal), content_type='application/json')

# maps 호출
@csrf_exempt
def mapsTest(request):
    rescode = 1
    rtnVal = {"rescode": rescode}
    if request.method == 'POST':
        encText = urllib.parse.quote(request.POST.get("encText"))

        url = "https://naveropenapi.apigw.ntruss.com/map/v1/geocode?query=" + encText
        request = App_Ajax(request, url)

        try:
            response = urllib.request.urlopen(request)
        except HTTPError as e:
            rescode = str(e)
        except URLError as e:
            rescode = str(e)
        else:
            rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
            rtnVal["rescode"] = rescode
            rtnVal["resval"] = response_body.decode('utf-8')
        else:
            print("Error Code:" + rescode)
            rtnVal["rescode"] = rescode

        return HttpResponse(json.dumps(rtnVal), content_type='application/json')
    else:
        return HttpResponse(json.dumps(rtnVal), content_type='application/json')

# nShortURL 호출
@csrf_exempt
def nShortURLTest(request):
    rescode = 1
    rtnVal = {"rescode": rescode}
    if request.method == 'POST':
        encText = urllib.parse.quote("http://d2.naver.com/helloworld/4874130")
        data = "url=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/util/v1/shorturl"
        request = App_Ajax(request, url)
        request.add_header("Content-Length", "0")

        try:
            response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        except HTTPError as e:
            rescode = str(e)
        except URLError as e:
            rescode = str(e)
        else:
            rescode = response.getcode()

        if(rescode==200):
            response_body = response.read()
            rtnVal["rescode"] = rescode
            rtnVal["resval"] = response_body.decode('utf-8')
        else:
            rtnVal["rescode"] = rescode
        return HttpResponse(json.dumps(rtnVal), content_type='application/json')
    else:
        return HttpResponse(json.dumps(rtnVal), content_type='application/json')


@csrf_exempt
def APIGW(request):
    if request.method=='POST':
        rtnVal = {}
        # url = "https://ta50do4nv5.apigw.ntruss.com" + uri
        # uri = "/api-test/v1/api"
        url = request.POST.get("url_value")
        uri = url[url.find('apigw.ntruss.com')+len('apigw.ntruss.com'):]

        try:
            res = Hmac_Ajax(request, uri)
        except URLError as e:
            rescode = "URL ERROR"
        except HTTPError as e:
            rescode = "HTTP ERROR"
        else:
            rescode = res.getcode()
        if(rescode == 200):
            response_body = res.read()
            rtnVal = {"rescode": rescode, "url": url, "uri": uri}
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
        else:
            print("Error Code:" + rescode)
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')

    else:
        return render(request, 'ncloud/ai_application/api_gateway.html')

@csrf_exempt
def geoLocation(request):
    if request.method=='POST':
        rtnVal = {}
        ip = request.POST.get("ip_value")
        #ip = "211.249.69.177"
        uri = "/geolocation/v1/geoLocation?ip=" + ip + "&ext=t&responseFormatType=json"
        url = "https://ncloud.apigw.ntruss.com" + uri

        try:
            res = Hmac_Ajax(request, uri)
        except URLError as e:
            rescode = str(e)
        except HTTPError as e:
            rescode = str(e)
        else:
            rescode = res.getcode()
        if(rescode == 200):
            response_body = res.read()
            result = response_body.decode('utf-8')
            rtnVal = {"rescode": rescode, "result": result}
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')
        else:
            print("Error Code:" + rescode)
            return HttpResponse(json.dumps(rtnVal), content_type='application/json')

    else:
        return render(request, 'ncloud/ai_application/geoLocation.html')
